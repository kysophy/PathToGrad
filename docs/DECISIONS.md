# PathToGrad: Decisions log

Running log of deviations from the Design document and of data-modelling choices that later tasks depend on. Add a line in the same change as the decision.

---

## 2026-08-22: Part 1 rewrite (W1 / W2)

Supersedes the 2026-08-16 entries where they conflict.

### `spec_code` is not `PROGRAM_TRACK`

The CSV column is `spec_code` (GEN, SE, CN, …). `PROGRAM_TRACK` in the schema remains CLC versus standard and holds the 14–24 credit policy. Never use the word "track" for both.

### General block is stored once

Semesters 1–6 are `spec_code=GEN`, 26 rows, shared by everyone. Semesters 7–9 carry a real specialization code. A student's curriculum is GEN rows plus their own specialization. Store the text `GEN` (not SQL NULL). A student with no specialization sees only `GEN` rows.

### Mandatory = `CSC*` or `MTH*`

`is_mandatory` is TRUE iff `course_code` starts with `CSC` or `MTH`. Everything else (`BAA`, `PHY`) is elective. Soft Skills and Entrepreneurship are mandatory because they are `CSC*`. **No floor-fill.** Semesters that fall below 14 mandatory credits are the intended soft-lock.

### `required_credits` is not the mandatory sum

Q31's "sum the seeded mandatory courses" is withdrawn. Compute

`required_credits = sum over semesters 1–9 of max(mandatory_credits, 14)`

For GEN+SE that is **138** against a mandatory sum of **120**. Graduation is two independent conditions: all mandatory `CSC`/`MTH` courses passed, **and** earned credits ≥ this figure.

### Cadence freeze (C-01): `2026.1` is `term_type = Semester2`

A calendar term has no programme-semester number (see A-09b). What it has is a position in the academic year, stored as `AcademicTerm.term_type`. `offerings.csv` was generated for programme semesters 2, 5 and 8; since `2 % 3 == 5 % 3 == 8 % 3 == 2`, that position is `Semester2`, and `seed.sql` sets `TERM-2026-1` accordingly. Demo personas therefore sit at semesters 2, 5 and 8, not 1/4/7. This resolves the cadence mismatch that previously had `seed.sql` saying `Semester1` while the offerings file was built for 2/5/8; do not reintroduce that split by editing one side without the other.

### Meeting times are clock intervals, half-open

`LT` is `07:30–11:10` or `13:30–17:10`. `TH` is one of `07:30–09:30`, `09:30–11:30`, `13:30–15:30`, `15:30–17:30`. Two sections clash when they share a day and `a.start < b.end AND b.start < a.end`. Touching endpoints do **not** clash. The old "periods 1–10 inclusive" convention is withdrawn.

### Importer defaults to Track A CSVs

`python -m app.scripts.import_courses` (no args) reads `PathToGrad/data/Courses.csv` and `offerings.csv`. It fills `course`, GEN+SE `curriculum_course` on `CURR-TEST-2024`, `prerequisite`, and the `2026.1` offering/section/meeting rows. The raw commented dump lives in `Materials and Notes/Courses.raw.csv` (never edited). `seed.sql` sets `required_credits = 138`. Do not apply `fixtures/academic_planning_test_data.sql` on a demo database: it used to overwrite that number and inject contradicting prerequisite edges.

### Prerequisite set is derived, not official

Official FIT tiên quyết / học trước / song hành lists were not available. Edges for the GEN+SE 1–9 path were derived from course names, semester order, and the unambiguous chains in `TaskToDo.md` §14.2. Illustrative curriculum structure, not the department's rules.

### All prerequisite edges use passed-only semantics

Semicolon-separated AND-list. No `rule_type`, no OR groups, no credit-threshold gates. `học trước` vs `tiên quyết` is not encoded; every edge is must-have-passed.

### Curriculum is truncated at semester 9

Thesis / graduation internship / graduation project internship are dropped. Do not hardcode the official programme total.

### Duplicate `(spec, course)` rows

`CSC14118` appears in both semester 8 and semester 9 of Computer Science and of Information Technology. Keep the unique key on `(curriculum_id, course_id)`, take the **earliest** semester as `assigned_semester`, and log the dedupe. (Q32)

---

## 2026-08-22: Part 2 schema (A-05 to A-08)

### Alembic is canonical

`src/database/schema.sql` and `src/database/migrations/002_add_academic_planning_tables.sql` are deleted. The schema is created only by `alembic upgrade head` from `src/backend`. `001_initial_schema` builds the 21 tables; `002_proofreading_fixes` applies the proofreading decisions below.

### No `PREREQUISITE.rule_type`

All edges remain passed-only AND-lists. Adding `rule_type` is still rejected.

### `curriculum_applicability` dropped

`STUDENT_PROFILE.curriculum_id` is the mapping. Intake year stays on the profile and on `CLASS_GROUP`.

### `PLAN_REVIEW` is append-only

`PlanReviewRepository` exposes `insert` and `list_for_plan` only. Rows are never updated or deleted (NFR-10).

### `selection_reason` stores A-09 codes

`STUDY_PLAN_ITEM.selection_reason` uses `ASSIGNED_THIS_SEMESTER`, `BACKLOG_FROM_SEMESTER_N`, `ELECTIVE_FILL`, `RETAKE_AFTER_FAIL`, `RETAKE_IMPROVEMENT`, not the short labels Assigned/Backlog/Elective/Retake.

### Course names are split

`COURSE.course_name` is replaced by `name_vi` and `name_en`.

### Credit policy lives on `PROGRAM_TRACK`

`min_credits_per_term=14`, `max_credits_per_term=24`, `min_courses=4`, `max_courses=6` are seeded on the CLC track (`TRACK-STD-001`, name `CLC`). They are not hardcoded in the engine.

---

## 2026-08-22: Proofreading decisions (applied)

Supersedes the earlier Part 2 bullets on GEN-as-NULL and `term_no` where they conflict.

### Store CSV `GEN` as the text `GEN`

`curriculum_course.spec_code` keeps the string. Lookup is `spec_code = 'GEN' OR spec_code = student.spec_code`. `student_profile.spec_code` stays nullable (no specialization picked yet). Migration `002` also rewrites any already-imported NULL rows to `'GEN'`.

### No `term_no` on `ACADEMIC_TERM`

The extra column is dropped. No programme-semester number is stored on the term row at all: `2026.1` carries only `term_type = Semester2` (see the cadence freeze above). Cadence (A-09b) must not parse `"2026.1"` and must not read a `term_no` column.

### `users.email` is UNIQUE

Constraint `uq_users_email`. One account per email.

### Seeded track is CLC

`TRACK-STD-001` keeps that id so existing FKs still work. `name` is `CLC`. Limits stay 14 / 24 / 4 / 6.

### Repositories flush; services commit

`AttemptRepository.add_attempt` flushes. `AcademicRecordService.add_attempt` commits.

### Graduation JSON is `GraduationProgress`

The live API `/graduation-progress` returns the tool type (`mandatory_passed`, `credit_requirement_met`, `gpa`, …). A-13 now fills `gpa` from the latest graded attempt per course (not the best grade). The old `GraduationProgressResponse` shape is gone.

### Demo curriculum stays GEN+SE on `CURR-TEST-2024`

Do not dump CN + SE + CS into the same `curriculum_id`; shared course codes would collide.

### Offering status follows the data spec

`Canceled`, not the old `Inactive`.

### IDs stay strings

Checklist tool sketches that used `int` were wrong.

---

## 2026-08-23: Part 3 engine (A-09 to A-18)

### Cadence lives in one helper

`position_of(semester_no)` / `is_offered_in` in `app/deterministic/cadence.py` is the only yearly-slot formula. Catalog, importer, retakes, and the plan generator all call it. Do not add a second `(current_semester - assigned_semester) % 3` check.

### GPA and risk thresholds (spec was silent)

The 10-point scale is already how grades are stored (`DECIMAL(3,1)`). Conventions used by A-13 / A-18:

- GPA is the credit-weighted average of the **latest** attempt per course that has a numeric grade (Failed grades count, so a worse retake lowers GPA).
- `GPA_BELOW_THRESHOLD` fires when GPA < **5.0**.
- `FAILED_UNRETAKEN_LATE` fires when `current_semester >= 7` and a Failed course still has a retake left.
- `BACKLOG_STALE` fires when a mandatory course is still unpassed and `current_semester - assigned_semester >= 2`.

Change `app/deterministic/constants.py` and this log together if the team picks different numbers.

### Plan uniqueness is the generator’s job

The database unique on `study_plan_item` is `(plan_id, section_id)`. A-16 refuses two sections of the same course in one plan.

### Completed mandatory courses have no enum

`CoursePrimaryStatus` has no Completed value. A passed mandatory course that cannot be retaken this term is labelled **Future** so it does not appear in Recommended (Assigned + Backlog).

