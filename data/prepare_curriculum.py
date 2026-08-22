"""A-01 / A-02 / A-02b / A-03 — normalize Courses.csv.

Reads the original comment-delimited dump and writes a loader-ready CSV:

    spec_code,semester_no,course_code,name_vi,name_en,credits,is_mandatory,prerequisites

Semesters 1–6 are stored once as spec_code=GEN. Semesters 7–9 keep all nine
specializations. is_mandatory is TRUE iff the course code starts with CSC or MTH.
Prerequisites are filled on GEN rows and on SE rows only.

Do not hand-edit the output. Change this script and re-run.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "Materials and Notes" / "Courses.raw.csv"
OUT_PATH = Path(__file__).resolve().parent / "Courses.csv"

MAX_SEMESTER = 9
GEN_CODE = "GEN"
DEMO_SPEC = "SE"

# A-02 expected mandatory credits for GEN + SE, semesters 1–9.
EXPECTED_MANDATORY = [15, 8, 14, 12, 12, 8, 12, 16, 23]
EXPECTED_REQUIRED_CREDITS = 138

SPEC_MAP = {
    "Mạng máy tính và Viễn thông": "CN",
    "Hệ thống thông tin": "IS",
    "Kỹ thuật phần mềm": "SE",
    "Khoa học máy tính": "CS",
    "Công nghệ tri thức": "KT",
    "Thị giác máy tính": "CV",
    "An toàn thông tin": "SEC",
    "Khoa học dữ liệu": "DS",
    "Công nghệ thông tin": "IT",
}

SPEC_ORDER = ["CN", "IS", "SE", "CS", "KT", "CV", "SEC", "DS", "IT"]

# Derived SE prerequisite map. Every listed code is required (AND, passed-only).
# Empty / missing means no named tiên quyết.
SE_PREREQUISITES: dict[str, str] = {
    # Semester 2
    "CSC10004": "CSC10012",
    "MTH00058": "MTH00009",
    # Semester 3
    "CSC10003": "CSC10004",
    "CSC10009": "CSC00004",
    # Semester 4
    "CSC10014": "CSC10004;MTH00009",
    "CSC10008": "CSC10009",
    "MTH00006": "MTH00005",
    # Semester 5
    "CSC10006": "CSC10004",
    "CSC10007": "CSC10009",
    "MTH00007": "MTH00005",
    "BAA00022": "BAA00021",
    # Semester 6
    "PHY00007": "PHY00005",
    "CSC14003": "CSC10003;MTH00007",
    "MTH00057": "MTH00007;MTH00008",
    # Semester 7
    "CSC13002": "CSC10003",
    "CSC13008": "CSC10003;CSC10006",
    "CSC13102": "CSC10003",
    # Semester 8
    "CSC13005": "CSC13002",
    "CSC13009": "CSC10003;CSC13002",
    "CSC13001": "CSC10003",
    "CSC13010": "CSC13002;CSC10003",
    "BAA00102": "BAA00101",
    # Semester 9
    "CSC13003": "CSC13002;CSC13010",
    "CSC13006": "CSC13002",
    "CSC13106": "CSC13002;CSC13010",
    "CSC13112": "CSC13002;CSC10003",
}


def split_name(combined: str) -> tuple[str, str]:
    """Split 'Tiếng Việt (English)' on the last opening parenthesis."""
    text = combined.strip()
    if text.endswith(")") and "(" in text:
        idx = text.rfind("(")
        return text[:idx].strip(), text[idx + 1 : -1].strip()
    return text, ""


def is_mandatory_code(course_code: str) -> str:
    if course_code.startswith("CSC") or course_code.startswith("MTH"):
        return "TRUE"
    return "FALSE"


def parse_raw(path: Path) -> tuple[list[dict], list[dict]]:
    """Return (general_education_rows, specialization_rows)."""
    ge_rows: list[dict] = []
    spec_rows: list[dict] = []
    spec_code: str | None = None
    semester_no: int | None = None

    with path.open(encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                spec_match = re.search(r"CHUYÊN NGÀNH:\s*(.+?)\s*\(", line)
                if spec_match:
                    name = spec_match.group(1).strip()
                    if name not in SPEC_MAP:
                        raise SystemExit(f"Unknown specialization name: {name}")
                    spec_code = SPEC_MAP[name]
                    continue
                sem_match = re.search(r"Học kỳ\s+(\d+)", line)
                if sem_match:
                    semester_no = int(sem_match.group(1))
                continue
            if line.lower().startswith("stt,"):
                continue
            if semester_no is None:
                continue
            if semester_no > MAX_SEMESTER:
                continue

            row = next(csv.reader([line]))
            if len(row) < 4:
                raise SystemExit(f"Unparseable row: {line}")
            _, course_code, combined_name, credits = row[0], row[1], row[2], row[3]
            name_vi, name_en = split_name(combined_name)
            record = {
                "semester_no": semester_no,
                "course_code": course_code.strip(),
                "name_vi": name_vi,
                "name_en": name_en,
                "credits": int(credits.strip()),
            }
            if spec_code is None:
                ge_rows.append(record)
            else:
                spec_rows.append({**record, "spec_code": spec_code})
    return ge_rows, spec_rows


def make_output_row(spec_code: str, row: dict) -> dict:
    code = row["course_code"]
    fill_prereqs = spec_code in {GEN_CODE, DEMO_SPEC}
    return {
        "spec_code": spec_code,
        "semester_no": row["semester_no"],
        "course_code": code,
        "name_vi": row["name_vi"],
        "name_en": row["name_en"],
        "credits": row["credits"],
        "is_mandatory": is_mandatory_code(code),
        "prerequisites": SE_PREREQUISITES.get(code, "") if fill_prereqs else "",
    }


def build_rows(ge_rows: list[dict], spec_rows: list[dict]) -> list[dict]:
    spec_by_code: dict[str, list[dict]] = defaultdict(list)
    for row in spec_rows:
        spec_by_code[row["spec_code"]].append(row)

    out: list[dict] = []
    for row in ge_rows:
        out.append(make_output_row(GEN_CODE, row))
    for spec in SPEC_ORDER:
        for row in spec_by_code[spec]:
            payload = {k: v for k, v in row.items() if k != "spec_code"}
            out.append(make_output_row(spec, payload))
    return out


def demo_path(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["spec_code"] in {GEN_CODE, DEMO_SPEC}]


def validate(rows: list[dict]) -> list[str]:
    warnings: list[str] = []
    required = ("spec_code", "semester_no", "course_code", "credits")
    for i, row in enumerate(rows, start=2):
        for col in required:
            if row[col] in ("", None):
                raise SystemExit(f"Row {i} missing {col}")
        if not row["name_en"]:
            warnings.append(f"{row['course_code']}: empty name_en")
        if int(row["semester_no"]) > MAX_SEMESTER:
            raise SystemExit(f"Row {i} has semester {row['semester_no']} > {MAX_SEMESTER}")
        if row["is_mandatory"] not in {"TRUE", "FALSE"}:
            raise SystemExit(f"{row['spec_code']} {row['course_code']} missing is_mandatory")
        expected_flag = is_mandatory_code(row["course_code"])
        if row["is_mandatory"] != expected_flag:
            raise SystemExit(
                f"{row['course_code']} is_mandatory={row['is_mandatory']}, "
                f"expected {expected_flag} from CSC/MTH prefix"
            )

    gen_rows = [r for r in rows if r["spec_code"] == GEN_CODE]
    if len(gen_rows) != 26:
        raise SystemExit(f"GEN should appear 26 times, got {len(gen_rows)}")
    gen_codes = [r["course_code"] for r in gen_rows]
    if len(gen_codes) != len(set(gen_codes)):
        raise SystemExit("GEN contains a duplicated course code")

    all_codes = {r["course_code"] for r in rows}
    demo = demo_path(rows)
    demo_by_code = {r["course_code"]: r for r in demo}

    for row in demo:
        for req in [c for c in row["prerequisites"].split(";") if c]:
            if req not in all_codes:
                raise SystemExit(f"{row['course_code']} prereq {req} not in file")
            if req == row["course_code"]:
                raise SystemExit(f"Self-reference on {req}")
            if req not in demo_by_code:
                raise SystemExit(
                    f"{row['course_code']} prereq {req} is not on the GEN+SE path"
                )
            req_row = demo_by_code[req]
            if int(req_row["semester_no"]) > int(row["semester_no"]):
                raise SystemExit(
                    f"{row['course_code']} (sem {row['semester_no']}) requires "
                    f"{req} (sem {req_row['semester_no']}) — later semester"
                )
            if row["is_mandatory"] == "TRUE" and req_row["is_mandatory"] != "TRUE":
                raise SystemExit(
                    f"Mandatory {row['course_code']} depends on elective {req}"
                )

    graph: dict[str, list[str]] = {r["course_code"]: [] for r in demo}
    for row in demo:
        graph[row["course_code"]] = [c for c in row["prerequisites"].split(";") if c]

    WHITE, GREY, BLACK = 0, 1, 2
    color = {code: WHITE for code in graph}

    def dfs(node: str, stack: list[str]) -> None:
        color[node] = GREY
        stack.append(node)
        for nxt in graph[node]:
            if color[nxt] == GREY:
                cycle = stack[stack.index(nxt) :] + [nxt]
                raise SystemExit(f"Prerequisite cycle: {' -> '.join(cycle)}")
            if color[nxt] == WHITE:
                dfs(nxt, stack)
        stack.pop()
        color[node] = BLACK

    for code in graph:
        if color[code] == WHITE:
            dfs(code, [])

    print("Demo path (GEN + SE) mandatory credits by semester:")
    mandatory_totals: list[int] = []
    for sem in range(1, MAX_SEMESTER + 1):
        total = sum(
            int(r["credits"])
            for r in demo
            if int(r["semester_no"]) == sem and r["is_mandatory"] == "TRUE"
        )
        mandatory_totals.append(total)
        expected = EXPECTED_MANDATORY[sem - 1]
        status = "OK" if total == expected else "FAIL"
        print(f"  semester {sem}: {total}  (expected {expected})  [{status}]")
        if total != expected:
            raise SystemExit(
                f"Semester {sem} mandatory total {total} != expected {expected}"
            )

    required_credits = sum(max(n, 14) for n in mandatory_totals)
    mandatory_sum = sum(mandatory_totals)
    print(f"Mandatory sum: {mandatory_sum}")
    print(
        f"required_credits = sum(max(mandatory, 14)) = {required_credits}  "
        f"(expected {EXPECTED_REQUIRED_CREDITS})"
    )
    if required_credits != EXPECTED_REQUIRED_CREDITS:
        raise SystemExit(
            f"required_credits {required_credits} != {EXPECTED_REQUIRED_CREDITS}"
        )

    seen: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["spec_code"], row["course_code"])
        sem = int(row["semester_no"])
        if key in seen and seen[key] != sem:
            warnings.append(
                f"Duplicate {key[0]}/{key[1]} in semesters {seen[key]} and {sem} "
                "(loader should keep earliest)"
            )
        else:
            seen[key] = sem
    return warnings


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "spec_code",
        "semester_no",
        "course_code",
        "name_vi",
        "name_en",
        "credits",
        "is_mandatory",
        "prerequisites",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if not RAW_PATH.exists():
        raise SystemExit(f"Raw curriculum not found: {RAW_PATH}")
    ge_rows, spec_rows = parse_raw(RAW_PATH)
    rows = build_rows(ge_rows, spec_rows)
    warnings = validate(rows)
    write_csv(rows, OUT_PATH)
    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")
    for warning in warnings:
        print(f"WARN: {warning}")
    print(f"GEN courses: {len(ge_rows)}; spec courses (7–9): {len(spec_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
