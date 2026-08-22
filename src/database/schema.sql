CREATE DATABASE IF NOT EXISTS pathtograd
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE pathtograd;


-- ============================================================
-- USER
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Student', 'Advisor', 'Admin') NOT NULL,
    account_status ENUM('Active', 'Suspended') NOT NULL
);


-- ============================================================
-- ACADEMIC STRUCTURE
-- ============================================================

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS program_track (
    track_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS academic_program (
    program_id VARCHAR(36) PRIMARY KEY,
    faculty_id VARCHAR(36) NOT NULL,
    track_id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,

    CONSTRAINT fk_program_faculty
        FOREIGN KEY (faculty_id)
        REFERENCES faculty(faculty_id),

    CONSTRAINT fk_program_track
        FOREIGN KEY (track_id)
        REFERENCES program_track(track_id)
);

CREATE TABLE IF NOT EXISTS curriculum (
    curriculum_id VARCHAR(36) PRIMARY KEY,
    program_id VARCHAR(36) NOT NULL,
    version VARCHAR(50) NOT NULL,
    required_credits INT NOT NULL,

    CONSTRAINT chk_required_credits
        CHECK (required_credits > 0),

    CONSTRAINT fk_curriculum_program
        FOREIGN KEY (program_id)
        REFERENCES academic_program(program_id)
);


/*
The SRS requires curriculum selection by program + intake year,
but the current Data Specification does not define that mapping.

This table is an implementation support table.
Replace it if the team provides an official mapping model.
*/
CREATE TABLE IF NOT EXISTS curriculum_applicability (
    curriculum_id VARCHAR(36) NOT NULL,
    intake_year INT NOT NULL,

    PRIMARY KEY (curriculum_id, intake_year),

    CONSTRAINT fk_curriculum_applicability
        FOREIGN KEY (curriculum_id)
        REFERENCES curriculum(curriculum_id)
);


-- ============================================================
-- STUDENT PROFILE
-- ============================================================

CREATE TABLE IF NOT EXISTS student_profile (
    student_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL UNIQUE,
    intake_year INT NOT NULL,
    current_semester INT NOT NULL,
    target_credit_load INT NOT NULL,
    program_id VARCHAR(36),

    CONSTRAINT chk_intake_year
        CHECK (intake_year > 1900),

    CONSTRAINT chk_current_semester
        CHECK (current_semester > 0),

    CONSTRAINT chk_target_credit_load
        CHECK (target_credit_load BETWEEN 14 AND 24),

    CONSTRAINT fk_profile_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_profile_program
        FOREIGN KEY (program_id)
        REFERENCES academic_program(program_id)
);


-- ============================================================
-- COURSE
-- ============================================================

CREATE TABLE IF NOT EXISTS course (
    course_id VARCHAR(36) PRIMARY KEY,
    course_code VARCHAR(15) NOT NULL UNIQUE,
    course_name VARCHAR(255) NOT NULL,
    credits INT NOT NULL,
    status ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',

    CONSTRAINT chk_course_credits
        CHECK (credits > 0)
);


-- ============================================================
-- ACADEMIC TERM
-- ============================================================

CREATE TABLE IF NOT EXISTS academic_term (
    term_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);


-- ============================================================
-- ACADEMIC RECORD
-- ============================================================

CREATE TABLE IF NOT EXISTS academic_record (
    record_id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_record_student
        FOREIGN KEY (student_id)
        REFERENCES student_profile(student_id)
);


CREATE TABLE IF NOT EXISTS course_attempt (
    attempt_id VARCHAR(36) PRIMARY KEY,
    record_id VARCHAR(36) NOT NULL,
    course_id VARCHAR(36) NOT NULL,
    term_id VARCHAR(36) NOT NULL,
    attempt_number INT NOT NULL,
    grade DECIMAL(3,1),
    result_status ENUM('Passed', 'Failed', 'InProgress') NOT NULL,
    credits_earned INT NOT NULL,

    CONSTRAINT chk_attempt_number
        CHECK (attempt_number >= 1),

    CONSTRAINT chk_credits_earned
        CHECK (credits_earned >= 0),

    CONSTRAINT fk_attempt_record
        FOREIGN KEY (record_id)
        REFERENCES academic_record(record_id),

    CONSTRAINT fk_attempt_course
        FOREIGN KEY (course_id)
        REFERENCES course(course_id),

    CONSTRAINT fk_attempt_term
        FOREIGN KEY (term_id)
        REFERENCES academic_term(term_id),

    CONSTRAINT uq_course_attempt
        UNIQUE (record_id, course_id, attempt_number)
);
