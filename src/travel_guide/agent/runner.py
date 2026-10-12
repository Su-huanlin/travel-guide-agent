from __future__ import annotations

import json
import re
from pathlib import Path

from rich.console import Console

from travel_guide.agent.llm import chat
from travel_guide.agent.tools import (
    copy_scaffold,
    extract_fenced_block,
    extract_json_object,
    write_text,
)
from travel_guide.pipeline.build import build_trip
from travel_guide.pipeline.verify import verify_trip

console = Console()
PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")


def _system() -> str:
    return _load_prompt("system.md")


def _ask(stage_prompt: str, user_payload: str) -> str:
    return chat(_system() + "\n\n" + stage_prompt, user_payload)


def _write_md_from_model(path: Path, model_text: str) -> None:
    body = extract_fenced_block(model_text, "markdown")
    if body.startswith("#") or body.startswith("##"):
        write_text(path, body + "\n")
    else:
        # model may return raw markdown without fence
        write_text(path, model_text.strip() + "\n")


def _write_csv_pack(trip_root: Path, model_text: str) -> list[str]:
    """Parse multiple ### data/xxx.csv + ```csv blocks."""
    written: list[str] = []
    pattern = re.compile(
        r"###\s*(data/[a-zA-Z0-9_\-]+\.csv)\s*```csv\s*(.*?)```",
        flags=re.DOTALL | re.IGNORECASE,
    )
    matches = list(pattern.finditer(model_text))
    if not matches:
        # looser: filename line then fence
        pattern2 = re.compile(
            r"(data/[a-zA-Z0-9_\-]+\.csv)[^\n]*\n```csv\s*(.*?)```",
            flags=re.DOTALL | re.IGNORECASE,
        )
        matches = list(pattern2.finditer(model_text))
    for match in matches:
        rel = match.group(1).replace("\\", "/")
        body = match.group(2).strip() + "\n"
        path = trip_root / rel
        write_text(path, body)
        written.append(rel)
    if not written:
        raise RuntimeError("CSV stage returned no parseable data/*.csv blocks")
    return written


def run_agent(
    *,
    brief_path: Path,
    trip_root: Path,
    scaffold_dir: Path,
    make_pdf: bool = True,
    skip_llm: bool = False,
) -> Path:
    """
    Staged agent:
      init scaffold → meta.json → route → daily → execution → csv → build → verify
    """
    brief = brief_path.read_text(encoding="utf-8")
    console.rule("[bold]Travel Guide Agent")
    console.print(f"Brief: {brief_path}")
    console.print(f"Trip:  {trip_root}")

    console.print("\n[cyan]Stage 0[/cyan] Copy scaffold")
    copy_scaffold(scaffold_dir, trip_root)
    write_text(trip_root / "brief.md", brief if brief_path.resolve() != (trip_root / "brief.md").resolve() else brief)

    if skip_llm:
        console.print("[yellow]skip_llm=True — only scaffold copied; fill content then run `tg build`.[/yellow]")
        return trip_root

    console.print("\n[cyan]Stage 1[/cyan] meta.json (LLM)")
    meta_raw = _ask(_load_prompt("stage_meta.md"), f"# Brief\n\n{brief}")
    meta = extract_json_object(meta_raw)
    write_text(trip_root / "meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    console.print(f"  title = {meta.get('title')}")

    console.print("\n[cyan]Stage 2[/cyan] content/01-route-design.md (LLM)")
    route_raw = _ask(
        _load_prompt("stage_route.md"),
        f"# Brief\n\n{brief}\n\n# meta.json\n\n```json\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n```",
    )
    _write_md_from_model(trip_root / "content" / "01-route-design.md", route_raw)

    route_text = (trip_root / "content" / "01-route-design.md").read_text(encoding="utf-8")

    console.print("\n[cyan]Stage 3[/cyan] content/02-daily-guide.md (LLM)")
    daily_raw = _ask(
        _load_prompt("stage_daily.md"),
        f"# Brief\n\n{brief}\n\n# Route design\n\n{route_text}",
    )
    _write_md_from_model(trip_root / "content" / "02-daily-guide.md", daily_raw)

    daily_text = (trip_root / "content" / "02-daily-guide.md").read_text(encoding="utf-8")

    console.print("\n[cyan]Stage 4[/cyan] content/03-execution-guide.md (LLM)")
    exec_raw = _ask(
        _load_prompt("stage_execution.md"),
        f"# Brief\n\n{brief}\n\n# Route\n\n{route_text}\n\n# Daily\n\n{daily_text[:12000]}",
    )
    _write_md_from_model(trip_root / "content" / "03-execution-guide.md", exec_raw)

    console.print("\n[cyan]Stage 5[/cyan] data/*.csv (LLM)")
    csv_raw = _ask(
        _load_prompt("stage_csv.md"),
        (
            f"# Brief\n\n{brief}\n\n# Route\n\n{route_text}\n\n"
            f"# Daily (truncated)\n\n{daily_text[:14000]}\n\n"
            f"# Execution\n\n{(trip_root / 'content' / '03-execution-guide.md').read_text(encoding='utf-8')[:8000]}"
        ),
    )
    written = _write_csv_pack(trip_root, csv_raw)
    console.print("  wrote: " + ", ".join(written))

    console.print("\n[cyan]Stage 6[/cyan] Deterministic build (no LLM)")
    paths = build_trip(trip_root, make_pdf=make_pdf)
    for path in paths:
        console.print(f"  {path}")

    console.print("\n[cyan]Stage 7[/cyan] Verify")
    verify_trip(trip_root, require_pdf=make_pdf)
    console.print("[green]All checks passed.[/green]")
    return trip_root
