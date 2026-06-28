# U003 - Generate Study Plan

## 1. Use Case Information

| Field                           | Description                                                      |
| ------------------------------- | ---------------------------------------------------------------- |
| Use Case ID                     | U003                                                             |
| Use Case Name                   | Generate Study Plan                                              |
| Primary Actor                   | Student                                                          |
| Supporting Actor                | LLM Provider                                                     |
| Related Functional Requirements | FR-03 to FR-14, FR-17                                            |
| Related Feature                 | LLM Planning Agent, Study Plan Generator, Fallback Planning Mode |

## 2. Brief Description

This use case allows students to request a recommended semester plan. The LLM Planning Agent receives the request, calls internal tools, checks academic rules, and returns a study plan with explanations and warnings.

## 3. Pre-Condition

* The student profile is available in the system.
* The student academic record is available in the system.
* Course catalog data is available in MySQL.

## 4. Result

* The system returns a recommended study plan.
* The plan includes prerequisite status, graduation progress, academic risks, and explanation.

## 5. Main Scenario

1. The student opens the study planning page.
2. The student enters a planning request, such as target credit load or preferred semester.
3. The system sends the request to the LLM Planning Agent.
4. The LLM Planning Agent reads the student profile and academic record.
5. The agent calls the Course Catalog Tool to retrieve course data.
6. The agent calls the Prerequisite Checker Tool to check course eligibility.
7. The agent calls the Graduation Progress Tracker to calculate completed and missing requirements.
8. The agent calls the Semester Plan Generator to create a recommended plan.
9. The agent calls the Academic Risk Detector to identify possible academic risks.
10. The system returns the recommended study plan.
11. The system explains why each course is recommended and shows warnings if needed.

## 6. Alternative Scenarios

### A1. Missing academic record

1. The student requests a study plan without entering academic records.
2. The system shows a warning message.
3. The student is asked to complete academic record information first.

### A2. Missing or uncertain course data

1. The system cannot find enough course or prerequisite data.
2. The system shows a warning that the recommendation is based on limited data.
3. The system returns only the verified parts of the plan.

### A3. LLM provider unavailable

1. The LLM provider fails or does not respond.
2. The system switches to fallback planning mode.
3. The rule-based tools generate a study plan.
4. The system provides template-based explanations instead of AI-generated explanations.

## 7. Non-Functional Constraints

- The system should verify LLM-generated recommendations using rule-based tools.
- The system should continue core planning functions when the LLM provider is unavailable.
- The system should log important agent actions and tool calls for traceability.
- The system should present planning results in clear and simple language.


