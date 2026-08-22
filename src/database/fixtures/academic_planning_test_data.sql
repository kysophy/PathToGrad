USE pathtograd;

-- ============================================================
-- SYNTHETIC ACADEMIC PLANNING TEST DATA
--
-- This file exists only for reproducible software tests.
-- Prerequisite and offering relationships below are NOT
-- claimed to be official university data.
-- ============================================================


-- ------------------------------------------------------------
-- Compact graduation requirement used by TC-13 to TC-15.
--
-- The value 6 is synthetic. It is NOT an official HCMUS
-- graduation-credit requirement.
-- ------------------------------------------------------------

UPDATE curriculum
SET required_credits = 6
WHERE curriculum_id = 'CURR-TEST-2024';


-- ------------------------------------------------------------
-- Required/Core courses used for graduation tests.
--
-- CSC00004 = 4 credits from Courses.csv
-- CSC10009 = 2 credits from Courses.csv
-- Total = 6 synthetic required credits
-- ------------------------------------------------------------

INSERT IGNORE INTO curriculum_course (
    curr_course_id,
    curriculum_id,
    course_id,
    requirement_type
)
SELECT
    'CURRCOURSE-TEST-BASE',
    'CURR-TEST-2024',
    course_id,
    'Core'
FROM course
WHERE course_code = 'CSC00004';


INSERT IGNORE INTO curriculum_course (
    curr_course_id,
    curriculum_id,
    course_id,
    requirement_type
)
SELECT
    'CURRCOURSE-TEST-SYSTEM',
    'CURR-TEST-2024',
    course_id,
    'Core'
FROM course
WHERE course_code = 'CSC10009';


-- ------------------------------------------------------------
-- Prerequisite fixture:
--
-- CSC10004 requires CSC00004.
--
-- This relationship is synthetic and exists only for
-- TC-17, TC-18 and TC-20.
-- ------------------------------------------------------------

INSERT IGNORE INTO prerequisite (
    course_id,
    required_course_id
)
SELECT
    target.course_id,
    required.course_id
FROM course AS target
CROSS JOIN course AS required
WHERE target.course_code = 'CSC10004'
  AND required.course_code = 'CSC00004';


-- ------------------------------------------------------------
-- Uncertain-data fixture:
--
-- CSC10003 requires MTH00058.
--
-- Used only for TC-19.
-- ------------------------------------------------------------

INSERT IGNORE INTO prerequisite (
    course_id,
    required_course_id
)
SELECT
    target.course_id,
    required.course_id
FROM course AS target
CROSS JOIN course AS required
WHERE target.course_code = 'CSC10003'
  AND required.course_code = 'MTH00058';


-- ------------------------------------------------------------
-- Course offering fixture for TC-20.
-- CSC10004 is offered in TERM-TEST-B.
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