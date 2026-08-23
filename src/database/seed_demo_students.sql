USE pathtograd;

/*
============================================================
FIVE DEMO STUDENTS — A-19 / A-20 seed data (T-020 / A-23)
SYNTHETIC DEVELOPMENT / TEST DATA ONLY.

Apply AFTER, in this order:
  1. alembic upgrade head
  2. src/database/seed.sql
  3. python -m app.scripts.import_courses   (loads course/curriculum/offering rows)
  4. this file

This is the "testing seed" the team keeps referring to: real MySQL rows
for A-19 (engine tests against seeded fixtures, not the in-memory fakes
in tests/fakes.py) and A-20 (one student worked out on paper, compared
against what the engine actually returns). Every scenario below is
picked to exercise a specific, named behaviour rather than being random
data — see the per-student comment blocks.

Demo term is TERM-2026-1 (2026.1, term_type=Semester2 per C-01), which
only offers programme semesters 2, 5 and 8 (see DECISIONS.md). All five
students below sit at one of those three semesters so their Assigned
courses are actually reachable this term.

TD-* mapping (A-23 / testing document identifiers):
  TD-COURSE-BASE       CSC10012 (Programming Fundamentals, sem 1, no prereqs)
  TD-COURSE-DEPENDENT  CSC10004 (Data Structures, sem 2, requires CSC10012)
  TD-ATTEMPT-PASSED    DEMO-S02 / DEMO-S08 / DEMO-CAP have CSC10012 Passed
  TD-ATTEMPT-FAILED    DEMO-FAIL has CSC10012 Failed once (still retake-eligible)
  TD-ATTEMPT-INPROGRESS  not seeded here — none of these five has an
                        InProgress attempt on CSC10012 specifically. Add a
                        sixth minimal student if the testing document needs
                        that exact literal fixture; every other InProgress-
                        adjacent path (Missing, Failed, Failed-twice) is
                        covered below on other courses.
  TD-CURRICULUM        CURR-TEST-2024 (from seed.sql, required_credits=138)
  TD-PROFILE-VALID     any of the five below (all have curriculum_id +
                        program_id set, so get_course_catalog / graduation
                        progress resolve normally)
  TD-PROFILE-INCOMPLETE  not created here — a profile with curriculum_id
                        or program_id left NULL is a one-row INSERT if a
                        specific "uncertain" test needs it; not duplicated
                        across all five for no reason.
  TD-TERM-TARGET        TERM-2026-1 (from seed.sql)
  TD-OFFERING-AVAILABLE  CSC13010 (sem 8, has sections in offerings.csv)
  TD-OFFERING-MISSING    CSC13001 (sem 8, mandatory, zero rows in
                        offerings.csv — every student below who reaches
                        semester 8 hits this as DROPPED_NOT_OFFERED /
                        COURSE_NOT_OFFERED)

Every INSERT below is IGNORE with a stable, human-readable id, so
re-running this file (or the whole pipeline from a fresh volume) is
safe — it will not duplicate rows or error on a second run.
============================================================
*/


-- ============================================================
-- Shared: five user accounts, one per demo student.
-- password is a placeholder — see work_checklist.md, auth/hashing is
-- explicitly out of scope for Track A ("password is still a placeholder").
-- ============================================================

INSERT IGNORE INTO users (user_id, full_name, email, password, role, account_status)
VALUES
    ('USER-DEMO-S02', 'Demo Student S02', 'demo.s02@example.com', 'NOT_USED_DAY1', 'Student', 'Active'),
    ('USER-DEMO-S05', 'Demo Student S05', 'demo.s05@example.com', 'NOT_USED_DAY1', 'Student', 'Active'),
    ('USER-DEMO-S08', 'Demo Student S08', 'demo.s08@example.com', 'NOT_USED_DAY1', 'Student', 'Active'),
    ('USER-DEMO-FAIL', 'Demo Student Fail', 'demo.fail@example.com', 'NOT_USED_DAY1', 'Student', 'Active'),
    ('USER-DEMO-CAP', 'Demo Student Cap', 'demo.cap@example.com', 'NOT_USED_DAY1', 'Student', 'Active');


-- ============================================================
-- DEMO-S02 — semester 2, GEN, no specialization yet, clean record.
--
-- Purpose: the "everything is simple" baseline. Semester-1 mandatory
-- (15cr) fully passed, nothing failed, nothing attempted beyond that.
--
-- Expect from get_course_catalog(current=2):
--   CSC10004, MTH00058          -> Assigned, not blocked (CSC10012 passed)
--   PHY00005, BAA00004          -> Elective, offered
--   everything semester >= 3    -> Future
-- Expect from generate_semester_plan: Assigned mandatory alone is only
-- 8 credits (below the 14-credit / 4-course floor -- see A-02's soft-lock
-- table), so the generator MUST pull PHY00005 and/or BAA00004 as
-- ELECTIVE_FILL to reach the minimum. If it stops at 8 credits and just
-- warns, that's the bug A-16's spec explicitly calls out.
-- Expect from get_graduation_progress: earned=15, required=138,
-- gpa=8.07, mandatory_passed=False, credit_requirement_met=False.
-- ============================================================

INSERT IGNORE INTO student_profile
    (student_id, user_id, intake_year, current_semester, target_credit_load, program_id, spec_code, curriculum_id)
VALUES
    ('DEMO-S02', 'USER-DEMO-S02', 2025, 2, 16, 'PROG-TEST-001', NULL, 'CURR-TEST-2024');

INSERT IGNORE INTO academic_record (record_id, student_id, updated_at)
VALUES ('RECORD-DEMO-S02', 'DEMO-S02', NOW());

INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT
    CONCAT('ATT-DEMO-S02-', c.course_code, '-1'),
    'RECORD-DEMO-S02',
    c.course_id,
    'TERM-TEST-A',
    1,
    g.grade,
    'Passed',
    c.credits
FROM course c
JOIN (
    SELECT 'CSC00004' AS course_code, 8.0 AS grade
    UNION ALL SELECT 'CSC10012', 8.0
    UNION ALL SELECT 'MTH00009', 7.5
    UNION ALL SELECT 'CSC10121', 9.0
) g ON g.course_code = c.course_code;


-- ============================================================
-- DEMO-S05 — semester 5, GEN, no specialization yet, one real backlog.
--
-- Purpose: a normal mid-path student who is genuinely behind on one
-- course. Demonstrates Backlog, Backlog+blocked, Backlog+stale, and
-- Assigned+blocked all at once, with no failures anywhere (so it's
-- clearly distinguishable from DEMO-FAIL's scenario).
--
-- CSC10009 (semester 3, "Computer Systems", 2cr) was never attempted.
-- That alone:
--   - CSC10009 itself         -> Backlog, and STALE (current 5 - assigned
--                                3 = 2, meets BACKLOG_STALE_SEMESTERS)
--   - CSC10008 (semester 4)   -> Backlog + blocked (requires CSC10009)
--   - CSC10007 (semester 5)   -> Assigned + blocked (requires CSC10009)
-- Everything else through semester 4 is passed cleanly, so CSC10006 and
-- MTH00007 (the other two semester-5 Assigned courses) come back clean.
--
-- Expect from generate_semester_plan: CSC10007 dropped with
-- DROPPED_PREREQ_BLOCKED; CSC10006 and MTH00007 placed with
-- ASSIGNED_THIS_SEMESTER; CSC10009 and CSC10008 excluded the same way
-- (both mandatory Backlog, both blocked). detect_risks should report
-- PREREQ_BLOCKED and BACKLOG_STALE.
-- Expect from get_graduation_progress: earned=43, required=138,
-- gpa=7.14, mandatory_passed=False, credit_requirement_met=False.
-- ============================================================

INSERT IGNORE INTO student_profile
    (student_id, user_id, intake_year, current_semester, target_credit_load, program_id, spec_code, curriculum_id)
VALUES
    ('DEMO-S05', 'USER-DEMO-S05', 2024, 5, 16, 'PROG-TEST-001', NULL, 'CURR-TEST-2024');

INSERT IGNORE INTO academic_record (record_id, student_id, updated_at)
VALUES ('RECORD-DEMO-S05', 'DEMO-S05', NOW());

INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT
    CONCAT('ATT-DEMO-S05-', c.course_code, '-1'),
    'RECORD-DEMO-S05',
    c.course_id,
    'TERM-TEST-A',
    1,
    g.grade,
    'Passed',
    c.credits
FROM course c
JOIN (
    -- semester 1 (all 4)
    SELECT 'CSC00004' AS course_code, 8.0 AS grade
    UNION ALL SELECT 'CSC10012', 7.5
    UNION ALL SELECT 'MTH00009', 7.0
    UNION ALL SELECT 'CSC10121', 9.0
    -- semester 2 (both mandatory)
    UNION ALL SELECT 'CSC10004', 7.0
    UNION ALL SELECT 'MTH00058', 6.5
    -- semester 3: CSC10009 deliberately NOT attempted, see header comment
    UNION ALL SELECT 'CSC10003', 6.0
    UNION ALL SELECT 'MTH00005', 7.5
    UNION ALL SELECT 'MTH00008', 7.0
    -- semester 4: CSC10008 deliberately NOT attempted (blocked by CSC10009 anyway)
    UNION ALL SELECT 'CSC10014', 7.0
    UNION ALL SELECT 'MTH00006', 6.5
) g ON g.course_code = c.course_code;


-- ============================================================
-- DEMO-FAIL — semester 5, one clean single fail + one graduation-
-- blocking double fail.
--
-- Purpose: dedicated failure/retake scenarios, kept on separate courses
-- so each is independently readable.
--
--   CSC10012 (TD-COURSE-BASE) -> Failed once, grade 4.0. This is
--     TD-ATTEMPT-FAILED. attempt_number=1 < 2, so the *attempt count*
--     alone doesn't rule out a retake -- but CSC10012 is a semester-1
--     course, and this demo term only offers semesters 2/5/8 (C-01).
--     So rank_retakes should return eligible=False here anyway, with
--     offered_this_term=False, NOT because of the attempt count. Worth
--     checking by hand: if it comes back eligible=True, the cadence
--     check inside rank_retakes isn't being applied. It also blocks
--     CSC10004, CSC10003, CSC10014 (everything downstream of CSC10012)
--     -- all show Backlog+blocked.
--   CSC10009 -> Failed TWICE (grades 3.5, then 3.0). attempt_number=2,
--     Failed -> NO_RETAKE_REMAINING (critical severity). Since CSC10009
--     can never be passed again, CSC10008 and CSC10007 (both require it)
--     are PERMANENTLY blocked -- this student cannot mathematically pass
--     the mandatory set through this path. Good demonstration of why
--     NO_RETAKE_REMAINING is graduation-blocking, not just a warning.
--   MTH00007 (semester 5, needs only MTH00005, which is passed) is left
--     clean and unblocked, so this student still has one normal,
--     placeable Assigned course -- the plan isn't *entirely* excluded.
--
-- Expect from get_graduation_progress: earned=27, required=138,
-- mandatory_passed will be False forever unless the team's rules
-- change, since CSC10009 has no attempts left. Only the LATEST attempt
-- per course counts toward GPA (progress.py uses latest_per_course), so
-- CSC10009's first fail (3.5) is superseded by its second (3.0) -- don't
-- double-count both. Passed courses were deliberately kept just above
-- the pass line (5.0-5.5) so that folding in the two failed grades
-- (4.0, 3.0) actually pulls the weighted average under the 5.0
-- GPA_BELOW_THRESHOLD line: expect gpa=4.82. If it comes back higher,
-- either an old attempt is being counted instead of the latest, or a
-- Failed attempt's grade isn't being weighted in at all.
-- ============================================================

INSERT IGNORE INTO student_profile
    (student_id, user_id, intake_year, current_semester, target_credit_load, program_id, spec_code, curriculum_id)
VALUES
    ('DEMO-FAIL', 'USER-DEMO-FAIL', 2024, 5, 16, 'PROG-TEST-001', NULL, 'CURR-TEST-2024');

INSERT IGNORE INTO academic_record (record_id, student_id, updated_at)
VALUES ('RECORD-DEMO-FAIL', 'DEMO-FAIL', NOW());

-- Passed courses (attempt_number 1)
INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT
    CONCAT('ATT-DEMO-FAIL-', c.course_code, '-1'),
    'RECORD-DEMO-FAIL',
    c.course_id,
    'TERM-TEST-A',
    1,
    g.grade,
    'Passed',
    c.credits
FROM course c
JOIN (
    -- barely-passing on purpose: with the two failed attempts below
    -- folded in, this is what actually pushes GPA under the 5.0
    -- warning threshold -- see the note above the graduation-progress
    -- expectation at the end of this block.
    SELECT 'CSC00004' AS course_code, 5.0 AS grade
    UNION ALL SELECT 'CSC10121', 5.0
    UNION ALL SELECT 'MTH00009', 5.0
    UNION ALL SELECT 'MTH00058', 5.0
    UNION ALL SELECT 'MTH00005', 5.0
    UNION ALL SELECT 'MTH00008', 5.5
    UNION ALL SELECT 'MTH00006', 5.0
) g ON g.course_code = c.course_code;

-- CSC10012: failed once, still retake-eligible (TD-ATTEMPT-FAILED)
INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT 'ATT-DEMO-FAIL-CSC10012-1', 'RECORD-DEMO-FAIL', c.course_id, 'TERM-TEST-A', 1, 4.0, 'Failed', 0
FROM course c WHERE c.course_code = 'CSC10012';

-- CSC10009: failed twice -> NO_RETAKE_REMAINING
INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT 'ATT-DEMO-FAIL-CSC10009-1', 'RECORD-DEMO-FAIL', c.course_id, 'TERM-TEST-A', 1, 3.5, 'Failed', 0
FROM course c WHERE c.course_code = 'CSC10009';

INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT 'ATT-DEMO-FAIL-CSC10009-2', 'RECORD-DEMO-FAIL', c.course_id, 'TERM-TEST-B', 2, 3.0, 'Failed', 0
FROM course c WHERE c.course_code = 'CSC10009';


-- ============================================================
-- DEMO-CAP — semester 8, SE, over the combined credit/course cap.
--
-- Purpose: the "over-cap" scenario. Real per-semester mandatory sums in
-- this curriculum never exceed 23 credits on their own (semester 9,
-- which isn't even offered this term), so Assigned alone can never
-- trigger A-16's "Assigned-over-cap" special case with this data. The
-- achievable, realistic version is Assigned + Backlog together crossing
-- the CLC track's 24-credit / 6-course cap -- this student is built to
-- do exactly that.
--
-- Passed cleanly through semester 4, plus CSC13002 (semester 7, needed
-- to unblock semester-8 SE courses). Deliberately left UNPASSED (but
-- NOT blocked -- their own prerequisites are satisfied) four semester-5
-- mandatory courses: CSC10006, CSC10007, MTH00007, and semester-2's
-- MTH00058. All four are offered this term (semesters 2 and 5 are both
-- in the Semester2 cadence) and all four are placeable, which is what
-- makes this a genuine cap collision rather than another blocked-course
-- scenario.
--
-- Expect from generate_semester_plan (track limits 14/24/4/6):
--   Assigned:  CSC13005, CSC13009, CSC13010 placed (12cr, 3 courses).
--              CSC13001 excluded DROPPED_NOT_OFFERED (TD-OFFERING-MISSING).
--   Backlog (sorted oldest-semester-first, then course code):
--     MTH00058 (sem 2)  -> placed, 16cr / 4 courses
--     CSC10006 (sem 5)  -> placed, 20cr / 5 courses
--     CSC10007 (sem 5)  -> placed, 24cr / 6 courses  (both caps now hit)
--     MTH00007 (sem 5)  -> DEFERRED_CREDIT_CAP (both max_credits and
--                          max_courses are exactly full)
-- No electives get a turn; the loop stops at the cap before reaching
-- them. detect_risks should NOT report ASSIGNED_OVER_CAP (Assigned
-- alone is 12cr, well under 24) -- if it does, something upstream of
-- the cap changed.
-- Expect from get_graduation_progress: earned=49, required=138,
-- gpa=7.29, mandatory_passed=False, credit_requirement_met=False.
-- ============================================================

INSERT IGNORE INTO student_profile
    (student_id, user_id, intake_year, current_semester, target_credit_load, program_id, spec_code, curriculum_id)
VALUES
    ('DEMO-CAP', 'USER-DEMO-CAP', 2022, 8, 20, 'PROG-TEST-001', 'SE', 'CURR-TEST-2024');

INSERT IGNORE INTO academic_record (record_id, student_id, updated_at)
VALUES ('RECORD-DEMO-CAP', 'DEMO-CAP', NOW());

INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT
    CONCAT('ATT-DEMO-CAP-', c.course_code, '-1'),
    'RECORD-DEMO-CAP',
    c.course_id,
    'TERM-TEST-A',
    1,
    g.grade,
    'Passed',
    c.credits
FROM course c
JOIN (
    -- semester 1 (all 4)
    SELECT 'CSC00004' AS course_code, 8.0 AS grade
    UNION ALL SELECT 'CSC10012', 8.0
    UNION ALL SELECT 'MTH00009', 7.5
    UNION ALL SELECT 'CSC10121', 9.0
    -- semester 2: CSC10004 passed, MTH00058 deliberately left unpassed
    UNION ALL SELECT 'CSC10004', 7.0
    -- semester 3 (all 4)
    UNION ALL SELECT 'CSC10003', 6.5
    UNION ALL SELECT 'CSC10009', 7.0
    UNION ALL SELECT 'MTH00005', 7.0
    UNION ALL SELECT 'MTH00008', 6.5
    -- semester 4 (all 3 mandatory)
    UNION ALL SELECT 'CSC10014', 7.0
    UNION ALL SELECT 'CSC10008', 7.5
    UNION ALL SELECT 'MTH00006', 7.0
    -- semester 7: only CSC13002, to unblock semester 8
    UNION ALL SELECT 'CSC13002', 7.0
) g ON g.course_code = c.course_code;


-- ============================================================
-- DEMO-S08 — semester 8, SE, strong/on-track senior.
--
-- Purpose: the near-graduation persona. Everything through semester 7
-- mandatory AND elective is passed, so this student is genuinely close
-- to done and exercises the parts of the engine the other four don't:
-- SPECIALIZATION_NOT_SET correctly NOT firing (spec_code is set),
-- retake-for-improvement, and the soft-lock top-up still applying even
-- this late (semester-8 mandatory minus the unoffered CSC13001 is only
-- 12cr, still under the 14-credit floor).
--
-- Every semester-2 and semester-5 course this student passed is offered
-- this term with attempt_number=1, so rank_retakes will return several
-- eligible=True rows, not just one -- that's realistic (any passed,
-- offered course is retake-eligible; ranking, not filtering, is A-17's
-- job). CSC10006 was deliberately given the lowest grade of the group
-- (5.0, vs. 6.5-8.0 for the rest), so A-17's sort (Failed first, then
-- lowest grade, then course code) should put it at the top of the
-- retake list, and it's the one most likely to actually get placed once
-- Assigned + BAA00102 (the one remaining unpassed, offered elective)
-- leaves room under this student's target_credit_load.
--
-- Expect from generate_semester_plan: CSC13005, CSC13009, CSC13010
-- placed (ASSIGNED_THIS_SEMESTER); CSC13001 excluded DROPPED_NOT_OFFERED;
-- BAA00102 placed (ELECTIVE_FILL); CSC10006 placed (RETAKE_IMPROVEMENT),
-- which should also produce a RETAKE_REPLACES_GRADE risk.
-- Expect from get_graduation_progress: mandatory_passed=False (semester
-- 8 and 9 mandatory still outstanding), credit_requirement_met=False
-- (107 earned vs. 138 required, gpa=7.26), completed=False -- this is a
-- "close but not done" student on purpose, not a finished one.
-- ============================================================

INSERT IGNORE INTO student_profile
    (student_id, user_id, intake_year, current_semester, target_credit_load, program_id, spec_code, curriculum_id)
VALUES
    ('DEMO-S08', 'USER-DEMO-S08', 2022, 8, 18, 'PROG-TEST-001', 'SE', 'CURR-TEST-2024');

INSERT IGNORE INTO academic_record (record_id, student_id, updated_at)
VALUES ('RECORD-DEMO-S08', 'DEMO-S08', NOW());

INSERT IGNORE INTO course_attempt
    (attempt_id, record_id, course_id, term_id, attempt_number, grade, result_status, credits_earned)
SELECT
    CONCAT('ATT-DEMO-S08-', c.course_code, '-1'),
    'RECORD-DEMO-S08',
    c.course_id,
    'TERM-TEST-A',
    1,
    g.grade,
    'Passed',
    c.credits
FROM course c
JOIN (
    -- semester 1 (all 4)
    SELECT 'CSC00004' AS course_code, 8.0 AS grade
    UNION ALL SELECT 'CSC10012', 8.5
    UNION ALL SELECT 'MTH00009', 7.5
    UNION ALL SELECT 'CSC10121', 9.0
    -- semester 2 (all 4, mandatory + elective)
    UNION ALL SELECT 'CSC10004', 7.5
    UNION ALL SELECT 'MTH00058', 7.0
    UNION ALL SELECT 'PHY00005', 6.5
    UNION ALL SELECT 'BAA00004', 8.0
    -- semester 3 (all 4)
    UNION ALL SELECT 'CSC10003', 7.5
    UNION ALL SELECT 'CSC10009', 7.0
    UNION ALL SELECT 'MTH00005', 7.0
    UNION ALL SELECT 'MTH00008', 6.5
    -- semester 4 (all 6)
    UNION ALL SELECT 'CSC10014', 7.5
    UNION ALL SELECT 'CSC10008', 7.0
    UNION ALL SELECT 'MTH00006', 7.0
    UNION ALL SELECT 'BAA00005', 8.0
    UNION ALL SELECT 'BAA00021', 8.0
    UNION ALL SELECT 'BAA00030', 7.0
    -- semester 5 (all 4) -- CSC10006 deliberately low, see header comment
    UNION ALL SELECT 'CSC10006', 5.0
    UNION ALL SELECT 'CSC10007', 7.0
    UNION ALL SELECT 'MTH00007', 7.0
    UNION ALL SELECT 'BAA00022', 8.0
    -- semester 6 (all 4)
    UNION ALL SELECT 'PHY00007', 7.0
    UNION ALL SELECT 'CSC14003', 7.0
    UNION ALL SELECT 'MTH00057', 6.5
    UNION ALL SELECT 'BAA00003', 8.0
    -- semester 7 (all 4: 3 mandatory + BAA00101)
    UNION ALL SELECT 'CSC13002', 7.5
    UNION ALL SELECT 'CSC13008', 7.0
    UNION ALL SELECT 'CSC13102', 7.5
    UNION ALL SELECT 'BAA00101', 8.0
) g ON g.course_code = c.course_code;
