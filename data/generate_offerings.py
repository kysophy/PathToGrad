"""A-04 — generate a synthetic demo-term timetable for GEN + SE.

Emits:

    term_code,course_code,section_code,section_type,day_of_week,start_time,end_time,room,capacity

Clock times only. LT occupies a half-day; TH is a two-hour practical.

Cadence: a course assigned to semester S is offered in a term whose
term_type matches position_of(S) = S % 3 (see A-09b). This file was
generated for programme semesters 2, 5 and 8 — all of which land on
position 2 (Semester2) — so the demo term (2026.1, term_type=Semester2
per the C-01 freeze) carries GEN semesters 2 and 5 plus SE semester 8.
No term number is stored anywhere; this docstring is the only place
"T=8" ever appears, purely as a description of how this fixture file
was built.

Fixtures (printed as 1-based CSV row numbers after generation):

1. Missing offering — CSC13001 Windows Programming has no rows.
2. Plausible clash — CSC13010-01 LT Mon 07:30–11:10 vs CSC13005-01 LT Mon 07:30–11:10.
3. All-sections clash — every CSC13009 LT is Monday morning, matching every CSC13010 LT.

Conflict convention (for A-14): half-open intervals. Touching endpoints do not clash.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
COURSES_PATH = DATA_DIR / "Courses.csv"
OUT_PATH = DATA_DIR / "offerings.csv"

TERM_CODE = "2026.1"
DEMO_TERM_NO = 8
DEMO_SPECS = ("GEN", "SE")
MISSING_OFFERING = "CSC13001"

LT_MORNING = ("07:30", "11:10")
LT_AFTERNOON = ("13:30", "17:10")
TH_SLOTS = [
    ("07:30", "09:30"),
    ("09:30", "11:30"),
    ("13:30", "15:30"),
    ("15:30", "17:30"),
]

# Default LT half-days. Monday morning is reserved for the clash fixtures.
LT_DEFAULTS = [
    ("Tue", *LT_MORNING),
    ("Tue", *LT_AFTERNOON),
    ("Wed", *LT_MORNING),
    ("Wed", *LT_AFTERNOON),
    ("Thu", *LT_MORNING),
    ("Thu", *LT_AFTERNOON),
    ("Fri", *LT_MORNING),
    ("Fri", *LT_AFTERNOON),
    ("Sat", *LT_MORNING),
    ("Sat", *LT_AFTERNOON),
    ("Mon", *LT_AFTERNOON),
]

TH_DEFAULTS = [
    ("Wed", "13:30", "15:30"),
    ("Thu", "13:30", "15:30"),
    ("Fri", "13:30", "15:30"),
    ("Sat", "13:30", "15:30"),
    ("Tue", "15:30", "17:30"),
    ("Wed", "15:30", "17:30"),
    ("Thu", "15:30", "17:30"),
    ("Fri", "15:30", "17:30"),
    ("Sat", "15:30", "17:30"),
    ("Tue", "07:30", "09:30"),
    ("Wed", "07:30", "09:30"),
    ("Thu", "07:30", "09:30"),
]

ROOMS_LT = ["I.11", "I.12", "I.13", "E.201", "E.202", "C.201", "C.202", "F.102"]
ROOMS_TH = ["TH.01", "TH.02", "TH.03", "TH.04", "LAB.A", "LAB.B"]

THREE_SECTION_COURSES = {
    "CSC10004",
    "CSC10006",
    "CSC13010",
    "CSC13009",
    "CSC13005",
}

FIXTURE_COURSES = {"CSC13010", "CSC13005", "CSC13009", "BAA00102"}


def is_offered_in(semester_no: int, term_no: int) -> bool:
    return semester_no % 3 == term_no % 3


def load_catalog(path: Path) -> list[dict]:
    catalog: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["spec_code"] not in DEMO_SPECS:
                continue
            if not is_offered_in(int(row["semester_no"]), DEMO_TERM_NO):
                continue
            code = row["course_code"]
            if code in seen:
                continue
            seen.add(code)
            catalog.append(row)
    return catalog


def meeting(
    course_code: str,
    section_code: str,
    section_type: str,
    day: str,
    start: str,
    end: str,
    room: str,
    capacity: int = 60,
) -> dict:
    return {
        "term_code": TERM_CODE,
        "course_code": course_code,
        "section_code": section_code,
        "section_type": section_type,
        "day_of_week": day,
        "start_time": start,
        "end_time": end,
        "room": room,
        "capacity": capacity,
    }


def overlap(a: dict, b: dict) -> bool:
    """Half-open: touching endpoints do not clash."""
    if a["day_of_week"] != b["day_of_week"]:
        return False
    return a["start_time"] < b["end_time"] and b["start_time"] < a["end_time"]


def clash_fixture_rows() -> list[dict]:
    rows: list[dict] = []

    # CSC13010 Software Design — every LT is Monday morning.
    rows += [
        meeting("CSC13010", "01", "LT", "Mon", *LT_MORNING, "I.11"),
        meeting("CSC13010", "01", "TH", "Wed", "13:30", "15:30", "TH.01"),
        meeting("CSC13010", "02", "LT", "Mon", *LT_MORNING, "I.12"),
        meeting("CSC13010", "02", "TH", "Thu", "13:30", "15:30", "TH.02"),
        meeting("CSC13010", "03", "LT", "Mon", *LT_MORNING, "I.13"),
        meeting("CSC13010", "03", "TH", "Fri", "13:30", "15:30", "TH.03"),
    ]

    # CSC13005 Requirements — section 01 clashes with Design; 02/03 do not.
    rows += [
        meeting("CSC13005", "01", "LT", "Mon", *LT_MORNING, "E.201"),
        meeting("CSC13005", "01", "TH", "Wed", "15:30", "17:30", "LAB.A"),
        meeting("CSC13005", "02", "LT", "Fri", *LT_AFTERNOON, "E.202"),
        meeting("CSC13005", "02", "TH", "Sat", "07:30", "09:30", "LAB.B"),
        meeting("CSC13005", "03", "LT", "Thu", *LT_AFTERNOON, "C.201"),
        meeting("CSC13005", "03", "TH", "Sat", "09:30", "11:30", "TH.04"),
    ]

    # CSC13009 Mobile — every LT is Monday morning, so all clash with every Design LT.
    rows += [
        meeting("CSC13009", "01", "LT", "Mon", *LT_MORNING, "C.202"),
        meeting("CSC13009", "01", "TH", "Tue", "13:30", "15:30", "LAB.A"),
        meeting("CSC13009", "02", "LT", "Mon", *LT_MORNING, "F.102"),
        meeting("CSC13009", "02", "TH", "Tue", "15:30", "17:30", "LAB.B"),
        meeting("CSC13009", "03", "LT", "Mon", *LT_MORNING, "E.201"),
        meeting("CSC13009", "03", "TH", "Sat", "13:30", "15:30", "TH.01"),
    ]

    # BAA00102 Political Economy — Saturday / Friday, never Monday morning.
    rows += [
        meeting("BAA00102", "01", "LT", "Sat", *LT_MORNING, "C.201"),
        meeting("BAA00102", "01", "TH", "Sat", "13:30", "15:30", "TH.04"),
        meeting("BAA00102", "02", "LT", "Sat", *LT_AFTERNOON, "C.202"),
        meeting("BAA00102", "02", "TH", "Fri", "15:30", "17:30", "LAB.A"),
    ]
    return rows


def default_rows(catalog: list[dict]) -> list[dict]:
    skip = {MISSING_OFFERING} | FIXTURE_COURSES
    rows: list[dict] = []
    index = 0
    for course in catalog:
        code = course["course_code"]
        if code in skip:
            continue
        n_sections = 3 if code in THREE_SECTION_COURSES else 2
        for n in range(n_sections):
            section = f"{n + 1:02d}"
            lt_day, lt_start, lt_end = LT_DEFAULTS[(index + n) % len(LT_DEFAULTS)]
            th_day, th_start, th_end = TH_DEFAULTS[(index + n) % len(TH_DEFAULTS)]
            if th_day == lt_day:
                th_day, th_start, th_end = TH_DEFAULTS[(index + n + 3) % len(TH_DEFAULTS)]
            rows.append(
                meeting(
                    code,
                    section,
                    "LT",
                    lt_day,
                    lt_start,
                    lt_end,
                    ROOMS_LT[(index + n) % len(ROOMS_LT)],
                )
            )
            rows.append(
                meeting(
                    code,
                    section,
                    "TH",
                    th_day,
                    th_start,
                    th_end,
                    ROOMS_TH[(index + n) % len(ROOMS_TH)],
                    capacity=40,
                )
            )
        index += 1
    return rows


def row_numbers(rows: list[dict], pred) -> list[int]:
    """1-based CSV line numbers including the header as line 1."""
    return [i + 2 for i, row in enumerate(rows) if pred(row)]


def validate(rows: list[dict], catalog: list[dict]) -> None:
    if any(r["course_code"] == MISSING_OFFERING for r in rows):
        raise SystemExit(f"{MISSING_OFFERING} must have no offering rows")

    catalog_codes = {c["course_code"] for c in catalog}
    if MISSING_OFFERING not in catalog_codes:
        raise SystemExit(f"{MISSING_OFFERING} is not in the T={DEMO_TERM_NO} catalog")

    offered = {r["course_code"] for r in rows}
    expected = catalog_codes - {MISSING_OFFERING}
    missing = expected - offered
    extra = offered - catalog_codes
    if missing:
        raise SystemExit(f"Courses with no offering besides the deliberate miss: {sorted(missing)}")
    if extra:
        raise SystemExit(f"Offerings for unknown courses: {sorted(extra)}")

    by_code = {c["course_code"]: int(c["semester_no"]) for c in catalog}
    for code in offered:
        if not is_offered_in(by_code[code], DEMO_TERM_NO):
            raise SystemExit(f"{code} (sem {by_code[code]}) violates the mod-3 cadence")

    design_lt = [r for r in rows if r["course_code"] == "CSC13010" and r["section_type"] == "LT"]
    req_01 = next(
        r
        for r in rows
        if r["course_code"] == "CSC13005"
        and r["section_code"] == "01"
        and r["section_type"] == "LT"
    )
    if not any(overlap(req_01, d) for d in design_lt):
        raise SystemExit("Expected CSC13005-01 LT to clash with Design")

    req_escape = [
        r
        for r in rows
        if r["course_code"] == "CSC13005"
        and r["section_code"] in {"02", "03"}
        and r["section_type"] == "LT"
    ]
    if not req_escape or all(any(overlap(r, d) for d in design_lt) for r in req_escape):
        raise SystemExit("Requirements needs at least one LT that does not clash with Design")

    mobile_lt = [r for r in rows if r["course_code"] == "CSC13009" and r["section_type"] == "LT"]
    for mobile in mobile_lt:
        if not all(overlap(mobile, d) for d in design_lt):
            raise SystemExit(
                f"CSC13009-{mobile['section_code']} LT does not clash with every Design LT"
            )

    # Touching endpoints must not count as a clash (TH 07:30–09:30 vs 09:30–11:30).
    early = {"start_time": "07:30", "end_time": "09:30", "day_of_week": "Mon"}
    late = {"start_time": "09:30", "end_time": "11:30", "day_of_week": "Mon"}
    if overlap(early, late):
        raise SystemExit("Half-open convention broken: touching TH slots must not clash")


def print_fixtures(rows: list[dict]) -> None:
    def is_design_01_lt(r: dict) -> bool:
        return (
            r["course_code"] == "CSC13010"
            and r["section_code"] == "01"
            and r["section_type"] == "LT"
        )

    def is_req_01_lt(r: dict) -> bool:
        return (
            r["course_code"] == "CSC13005"
            and r["section_code"] == "01"
            and r["section_type"] == "LT"
        )

    def is_mobile_lt(r: dict) -> bool:
        return r["course_code"] == "CSC13009" and r["section_type"] == "LT"

    def is_design_lt(r: dict) -> bool:
        return r["course_code"] == "CSC13010" and r["section_type"] == "LT"

    def is_available(r: dict) -> bool:
        return r["course_code"] == "CSC10004" and r["section_code"] == "01" and r["section_type"] == "LT"

    print(f"Term {TERM_CODE} (T={DEMO_TERM_NO}): {len(rows)} meeting rows")
    print(f"  TD-OFFERING-MISSING : {MISSING_OFFERING} (no rows)")
    print(f"  TD-OFFERING-AVAILABLE: CSC10004 LT 01  rows {row_numbers(rows, is_available)}")
    print(
        "  Plausible clash      : "
        f"CSC13010-01 LT rows {row_numbers(rows, is_design_01_lt)}  vs  "
        f"CSC13005-01 LT rows {row_numbers(rows, is_req_01_lt)}"
    )
    print(
        "  All-sections clash   : "
        f"CSC13009 LT rows {row_numbers(rows, is_mobile_lt)}  overlap  "
        f"CSC13010 LT rows {row_numbers(rows, is_design_lt)}"
    )


def main() -> int:
    catalog = load_catalog(COURSES_PATH)
    rows = clash_fixture_rows() + default_rows(catalog)
    validate(rows, catalog)
    fieldnames = [
        "term_code",
        "course_code",
        "section_code",
        "section_type",
        "day_of_week",
        "start_time",
        "end_time",
        "room",
        "capacity",
    ]
    with OUT_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print_fixtures(rows)
    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
