"""Illustrative “what is taught” notes. Not an official HCMUS syllabus."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_DEFAULT = (
    Path(__file__).resolve().parents[4] / "data" / "course_briefs.json"
)


def briefs_path() -> Path:
    return _DEFAULT


@lru_cache(maxsize=1)
def load_briefs(path: str | None = None) -> dict[str, dict[str, Any]]:
    target = Path(path) if path else _DEFAULT
    if not target.is_file():
        return {}
    payload = json.loads(target.read_text(encoding="utf-8"))
    return {str(code).upper(): value for code, value in payload.items()}


def get_brief(course_code: str, path: str | None = None) -> dict[str, Any] | None:
    return load_briefs(path).get(course_code.upper())
