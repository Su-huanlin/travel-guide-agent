from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from travel_guide.agent.runner import run_agent
from travel_guide.pipeline.build import build_trip
from travel_guide.pipeline.verify import verify_trip

app = typer.Typer(
    name="tg",
    help="Travel Guide Agent — brief → MD/CSV handbook → Excel/HTML/PDF",
    add_completion=False,
)
console = Console()

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCAFFOLD = ROOT / "templates" / "trip-scaffold"
DEFAULT_WORKSPACE = ROOT / "workspace"


@app.command("init")
def init_trip(
    name: str = typer.Argument(..., help="Trip folder name under workspace/"),
    scaffold: Path = typer.Option(DEFAULT_SCAFFOLD, help="Scaffold directory"),
) -> None:
    """Copy empty trip scaffold (no LLM)."""
    trip_root = DEFAULT_WORKSPACE / name
    from travel_guide.agent.tools import copy_scaffold

    copy_scaffold(scaffold, trip_root)
    console.print(f"[green]Scaffold ready:[/green] {trip_root}")
    console.print("Next: edit brief.md / meta.json, or run `tg run --brief ...`")


@app.command("run")
def run_trip(
    brief: Path = typer.Option(..., exists=True, dir_okay=False, help="Path to brief.md"),
    name: Optional[str] = typer.Option(None, help="Trip folder name; default from brief stem"),
    out: Optional[Path] = typer.Option(None, help="Trip root directory override"),
    scaffold: Path = typer.Option(DEFAULT_SCAFFOLD, exists=True, file_okay=False),
    no_pdf: bool = typer.Option(False, help="Skip HTML→PDF step"),
    scaffold_only: bool = typer.Option(False, help="Only copy scaffold, do not call LLM"),
) -> None:
    """Run staged LLM agent + deterministic build/verify."""
    trip_name = name or brief.stem.replace(" ", "-")
    trip_root = out or (DEFAULT_WORKSPACE / trip_name)
    run_agent(
        brief_path=brief,
        trip_root=trip_root,
        scaffold_dir=scaffold,
        make_pdf=not no_pdf,
        skip_llm=scaffold_only,
    )
    console.print(f"\n[bold green]Done.[/bold green] Open: {trip_root / 'output'}")


@app.command("build")
def build_cmd(
    trip: Path = typer.Argument(..., exists=True, file_okay=False, help="Trip root"),
    no_pdf: bool = typer.Option(False, help="Skip PDF"),
) -> None:
    """Rebuild outputs from existing content/data (no LLM)."""
    paths = build_trip(trip, make_pdf=not no_pdf)
    for path in paths:
        console.print(str(path))
    verify_trip(trip, require_pdf=not no_pdf)
    console.print("[green]Build + verify OK[/green]")


@app.command("verify")
def verify_cmd(
    trip: Path = typer.Argument(..., exists=True, file_okay=False),
    no_pdf: bool = typer.Option(False),
) -> None:
    """Verify existing output files."""
    verify_trip(trip, require_pdf=not no_pdf)
    console.print("[green]Verify OK[/green]")


if __name__ == "__main__":
    app()
