#!/usr/bin/env python3
"""Validate an exported video with ffprobe and optional FFmpeg checks."""

import argparse
import json
import re
import subprocess
from pathlib import Path


def run(command):
    return subprocess.run(command, capture_output=True, text=True)


def parse_rate(value):
    if not value or value == "0/0":
        return None
    numerator, denominator = value.split("/", 1)
    return int(numerator) / int(denominator) if int(denominator) else None


def close(actual, expected, tolerance):
    return actual is not None and abs(actual - expected) <= tolerance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Video file to check")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--duration", type=float, help="Expected duration in seconds")
    parser.add_argument("--duration-tolerance", type=float, default=0.15)
    parser.add_argument("--codec", help="Expected video codec, for example h264")
    parser.add_argument("--audio", choices=("any", "required", "forbidden"), default="any")
    parser.add_argument("--decode", action="store_true", help="Decode the full file and report errors")
    parser.add_argument("--blackdetect", action="store_true", help="Fail on black segments of 0.2 s or longer")
    parser.add_argument("--json", dest="json_path", help="Also save the JSON report here")
    args = parser.parse_args()

    path = Path(args.video)
    if not path.is_file():
        parser.error(f"File does not exist: {path}")

    probe = run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ])
    if probe.returncode != 0:
        raise SystemExit(probe.stderr.strip() or "ffprobe failed")
    data = json.loads(probe.stdout)
    streams = data.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video_stream:
        raise SystemExit("No video stream found")
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    duration_value = data.get("format", {}).get("duration")
    duration = float(duration_value) if duration_value is not None else None
    fps = parse_rate(video_stream.get("avg_frame_rate"))

    report = {
        "file": str(path.resolve()),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "fps": fps,
        "duration_seconds": duration,
        "video_codec": video_stream.get("codec_name"),
        "audio_stream_count": len(audio_streams),
        "checks": [],
    }

    def add(name, passed, expected=None, actual=None):
        report["checks"].append({
            "name": name, "passed": bool(passed),
            "expected": expected, "actual": actual,
        })

    if args.width is not None:
        add("width", report["width"] == args.width, args.width, report["width"])
    if args.height is not None:
        add("height", report["height"] == args.height, args.height, report["height"])
    if args.fps is not None:
        add("fps", close(fps, args.fps, 0.01), args.fps, fps)
    if args.duration is not None:
        add("duration", close(duration, args.duration, args.duration_tolerance), args.duration, duration)
    if args.codec:
        add("video_codec", report["video_codec"] == args.codec, args.codec, report["video_codec"])
    if args.audio == "required":
        add("audio_required", len(audio_streams) > 0, "at least one", len(audio_streams))
    elif args.audio == "forbidden":
        add("audio_forbidden", len(audio_streams) == 0, "zero", len(audio_streams))

    if args.decode:
        decoded = run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"])
        message = decoded.stderr.strip()
        add("decode", decoded.returncode == 0 and not message, "no decode errors", message or None)

    if args.blackdetect:
        detected = run([
            "ffmpeg", "-v", "info", "-i", str(path),
            "-vf", "blackdetect=d=0.20:pix_th=0.02", "-an", "-f", "null", "-",
        ])
        segments = re.findall(r"black_start:[^\s]+ black_end:[^\s]+", detected.stderr)
        add("black_segments", detected.returncode == 0 and not segments, "none", segments)

    report["passed"] = all(check["passed"] for check in report["checks"])
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_path:
        output = Path(args.json_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
