# System Architect Test Case Specifications

## 1. Purpose
This document specifies the test cases assigned to the System Architect for the PathToGrad system. The test cases are derived from the approved Project Proposal, Software Requirements Specification, and Software Design Document.

The assigned testing scope covers the following functional areas:
1. Core Logic validation, deterministic rule enforcement, and data boundaries.
2. Orchestration Layer fallback mechanisms and API routing.
3. Database integrity, plan versioning, and advisor review state transitions.

The purpose of these test cases is to verify that the underlying architecture correctly processes algorithms (such as the Prerequisite Checker DAG), maintains strict data integrity in MySQL, handles external LLM timeouts gracefully via fallback routing, and accurately manages the lifecycle of study plan versions.

## 2. Test Scope

### 2.1 Core Logic and Data Boundaries
The testing scope includes:
- Validating attempt-number and earned-credit database boundaries.
- Calculating graduation progress strictly from verified, passed attempts.
- Evaluating required-credit boundary logic at the exact threshold.
- Detecting missing required core courses despite sufficient total credits.
- Verifying DAG logic for courses with zero prerequisites vs. satisfied/unsatisfied prerequisites.
- Handling incomplete prerequisite graphs and querying course offering availability.

### 2.2 Advisor Review, Fallback, and Versioning
The testing scope includes:
- Retrieving and viewing submitted study plans and student academic info via API.
- Executing database state transitions for plan approval and revision requests.
- Writing and storing advisor feedback comments.
- Intercepting LLM API failures and triggering the rule-based Fallback Planner.
- Creating Draft plans, transitioning them to PendingReview, and viewing chronological version history.
- Generating new revisions without overwriting immutable historical plan records.

## 3. Test Basis

| Test Area | Related Feature | Related Requirement | Related Use Case | Related Design Objects |
|---|---|---|---|---|
| Data Boundaries & Logic | F-02, F-06 | FR-02, FR-08 | U002, U003 | CourseAttempt, Curriculum |
| DAG Prerequisites | F-05 Prerequisite Checker | FR-07 | U003 Generate Study Plan | Course, Prerequisite |
| Advisor Review Workflow | F-11 Advisor Plan Review | FR-15 | U004 Advisor Plan Review | PlanReview, StudyPlan |
| Orchestration & Fallback | F-10 Fallback Planning | FR-13, FR-17 | U003 Generate Study Plan | LLMPlanningAgent, FallbackPlanner |
| Plan Versioning | F-07 Semester Plan Generator | FR-22, FR-23 | U003, U004 | StudyPlan, StudyPlanItem |

## 4. Testing Techniques
The following testing techniques are used in this document:

### 4.1 White-Box Testing (Unit & Integration)
Used extensively for the Core Logic Layer to verify that the Python deterministic engine correctly traverses the Prerequisite Checker DAG, performs credit calculations, and executes database queries safely.

### 4.2 Boundary Value Analysis
Applied to backend database constraints and calculation logic, ensuring that database limits (e.g., attempt numbers >= 1, non-negative earned credits) and curriculum thresholds are strictly enforced.

### 4.3 State Transition Testing
Used to verify the lifecycle of a Study Plan. Tests ensure that a plan correctly transitions through valid states (`Draft` -> `PendingReview` -> `Approved` or `Needs Revision` -> `Draft` for new version) without skipping mandatory steps or violating data immutability.

## 5. Test Cases

### 5.1 Core Logic and Constraints
*   **TC-10 Validate attempt-number boundaries:** Verify that the database accepts attempt number 1 as the minimum valid value and rejects attempt number 0.
*   **TC-11 Validate earned-credit boundaries:** Verify that negative earned credits are rejected, while 0 is accepted for Failed/InProgress statuses.
*   **TC-12 Calculate graduation progress from mixed attempts:** Verify that the logic engine only aggregates verified Passed attempts for earned credits, ignoring Failed/InProgress data.
*   **TC-13 Evaluate the required-credit boundary:** Verify logic when earned credits equal required credits minus one (Incomplete) versus exact required credits (Satisfied).
*   **TC-14 Detect missing required courses:** Verify that the system blocks graduation completion if a mandatory course is missing, even if total credits are met.
*   **TC-15 Confirm completed graduation requirements:** Verify that full completion is triggered only when both credit totals and all required courses are satisfied.
*   **TC-16 Validate a course without prerequisites:** Verify the DAG engine returns immediate eligibility for base courses with zero dependencies.
*   **TC-17 Validate satisfied prerequisites:** Verify the DAG engine returns eligibility when the required prerequisite has a Passed attempt.
*   **TC-18 Validate unsatisfied prerequisite decisions:** Verify that Failed, InProgress, or Unattempted prerequisites correctly return an ineligible status.
*   **TC-19 Handle uncertain prerequisite data:** Verify that the logic layer halts and issues a warning rather than bypassing rules when prerequisite definitions are corrupt or missing.
*   **TC-20 Validate course offering availability:** Verify that the system queries class sections accurately, confirming availability for the selected term and rejecting unoffered courses.

### 5.2 Advisor Review, Fallback & Versioning
*   **TC-24 View submitted study plan:** Verify that API endpoints successfully return full plan payloads (sections, timetables, credits) to the advisor.
*   **TC-25 View academic info:** Verify that the advisor context API fetches the correct student profile, GPA, and graduation metrics during review.
*   **TC-26 Provide plan comments:** Verify that advisor feedback strings are successfully written to the `PLAN_REVIEW` table with correct foreign keys.
*   **TC-27 Approve suitable plans:** Verify that approving a plan correctly updates the `STUDY_PLAN.status` to `Approved` in the database.
*   **TC-28 Request plan revision:** Verify that an advisor can update status to `Needs Revision` and that submitting without a mandatory comment is rejected by the backend.
*   **TC-29 Record fallback actions:** Verify that blocking the LLM API triggers the Fallback Controller, generates a rule-based plan, and logs the fallback event in the system audit logs.
*   **TC-30 Save plan as Draft:** Verify that a newly generated plan is successfully persisted in MySQL with a `Draft` status.
*   **TC-31 Submit Draft for review:** Verify the state transition from `Draft` to `PendingReview`, locking the plan from further student edits.
*   **TC-32 View plan version history:** Verify that database queries return a chronologically ordered list of all historical plan iterations and statuses for a student.
*   **TC-33 View review status and decisions:** Verify that the presentation layer accurately fetches and displays `Approved` or `Needs Revision` badges alongside advisor comments.
*   **TC-34 Create new revision without overwriting:** Verify that triggering a revision on a returned plan generates a new database record (new `version_number`) linked via `previousVersion`, keeping the old record immutable.