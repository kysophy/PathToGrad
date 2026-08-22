USE pathtograd;

-- ============================================================
-- ACADEMIC PLANNING SUPPORT TABLES
-- Curriculum requirements, prerequisites and course offering
-- ============================================================


-- ============================================================
-- CURRICULUM COURSE
-- Maps courses to a curriculum.
-- ============================================================

CREATE TABLE IF NOT EXISTS curriculum_course (
    curr_course_id VARCHAR(36) PRIMARY KEY,
    curriculum_id VARCHAR(36) NOT NULL,
    course_id VARCHAR(36) NOT NULL,
    requirement_type ENUM('Core', 'Elective') NOT NULL,

    CONSTRAINT fk_curriculum_course_curriculum
        FOREIGN KEY (curriculum_id)
        REFERENCES curriculum(curriculum_id),

    CONSTRAINT fk_curriculum_course_course
        FOREIGN KEY (course_id)
        REFERENCES course(course_id),

    CONSTRAINT uq_curriculum_course
        UNIQUE (curriculum_id, course_id)
);


-- ============================================================
-- PREREQUISITE
-- Represents Course A requiring Course B.
-- ============================================================

CREATE TABLE IF NOT EXISTS prerequisite (
    prereq_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(36) NOT NULL,
    required_course_id VARCHAR(36) NOT NULL,

    CONSTRAINT fk_prerequisite_course
        FOREIGN KEY (course_id)
        REFERENCES course(course_id),

    CONSTRAINT fk_prerequisite_required_course
        FOREIGN KEY (required_course_id)
        REFERENCES course(course_id),

    CONSTRAINT uq_prerequisite_rule
        UNIQUE (course_id, required_course_id),

    CONSTRAINT chk_prerequisite_not_self
        CHECK (course_id <> required_course_id)
);


-- ============================================================
-- COURSE OFFERING
-- Makes one course available in one academic term.
-- ============================================================

CREATE TABLE IF NOT EXISTS course_offering (
    offering_id VARCHAR(36) PRIMARY KEY,
    course_id VARCHAR(36) NOT NULL,
    term_id VARCHAR(36) NOT NULL,

    status ENUM(
        'Active',
        'Inactive',
        'Archived'
    ) NOT NULL DEFAULT 'Active',

    CONSTRAINT fk_offering_course
        FOREIGN KEY (course_id)
        REFERENCES course(course_id),

    CONSTRAINT fk_offering_term
        FOREIGN KEY (term_id)
        REFERENCES academic_term(term_id),

    CONSTRAINT uq_course_offering
        UNIQUE (course_id, term_id)
);


-- ============================================================
-- CLASS SECTION
-- A selectable class group belonging to one offering.
-- ============================================================

CREATE TABLE IF NOT EXISTS class_section (
    section_id VARCHAR(36) PRIMARY KEY,
    offering_id VARCHAR(36) NOT NULL,

    section_code VARCHAR(20) NOT NULL,

    capacity INT NOT NULL,

    status ENUM(
        'Active',
        'Inactive',
        'Archived'
    ) NOT NULL DEFAULT 'Active',

    CONSTRAINT chk_section_capacity
        CHECK (capacity >= 0),

    CONSTRAINT fk_section_offering
        FOREIGN KEY (offering_id)
        REFERENCES course_offering(offering_id),

    CONSTRAINT uq_section_code_per_offering
        UNIQUE (offering_id, section_code)
);


-- ============================================================
-- SECTION MEETING
-- Stores the real weekly meeting blocks of a class section.
-- ============================================================

CREATE TABLE IF NOT EXISTS section_meeting (
    meeting_id VARCHAR(36) PRIMARY KEY,

    section_id VARCHAR(36) NOT NULL,

    day_of_week ENUM(
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ) NOT NULL,

    start_time TIME NOT NULL,
    end_time TIME NOT NULL,

    CONSTRAINT chk_meeting_time
        CHECK (end_time > start_time),

    CONSTRAINT fk_meeting_section
        FOREIGN KEY (section_id)
        REFERENCES class_section(section_id)
);