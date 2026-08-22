USE pathtograd;


/*
============================================================
SYNTHETIC DEVELOPMENT / TEST DATA ONLY
These values are NOT claimed to be official university data.
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
    name
)
VALUES (
    'TRACK-STD-001',
    'Standard'
);


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
    120
);


/*
Only intake 2024 is mapped.
Use another intake such as 2023 to exercise TC-04.
*/
INSERT IGNORE INTO curriculum_applicability (
    curriculum_id,
    intake_year
)
VALUES (
    'CURR-TEST-2024',
    2024
);


/*
Synthetic academic terms used only for development/testing.
They are not official university semester dates.
*/
INSERT IGNORE INTO academic_term (
    term_id,
    name,
    start_date,
    end_date
)
VALUES
(
    'TERM-TEST-A',
    'Test Term A',
    '2026-01-01',
    '2026-06-30'
),
(
    'TERM-TEST-B',
    'Test Term B',
    '2026-07-01',
    '2026-12-31'
);
