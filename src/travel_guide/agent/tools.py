from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


def copy_scaffold(scaffold_dir: Path, trip_root: Path) -> None:
    if trip_root.exists() and any(trip_root.iterdir()):
        # Allow merge into existing empty-ish dirs; refuse overwrite of content/
        content = trip_root / "content"
        if content.exists() and any(content.glob("*.md")):
            raise RuntimeError(f"Trip already has content/: {trip_root}")
    trip_root.mkdir(parents=True, exist_ok=True)
    for item in scaffold_dir.iterdir():
        dest = trip_root / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            if not dest.exists():
                shutil.copy2(item, dest)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_fenced_block(text: str, language: str | None = None) -> str:
    """Extract first markdown fenced code block, optionally filtered by language."""
    pattern = r"```([a-zA-Z0-9_-]*)\n(.*?)```"
    for match in re.finditer(pattern, text, flags=re.DOTALL):
        lang = match.group(1).strip().lower()
        body = match.group(2).strip("\n")
        if language is None or lang == language.lower() or lang == "":
            return body
    # Fallback: whole text if it already looks like CSV/MD
    return text.strip()


def extract_json_object(text: str) -> dict:
    block = extract_fenced_block(text, "json")
    try:
        data = json.loads(block)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < 0:
            raise
        data = json.loads(text[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object")
    return data


def list_trip_files(trip_root: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(trip_root.rglob("*")):
        if path.is_file() and "output" not in path.parts and "__pycache__" not in path.parts:
            files.append(str(path.relative_to(trip_root)).replace("\\", "/"))
    return files
