# Requirements Analyst Test Case Specifications

## 1. Purpose

This document specifies the test cases assigned to the Requirements Analyst for the PathToGrad system. The test cases are derived from the approved Project Proposal, Software Requirements Specification, and Software Design Document.

The assigned testing scope covers the following functional areas:

1. Academic Profile, Academic Record, and Graduation Progress.
2. Prerequisite and Course Eligibility Validation.

The purpose of these test cases is to verify that the system processes academic data according to the documented requirements, validates invalid or incomplete input, and produces deterministic academic results based on the student record, curriculum, course catalog, prerequisite rules, and course-offering data.

## 2. Test Scope

### 2.1 Academic Profile, Academic Record, and Graduation Progress

The testing scope includes:

- Creating and updating a student academic profile.
- Validating required profile information.
- Identifying the curriculum applicable to the student's academic program and intake year.
- Adding, updating, and validating course attempts.
- Distinguishing Passed, Failed, and InProgress course attempts.
- Calculating earned credits from valid passed course attempts.
- Identifying completed and missing curriculum requirements.
- Calculating the student's graduation progress.

### 2.2 Prerequisite and Course Eligibility Validation

The testing scope includes:

- Validating courses that do not require prerequisites.
- Validating satisfied and unsatisfied prerequisites.
- Handling failed and in-progress prerequisite courses.
- Handling multiple prerequisite conditions.
- Handling missing, invalid, or uncertain prerequisite data.
- Verifying that the selected course exists in the course catalog.
- Retrieving course-offering data for the selected academic term.
- Handling courses that are not offered in the selected academic term.
- Handling missing class-section or course-offering data.

## 3. Test Basis

| Test Area | Related Feature | Related Requirement | Related Use Case | Related Design Objects |
|---|---|---|---|---|
| Academic Profile | F-01 Student Profile Management | FR-01 | U001 Manage Profile | StudentProfile, AcademicProgram, Curriculum |
| Academic Record | F-02 Academic Record Management | FR-02 | U002 Manage Academic Record | AcademicRecord, CourseAttempt, Course, AcademicTerm |
| Graduation Progress | F-06 Graduation Progress Tracker | FR-08 | U003 Generate Study Plan | AcademicRecord, CourseAttempt, Curriculum, Course |
| Course Data Retrieval | F-04 Course Catalog Tool | FR-06 | U003 Generate Study Plan | Course, Curriculum, CourseOffering |
| Prerequisite Validation | F-05 Prerequisite Checker Tool | FR-07 | U003 Generate Study Plan | Course, CourseAttempt, AcademicRecord |
| Course Eligibility and Availability | F-04 Course Catalog Tool and F-05 Prerequisite Checker Tool | FR-19 | U003 Generate Study Plan | CourseOffering, ClassSection, AcademicTerm |

## 4. Testing Techniques

The following black-box testing techniques are used in this document:

### 4.1 Functional Testing

Functional testing is used to verify whether each feature produces the expected result defined by the requirements and use-case specifications.

### 4.2 Equivalence Partitioning

Input data are divided into valid and invalid groups. Representative values from each group are selected to reduce duplicated test cases while maintaining requirement coverage.

### 4.3 Boundary Value Analysis

Boundary-value testing is applied to fields with documented limits, such as attempt number, earned credits, and configured academic constraints.

Values that are not explicitly defined in the approved project documents are not assumed. Such values must be confirmed by the team before test execution.

### 4.4 Decision-Table Testing

Decision-table testing is used for prerequisite and course-eligibility validation because the result may depend on several conditions, including prerequisite status, course existence, course offering, academic term, and data completeness.