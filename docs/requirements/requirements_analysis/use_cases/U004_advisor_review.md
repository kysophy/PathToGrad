# U004 - Advisor Plan Review

## 1. Use Case Information

| Field                          | Description                                                                 |
| ------------------------------ | --------------------------------------------------------------------------- |
| Use Case ID                    | U004                                                            |
| Use Case Name                  | Advisor Plan Review                                           |
| Actor                          | Academic Advisor                                                |
| Related Functional Requirement | FR-15                                                          |
| Related Feature                | F-11 Advisor Plan Review View                                  |

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
4. The system triggers the Advisor Summary Skill, fetching the student's academic profile, the proposed 7-day schedule, and any flagged academic risks (e.g., missing prerequisites, heavy credit load).
5. The Advisor reviews the AI-generated summary and visual schedule.
6. The Advisor selects "Approve Plan" or "Request Revision" and inputs an optional text comment.
7. The system updates the plan's status in the database and notifies the student.

## 6. Alternative Scenarios

### A1. LLM Summary Unavailable (Timeout)
1. In step 4, if the API call to generate the summary fails, the system defaults to Fallback Mode.
2. The system displays the raw rule-based data and a template-based warning summary instead of the AI summary.

### A2. Empty Data
1. In step 2, if no students have generated plans, the system displays a "No pending reviews" message.