"""Stage-3 course-code allow-list (NFR-06 / NEW-TC-51)."""

from __future__ import annotations

import re

COURSE_CODE_RE = re.compile(r"\b(?:CSC|MTH|BAA|PHY)\d{5}\b", re.IGNORECASE)


def extract_course_codes(text: str) -> set[str]:
    return {match.group(0).upper() for match in COURSE_CODE_RE.finditer(text or "")}


def prose_is_allowed(prose: str, allowed: set[str]) -> bool:
    allowed_upper = {code.upper() for code in allowed}
    return extract_course_codes(prose).issubset(allowed_upper)
