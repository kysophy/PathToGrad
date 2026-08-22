USE pathtograd;


/*
============================================================
SYNTHETIC DEVELOPMENT / TEST DATA ONLY
These values are NOT claimed to be official university data.

Apply AFTER: alembic upgrade head
Do not apply fixtures/academic_planning_test_data.sql on a demo database.
============================================================
*/


INSERT IGNORE INTO users (
    user_id,
    full_name,
    email,
    password,
    role,
    account_status
)
VALUES (
    'USER-TEST-001',
    'Test Student',
    'student.test@example.com',
    'NOT_USED_DAY1',
    'Student',
    'Active'
);


INSERT IGNORE INTO faculty (
    faculty_id,
    name
)
VALUES (
    'FAC-TEST-001',
    'Test Faculty'
);


INSERT IGNORE INTO program_track (
    track_id,
    name,
    min_credits_per_term,
    max_credits_per_term,
    min_courses,
    max_courses
)
VALUES (
    'TRACK-STD-001',
    'CLC',
    14,
    24,
    4,
    6
);

-- INSERT IGNORE will not rename a row that already exists.
UPDATE program_track
SET name = 'CLC'
WHERE track_id = 'TRACK-STD-001';


INSERT IGNORE INTO academic_program (
    program_id,
    faculty_id,
    track_id,
    name
)
VALUES (
    'PROG-TEST-001',
    'FAC-TEST-001',
    'TRACK-STD-001',
    'Software Engineering Test Program'
);


-- Demo SE curriculum. required_credits is sum(max(mandatory, 14)) over
-- semesters 1–9 of GEN+SE from PathToGrad/data/Courses.csv (= 138).
INSERT IGNORE INTO curriculum (
    curriculum_id,
    program_id,
    version,
    required_credits
)
VALUES (
    'CURR-TEST-2024',
    'PROG-TEST-001',
    'TEST-2024',
    138
);


/*
Synthetic academic terms used only for development/testing.
Cadence freeze (C-01): term_type = Semester2 so the demo catalog (GEN 2,
GEN 5, SE 8 in offerings.csv) is actually offered — position_of(S) =
S % 3, and 2/5/8 % 3 = 2, which is Semester2, not Semester1. This is not
a programme-semester number; it's just the yearly slot the term sits in.
*/
INSERT IGNORE INTO academic_term (
    term_id,
    name,
    start_date,
    end_date,
    term_type
)
VALUES
(
    'TERM-2026-1',
    '2026.1',
    '2026-09-01',
    '2027-01-15',
    'Semester2'
),
(
    'TERM-TEST-A',
    'Test Term A',
    '2026-01-01',
    '2026-06-30',
    'Semester1'
),
(
    'TERM-TEST-B',
    'Test Term B',
    '2026-07-01',
    '2026-12-31',
    'Semester2'
);
