# Business Analyst Test Case Specifications

## 1. Purpose
This document specifies the test cases assigned to the Business Analyst for the PathToGrad system. The test cases are derived from the approved Project Proposal, Software Requirements Specification, and Software Design Document.

The assigned testing scope covers the following functional areas:
1. Academic Profile and Academic Record Management workflows.
2. Authentication, User Access, and Role Management.

The purpose of these test cases is to verify that the system accurately captures user input, provides clear frontend validation, handles edge cases in data entry, and correctly routes users based on their assigned system roles.

## 2. Test Scope

### 2.1 Academic Profile and Academic Record Management
The testing scope includes:
- Creating and updating a student academic profile.
- Validating required profile information and handling missing inputs.
- Enforcing target credit-load boundaries (14-24 credits).
- Handling unavailable curriculum mappings for specific intake years.
- Adding valid passed course attempts to the academic record.
- Distinguishing and recording failed or in-progress attempts.
- Rejecting unknown courses or incomplete grade/credit submissions.

### 2.2 Authentication and Role Management
The testing scope includes:
- Verifying successful logins for Student, Advisor, and Admin roles.
- Handling failed login attempts with invalid credentials.
- Managing the password recovery and reset workflow.

## 3. Test Basis

| Test Area | Related Feature | Related Requirement | Related Use Case | Related Design Objects |
|---|---|---|---|---|
| Academic Profile | F-01 Student Profile Management | FR-01 | U001 Manage Profile | StudentProfile, AcademicProgram, Curriculum |
| Academic Record | F-02 Academic Record Management | FR-02 | U002 Manage Academic Record | AcademicRecord, CourseAttempt, Course |
| Authentication & Roles | Authentication & Role Management | NFR-04 | SCR-01 Login | User |

## 4. Testing Techniques
The following black-box testing techniques are used in this document:

### 4.1 Functional Testing
Functional testing is used to verify whether each feature produces the expected result defined by the requirements and use-case specifications, such as successful profile saves and correct dashboard routing.

### 4.2 Equivalence Partitioning
Input data are divided into valid and invalid groups. Representative values from each group (e.g., registered vs. unregistered email addresses, known vs. unknown course codes) are selected to reduce duplicated test cases while maintaining requirement coverage.

### 4.3 Boundary Value Analysis
Boundary-value testing is applied to fields with documented limits, specifically testing the extreme edges of the target credit load (e.g., 13, 14, 24, and 25).

## 5. Test Cases

### 5.1 Academic Profile and Record
*   **TC-01 Create a valid academic profile:** Verify that a complete and valid academic profile (Faculty, Program, Track, Intake, Semester, Target Credit Load) can be saved successfully.
*   **TC-02 Reject missing required profile information:** Verify that omitting a mandatory field rejects the profile save and displays a clear validation message.
*   **TC-03 Validate target credit-load boundaries:** Verify that values 14 and 24 are accepted, while values 13 and 25 are rejected with a credit-load policy error.
*   **TC-04 Handle unavailable curriculum mapping:** Verify the system's behavior and warning generation when no curriculum matches the selected program and intake year.
*   **TC-05 Update an existing academic profile:** Verify that valid profile information can be updated in-place without creating a duplicate profile.
*   **TC-06 Add a valid Passed course attempt:** Verify that a valid Passed attempt is saved, added to completed courses, and increments earned credits.
*   **TC-07 Record Failed and InProgress attempts:** Verify that Failed and InProgress attempts are stored but do not contribute to completed courses or earned credits.
*   **TC-08 Reject an unknown course:** Verify validation blocks submission when an entered course does not exist in the course catalog.
*   **TC-09 Reject missing grade or credit information:** Verify that validation fails and the user is prompted when required course-attempt information (grade or credits) is incomplete.

### 5.2 Authentication & Roles
*   **TC-21 Login success:** Verify that a user with each role (Student, Advisor, Admin) can successfully log in and access their respective dashboards.
*   **TC-22 Login failed:** Verify that incorrect login information displays a clear error and denies dashboard access.
*   **TC-23 Forgot password:** Verify that the system successfully handles the reset password workflow via email verification code.