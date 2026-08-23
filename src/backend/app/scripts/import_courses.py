"""Load the Track A curriculum CSVs into the existing tables.

Default files (canonical):

    PathToGrad/data/Courses.csv
    PathToGrad/data/offerings.csv

Usage (from src/backend, with PYTHONPATH=.):

    python -m app.scripts.import_courses
    python -m app.scripts.import_courses path/to/Courses.csv

A legacy STT dump is still accepted if you pass one explicitly, but it only
fills the COURSE table. Prerequisites, GEN+SE curriculum rows, and offerings
come from the normalized files under PathToGrad/data/.

Requires seed.sql to have been applied first (curriculum CURR-TEST-2024
and academic term named 2026.1).
"""

from __future__ import annotations

import csv
import sys
import uuid
from collections import defaultdict
from datetime import time
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.deterministic.cadence import CadenceMismatchError, assert_offered_in
from app.models import (
    AcademicTerm,
    ClassSection,
    Course,
    CourseOffering,
    Curriculum,
    CurriculumCourse,
    Prerequisite,
    SectionMeeting,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_COURSES = REPO_ROOT / "data" / "Courses.csv"
DEFAULT_OFFERINGS = REPO_ROOT / "data" / "offerings.csv"

DEMO_CURRICULUM_ID = "CURR-TEST-2024"
DEMO_TERM_NAME = "2026.1"
DEMO_SPECS = {"GEN", "SE"}

DAY_NAME = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday",
}


def parse_time(value: str) -> time:
    hours, minutes = value.strip().split(":")[:2]
    return time(int(hours), int(minutes))


def is_normalized(fieldnames: list[str] | None) -> bool:
    if not fieldnames:
        return False
    return "course_code" in fieldnames and "spec_code" in fieldnames


def read_normalized(path: Path) -> tuple[list[dict], int]:
    rows: list[dict] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            if not raw or not raw.get("course_code"):
                continue
            rows.append(
                {
                    "spec_code": raw["spec_code"].strip(),
                    "semester_no": int(raw["semester_no"]),
                    "course_code": raw["course_code"].strip(),
                    "name_vi": raw["name_vi"].strip(),
                    "name_en": raw["name_en"].strip(),
                    "credits": int(raw["credits"]),
                    "is_mandatory": raw.get("is_mandatory", "").strip().upper()
                    == "TRUE",
                    "prerequisites": [
                        code.strip()
                        for code in raw.get("prerequisites", "").split(";")
                        if code.strip()
                    ],
                }
            )
    return rows, len(rows)


def read_legacy_stt(path: Path) -> tuple[list[dict], int]:
    """Fallback for an old comment-delimited STT dump, if one is passed explicitly."""
    rows: list[dict] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        next(reader, None)
        for raw in reader:
            if not raw or len(raw) < 4:
                continue
            if not raw[0].strip().isdigit():
                continue
            code = raw[1].strip()
            name = raw[2].strip()
            if not code or not name:
                continue
            rows.append(
                {
                    "spec_code": "",
                    "semester_no": 0,
                    "course_code": code,
                    "name_vi": name,
                    "name_en": "",
                    "credits": int(raw[3].strip()),
                    "is_mandatory": False,
                    "prerequisites": [],
                }
            )
    return rows, len(rows)


def upsert_courses(db: Session, rows: list[dict]) -> tuple[dict[str, Course], int, int, int]:
    by_code: dict[str, dict] = {}
    duplicates = 0
    for row in rows:
        code = row["course_code"]
        if code in by_code:
            duplicates += 1
            continue
        by_code[code] = row

    inserted = 0
    updated = 0
    courses: dict[str, Course] = {}
    for code, row in by_code.items():
        existing = db.scalar(select(Course).where(Course.course_code == code))
        if existing:
            existing.name_vi = row["name_vi"]
            existing.name_en = row["name_en"]
            existing.credits = row["credits"]
            existing.status = "Active"
            courses[code] = existing
            updated += 1
        else:
            course = Course(
                course_id=str(uuid.uuid4()),
                course_code=code,
                name_vi=row["name_vi"],
                name_en=row["name_en"],
                credits=row["credits"],
                status="Active",
            )
            db.add(course)
            courses[code] = course
            inserted += 1
    db.flush()
    return courses, inserted, updated, duplicates


def import_prerequisites(db: Session, rows: list[dict], courses: dict[str, Course]) -> int:
    added = 0
    seen: set[tuple[str, str]] = set()
    for row in rows:
        if row["spec_code"] not in DEMO_SPECS:
            continue
        course = courses.get(row["course_code"])
        if course is None:
            continue
        for req_code in row["prerequisites"]:
            required = courses.get(req_code)
            if required is None:
                print(f"WARN: prerequisite {req_code} for {row['course_code']} not in catalog")
                continue
            pair = (course.course_id, required.course_id)
            if pair in seen:
                continue
            seen.add(pair)
            exists = db.scalar(
                select(Prerequisite).where(
                    Prerequisite.course_id == course.course_id,
                    Prerequisite.required_course_id == required.course_id,
                )
            )
            if exists:
                continue
            db.add(
                Prerequisite(
                    course_id=course.course_id,
                    required_course_id=required.course_id,
                )
            )
            added += 1
    return added


def import_curriculum_courses(
    db: Session,
    rows: list[dict],
    courses: dict[str, Course],
) -> int:
    curriculum = db.scalar(
        select(Curriculum).where(Curriculum.curriculum_id == DEMO_CURRICULUM_ID)
    )
    if curriculum is None:
        print(
            f"WARN: curriculum {DEMO_CURRICULUM_ID} missing — "
            "apply seed.sql before importing GEN+SE rows"
        )
        return 0

    # Unique (curriculum, course): keep the earliest semester.
    chosen: dict[str, dict] = {}
    for row in rows:
        if row["spec_code"] not in DEMO_SPECS:
            continue
        code = row["course_code"]
        previous = chosen.get(code)
        if previous is None or row["semester_no"] < previous["semester_no"]:
            chosen[code] = row

    added = 0
    for code, row in chosen.items():
        course = courses[code]
        spec_code = row["spec_code"]
        requirement_type = "Core" if row["is_mandatory"] else "Elective"
        exists = db.scalar(
            select(CurriculumCourse).where(
                CurriculumCourse.curriculum_id == DEMO_CURRICULUM_ID,
                CurriculumCourse.course_id == course.course_id,
            )
        )
        if exists:
            exists.requirement_type = requirement_type
            exists.assigned_semester = row["semester_no"]
            exists.spec_code = spec_code
            continue
        db.add(
            CurriculumCourse(
                curr_course_id=str(uuid.uuid4()),
                curriculum_id=DEMO_CURRICULUM_ID,
                course_id=course.course_id,
                requirement_type=requirement_type,
                assigned_semester=row["semester_no"],
                spec_code=spec_code,
            )
        )
        added += 1
    return added


def import_offerings(db: Session, offerings_path: Path, courses: dict[str, Course]) -> tuple[int, int, int]:
    if not offerings_path.exists():
        print(f"WARN: offerings file not found: {offerings_path}")
        return 0, 0, 0

    term = db.scalar(select(AcademicTerm).where(AcademicTerm.name == DEMO_TERM_NAME))
    if term is None:
        print(
            f"WARN: academic term named {DEMO_TERM_NAME} missing — "
            "apply the updated seed.sql before importing offerings"
        )
        return 0, 0, 0

    assigned_by_course_id = {
        row.course_id: row.assigned_semester
        for row in db.scalars(
            select(CurriculumCourse).where(
                CurriculumCourse.curriculum_id == DEMO_CURRICULUM_ID
            )
        )
    }

    with offerings_path.open(encoding="utf-8-sig", newline="") as fh:
        meetings = list(csv.DictReader(fh))

    by_course: dict[str, list[dict]] = defaultdict(list)
    for row in meetings:
        by_course[row["course_code"].strip()].append(row)

    offerings = 0
    sections = 0
    meeting_rows = 0
    for course_code, rows in by_course.items():
        course = courses.get(course_code)
        if course is None:
            print(f"WARN: offering for unknown course {course_code}")
            continue

        assigned_semester = assigned_by_course_id.get(course.course_id)
        if assigned_semester is None:
            raise CadenceMismatchError(
                f"Offering for {course_code} has no GEN+SE curriculum row, "
                "so its yearly slot cannot be checked."
            )
        assert_offered_in(
            assigned_semester,
            term.term_type,
            course_code=course_code,
        )

        offering = db.scalar(
            select(CourseOffering).where(
                CourseOffering.course_id == course.course_id,
                CourseOffering.term_id == term.term_id,
            )
        )
        if offering is None:
            offering = CourseOffering(
                offering_id=str(uuid.uuid4()),
                course_id=course.course_id,
                term_id=term.term_id,
                status="Active",
            )
            db.add(offering)
            db.flush()
            offerings += 1

        by_section: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            by_section[row["section_code"].strip()].append(row)

        for section_code, section_rows in by_section.items():
            capacity = max(int(r["capacity"]) for r in section_rows)
            section = db.scalar(
                select(ClassSection).where(
                    ClassSection.offering_id == offering.offering_id,
                    ClassSection.section_code == section_code,
                )
            )
            if section is None:
                section = ClassSection(
                    section_id=str(uuid.uuid4()),
                    offering_id=offering.offering_id,
                    section_code=section_code,
                    capacity=capacity,
                    status="Active",
                )
                db.add(section)
                db.flush()
                sections += 1

            for row in section_rows:
                day = DAY_NAME[row["day_of_week"].strip()]
                start = parse_time(row["start_time"])
                end = parse_time(row["end_time"])
                exists = db.scalar(
                    select(SectionMeeting).where(
                        SectionMeeting.section_id == section.section_id,
                        SectionMeeting.day_of_week == day,
                        SectionMeeting.start_time == start,
                        SectionMeeting.end_time == end,
                    )
                )
                if exists:
                    continue
                db.add(
                    SectionMeeting(
                        meeting_id=str(uuid.uuid4()),
                        section_id=section.section_id,
                        meeting_type=row["section_type"].strip(),
                        day_of_week=day,
                        start_time=start,
                        end_time=end,
                        room=row["room"].strip(),
                        instructor=None,
                    )
                )
                meeting_rows += 1
    return offerings, sections, meeting_rows


def import_data(courses_path: Path, offerings_path: Path | None = None) -> None:
    with courses_path.open(encoding="utf-8-sig", newline="") as fh:
        header = fh.readline()
    normalized = "spec_code" in header and "course_code" in header

    if normalized:
        rows, actual = read_normalized(courses_path)
    else:
        rows, actual = read_legacy_stt(courses_path)
        print("Note: legacy STT dump detected — courses only, no prereqs/offerings")

    with SessionLocal() as db:
        courses, inserted, updated, duplicates = upsert_courses(db, rows)
        prereq_count = 0
        curr_count = 0
        off_n = sec_n = meet_n = 0
        if normalized:
            prereq_count = import_prerequisites(db, rows, courses)
            curr_count = import_curriculum_courses(db, rows, courses)
            off_path = offerings_path or courses_path.with_name("offerings.csv")
            off_n, sec_n, meet_n = import_offerings(db, off_path, courses)
        db.commit()

    print("Import completed")
    print(f"Source: {courses_path}")
    print(f"Course rows read: {actual}")
    print(f"Unique courses: {len(courses)}")
    print(f"Duplicate occurrences skipped: {duplicates}")
    print(f"Courses inserted: {inserted}")
    print(f"Courses updated: {updated}")
    if normalized:
        print(f"Prerequisite edges added: {prereq_count}")
        print(f"GEN+SE curriculum rows added: {curr_count}")
        print(f"Offerings inserted: {off_n}")
        print(f"Sections inserted: {sec_n}")
        print(f"Meetings inserted: {meet_n}")
        print(f"Missing offering (intentional): CSC13001 has no rows in offerings.csv")


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: python -m app.scripts.import_courses [path-to-Courses.csv]")
        raise SystemExit(1)

    path = Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_COURSES
    if not path.exists():
        raise FileNotFoundError(
            f"{path}\nExpected the Track A file at {DEFAULT_COURSES}"
        )
    import_data(path)


if __name__ == "__main__":
    main()
