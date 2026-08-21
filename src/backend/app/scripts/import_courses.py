import csv
import sys
import uuid
from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models.academic import Course


def read_courses(csv_path: Path):
    unique_courses: dict[str, tuple[str, int]] = {}

    actual_rows = 0
    duplicate_rows = 0

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.reader(file)

        # Skip CSV header
        next(reader, None)

        for row in reader:
            # Blank row
            if not row:
                continue

            # Metadata/comment row
            if len(row) == 1:
                continue

            # Need 4 CSV columns
            if len(row) < 4:
                continue

            stt = row[0].strip()

            # Real course rows have a numeric STT
            if not stt.isdigit():
                continue

            course_code = row[1].strip()
            course_name = row[2].strip()
            credits_text = row[3].strip()

            if not course_code:
                continue

            if not course_name:
                continue

            try:
                credits = int(credits_text)
            except ValueError:
                raise ValueError(
                    f"Invalid credits for {course_code}: {credits_text}"
                )

            actual_rows += 1

            if course_code in unique_courses:
                old_name, old_credits = unique_courses[course_code]

                if old_name != course_name or old_credits != credits:
                    raise ValueError(
                        f"Conflicting duplicate course: {course_code}"
                    )

                duplicate_rows += 1
                continue

            unique_courses[course_code] = (
                course_name,
                credits,
            )

    return unique_courses, actual_rows, duplicate_rows


def import_courses(csv_path: Path):
    courses, actual_rows, duplicate_rows = read_courses(csv_path)

    inserted = 0
    updated = 0

    with SessionLocal() as db:
        for course_code, (course_name, credits) in courses.items():

            existing = db.scalar(
                select(Course).where(
                    Course.course_code == course_code
                )
            )

            if existing:
                existing.course_name = course_name
                existing.credits = credits
                existing.status = "Active"
                updated += 1

            else:
                db.add(
                    Course(
                        course_id=str(uuid.uuid4()),
                        course_code=course_code,
                        course_name=course_name,
                        credits=credits,
                        status="Active",
                    )
                )

                inserted += 1

        db.commit()

    print("Import completed")
    print(f"Actual course rows read: {actual_rows}")
    print(f"Unique courses: {len(courses)}")
    print(f"Duplicate occurrences skipped: {duplicate_rows}")
    print(f"Inserted: {inserted}")
    print(f"Updated: {updated}")


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m app.scripts.import_courses "
            "<path-to-Courses.csv>"
        )
        raise SystemExit(1)

    path = Path(sys.argv[1])

    if not path.exists():
        raise FileNotFoundError(path)

    import_courses(path)


if __name__ == "__main__":
    main()
