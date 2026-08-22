USE pathtograd;

-- ============================================================
-- OPTIONAL isolated test fixtures — DO NOT apply on a demo DB.
--
-- After Track A data is loaded via:
--   python -m app.scripts.import_courses
-- this file would overwrite required_credits (138 → 6) and insert
-- prerequisite edges that contradict data/Courses.csv
-- (CSC10004 requires CSC10012, not CSC00004).
--
-- Keep it for standalone TC-13–TC-20 database tests only.
-- Conflicting statements below are commented out so a mistaken
-- source of this file cannot poison the demo curriculum.
-- ============================================================


-- ------------------------------------------------------------
-- Compact graduation requirement used by TC-13 to TC-15.
-- Disabled: demo seed uses required_credits = 138 from Courses.csv.
-- ------------------------------------------------------------
-- UPDATE curriculum
-- SET required_credits = 6
-- WHERE curriculum_id = 'CURR-TEST-2024';


-- ------------------------------------------------------------
-- Required/Core courses used for graduation tests.
-- Disabled: GEN+SE Core/Elective rows come from import_courses.py.
-- ------------------------------------------------------------
-- INSERT IGNORE INTO curriculum_course ... CSC00004 / CSC10009


-- ------------------------------------------------------------
-- Prerequisite fixture (synthetic, contradicts the demo graph).
-- Disabled.
-- CSC10004 requires CSC00004  — demo: CSC10004 requires CSC10012
-- CSC10003 requires MTH00058 — demo: CSC10003 requires CSC10004
-- ------------------------------------------------------------
-- INSERT IGNORE INTO prerequisite ...


-- ------------------------------------------------------------
-- Extra offering of CSC10004 in TERM-TEST-B (TC-20 Dataset A on
-- the test term). Harmless alongside the 2026.1 demo offerings.
-- ------------------------------------------------------------

INSERT IGNORE INTO course_offering (
    offering_id,
    course_id,
    term_id,
    status
)
SELECT
    'OFFER-TEST-001',
    course_id,
    'TERM-TEST-B',
    'Active'
FROM course
WHERE course_code = 'CSC10004';


-- ------------------------------------------------------------
-- One active class section.
-- ------------------------------------------------------------

INSERT IGNORE INTO class_section (
    section_id,
    offering_id,
    section_code,
    capacity,
    status
)
SELECT
    'SECTION-TEST-001',
    offering_id,
    'G1',
    40,
    'Active'
FROM course_offering
WHERE offering_id = 'OFFER-TEST-001';


-- ------------------------------------------------------------
-- Meeting schedule for the active class section.
-- ------------------------------------------------------------

INSERT IGNORE INTO section_meeting (
    meeting_id,
    section_id,
    day_of_week,
    start_time,
    end_time
)
SELECT
    'MEETING-TEST-001',
    section_id,
    'Monday',
    '09:00:00',
    '10:30:00'
FROM class_section
WHERE section_id = 'SECTION-TEST-001';


INSERT IGNORE INTO section_meeting (
    meeting_id,
    section_id,
    day_of_week,
    start_time,
    end_time
)
SELECT
    'MEETING-TEST-002',
    section_id,
    'Wednesday',
    '09:00:00',
    '10:30:00'
FROM class_section
WHERE section_id = 'SECTION-TEST-001';