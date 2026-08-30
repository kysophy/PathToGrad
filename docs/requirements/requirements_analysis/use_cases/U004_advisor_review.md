# U004 - Advisor Plan Review

## 1. Use Case Information

| Field                              | Description                    |
| ---------------------------------- | -------------------------------- |
| Use Case ID                       | U004                            |
| Use Case Name                     | Advisor Plan Review             |
| Actor(s)                          | Academic Advisor                |
| Related Functional Requirement(s) | FR-15                           |
| Related Feature(s)                | F-11 Advisor Plan Review View   |

## 2. Brief Description

Allows Academic Advisors to view a summarized dashboard of a student's LLM-generated semester plan, evaluate identified academic risks, and provide official feedback or approval.

## 3. Pre-Condition

* The Advisor is authenticated in the system.
* The target student has successfully generated at least one semester plan using the LLM Planning Agent or Fallback Mode.

## 4. Result

* The student's plan is marked as "Approved" or "Needs Revision" with attached advisor comments.

## 5. Main Scenario

1. The Advisor navigates to the "Student Plans Dashboard".
2. The system retrieves and displays a list of pending student plans.
3. The Advisor selects a specific student.
4. The system triggers the Advisor Summary Skill, fetching the student's academic profile, the proposed weekly schedule, and any flagged academic risks (e.g., missing prerequisites, heavy credit load).
5. The Advisor reviews the AI-generated summary and visual schedule.
6. The Advisor selects "Approve Plan" or "Request Revision" and inputs an optional text comment.
7. The system updates the plan's status in the MySQL database and notifies the student.

## 6. Alternative Scenarios

### A1. LLM summary unavailable (timeout)

1. In step 4, if the API call to generate the summary fails, the system defaults to Fallback Mode.
2. The system displays the raw rule-based data and a template-based warning summary instead of the AI summary.

### A2. Empty data

1. In step 2, if no students have generated plans, the system displays a "No pending reviews" message.

## 7. Non-Functional Constraints

- No use case-specific non-functional constraints were documented for this use case in the source requirements; the system-wide non-functional requirements (NFR-01 to NFR-09 in the Non-Functional Requirements Specification) still apply, including data protection and role-based access control.
