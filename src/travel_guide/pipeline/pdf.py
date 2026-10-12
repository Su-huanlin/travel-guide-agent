from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .meta import load_meta


def find_browser() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def html_to_pdf(html_path: Path, pdf_path: Path, browser: Path) -> Path:
    with tempfile.TemporaryDirectory(prefix="tg-pdf-") as tmp:
        tmp_path = Path(tmp)
        profile = tmp_path / "profile"
        profile.mkdir()
        temp_html = tmp_path / "input.html"
        temp_pdf = tmp_path / "output.pdf"
        shutil.copy2(html_path, temp_html)
        uri = temp_html.resolve().as_uri()
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={temp_pdf}",
            uri,
        ]
        subprocess.run(cmd, check=False, capture_output=True)
        for _ in range(40):
            if temp_pdf.exists() and temp_pdf.stat().st_size >= 10_000:
                break
            time.sleep(0.5)
        if not temp_pdf.exists() or temp_pdf.stat().st_size < 10_000:
            raise RuntimeError(f"PDF generation failed for {html_path.name}")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(temp_pdf, pdf_path)
    return pdf_path


def html_files_to_pdf(trip_root: Path, meta: dict | None = None) -> list[Path]:
    meta = meta or load_meta(trip_root)
    browser = find_browser()
    if browser is None:
        raise RuntimeError("Edge/Chrome not found; cannot generate PDF. HTML/XLSX are still available.")
    output = trip_root / "output"
    pairs = [
        (meta["html_handbook"], meta["pdf_handbook"]),
        (meta["html_map"], meta["pdf_map"]),
    ]
    written: list[Path] = []
    for html_name, pdf_name in pairs:
        html_path = output / html_name
        if not html_path.exists():
            continue
        written.append(html_to_pdf(html_path, output / pdf_name, browser))
    return written
