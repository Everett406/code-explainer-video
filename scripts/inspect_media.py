#!/usr/bin/env python3
"""Inspect user-supplied media and write a JSON asset manifest."""

import argparse
import json
import subprocess
from pathlib import Path

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".svg"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus"}
FONT_EXT = {".ttf", ".otf", ".woff", ".woff2"}
DATA_EXT = {".csv", ".tsv", ".json", ".jsonl", ".xlsx", ".xls", ".parquet"}
DOC_EXT = {".txt", ".md", ".pdf", ".docx", ".pptx", ".srt", ".vtt"}


def category(path):
    ext = path.suffix.lower()
    for name, extensions in (
        ("image", IMAGE_EXT),
        ("video", VIDEO_EXT),
        ("audio", AUDIO_EXT),
        ("font", FONT_EXT),
        ("data", DATA_EXT),
        ("document", DOC_EXT),
    ):
        if ext in extensions:
            return name
    return "other"


def probe(path):
    command = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def frame_rate(value):
    if not value or value == "0/0":
        return None
    numerator, denominator = value.split("/", 1)
    return round(int(numerator) / int(denominator), 6) if int(denominator) else None


def image_info(path, record):
    try:
        from PIL import Image
        with Image.open(path) as image:
            record.update(width=image.width, height=image.height, mode=image.mode)
        return
    except ImportError:
        pass
    except Exception:
        pass
    if path.suffix.lower() == ".svg":
        return
    data = probe(path)
    stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if stream:
        record.update(width=stream.get("width"), height=stream.get("height"))


def av_info(path, record):
    data = probe(path)
    duration = data.get("format", {}).get("duration")
    if duration is not None:
        record["duration_seconds"] = round(float(duration), 6)
    for stream in data.get("streams", []):
        kind = stream.get("codec_type")
        if kind == "video" and "video" not in record:
            record["video"] = {
                "codec": stream.get("codec_name"),
                "width": stream.get("width"),
                "height": stream.get("height"),
                "fps": frame_rate(stream.get("avg_frame_rate")),
            }
        elif kind == "audio" and "audio" not in record:
            record["audio"] = {
                "codec": stream.get("codec_name"),
                "sample_rate": stream.get("sample_rate"),
                "channels": stream.get("channels"),
            }


def inspect(path):
    record = {
        "path": str(path.resolve()),
        "name": path.name,
        "category": category(path),
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
    }
    try:
        if record["category"] == "image":
            image_info(path, record)
        elif record["category"] in {"video", "audio"}:
            av_info(path, record)
    except Exception as error:
        record["inspection_error"] = str(error)
    return record


def collect(paths, output_path):
    files = set()
    for value in paths:
        path = Path(value)
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        if path.is_file():
            files.add(path)
        else:
            for child in path.rglob("*"):
                if child.is_file() and not any(part.startswith(".") for part in child.parts):
                    files.add(child)
    if output_path:
        files.discard(output_path)
    return sorted(files, key=lambda item: str(item))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories to inspect")
    parser.add_argument("--json", dest="json_path", help="Also save the manifest here")
    args = parser.parse_args()
    output_path = Path(args.json_path).resolve() if args.json_path else None
    files = collect(args.paths, output_path)
    records = [inspect(path) for path in files]
    payload = {"asset_count": len(records), "assets": records}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
