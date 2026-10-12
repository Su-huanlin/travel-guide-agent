from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_META: dict[str, Any] = {
    "title": "旅行攻略手册",
    "subtitle": "多日行程指南",
    "cover_facts": [],
    "footer_note": "门票、航班、天气、道路信息出发前请再次核验；地图不替代实时导航。",
    "xlsx_itinerary": "每日行程与预算.xlsx",
    "xlsx_waypoints": "导航与摄影点位.xlsx",
    "html_handbook": "旅行攻略手册.html",
    "html_map": "A3总路线图.html",
    "pdf_handbook": "旅行攻略手册.pdf",
    "pdf_map": "A3总路线图.pdf",
    "forbidden_terms": [],
    "required_terms": [],
}


def load_meta(trip_root: Path) -> dict[str, Any]:
    path = trip_root / "meta.json"
    meta = dict(DEFAULT_META)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("meta.json must be a JSON object")
        meta.update(data)
    return meta
