# Use Case Diagram - PathToGrad

## 1. Overview

This use case diagram describes the main interactions between PathToGrad and its external actors.

PathToGrad is a course planning system that helps students manage academic profiles, manage academic records, and generate study plans. The system also supports academic advisors in reviewing student plans and supports academic staff/admin users in managing course data.

The central use case is **U003 Generate Study Plan**. This use case includes retrieving course data, checking prerequisites, tracking graduation progress, detecting academic risks, and explaining the recommended plan. If the LLM provider is unavailable, the system can switch to fallback planning mode.

## 2. Actors

| Actor                  | Description                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| Student                | Main user of the system. The student can manage profile, manage academic record, and generate a study plan. |
| Academic Advisor       | Supporting user. The advisor can review student plans and warnings.                                         |
| Academic Staff / Admin | Data-related user. This actor can manage course and prerequisite data.                                      |
| LLM Provider           | External service used to support explanation generation when available.                                     |

## 3. Main Use Cases

| Use Case ID | Use Case Name          | Main Actor             |
| ----------- | ---------------------- | ---------------------- |
| U001        | Manage Profile         | Student                |
| U002        | Manage Academic Record | Student                |
| U003        | Generate Study Plan    | Student                |
| U004        | Review Student Plan    | Academic Advisor       |
| U005        | Manage Course Data     | Academic Staff / Admin |

## 4. Use Case Diagram

<img width="1431" height="699" alt="image" src="https://github.com/user-attachments/assets/67786b3d-2de5-4076-9ce4-1009e22548b2" />


## 5. Relationship Description

| Relationship                                   | Description                                                                       |
| ---------------------------------------------- | --------------------------------------------------------------------------------- |
| Student → U001 Manage Profile                  | The student creates or updates academic profile information.                      |
| Student → U002 Manage Academic Record          | The student enters completed courses, failed courses, grades, and credits.        |
| Student → U003 Generate Study Plan             | The student requests a recommended semester plan.                                 |
| Academic Advisor → U004 Review Student Plan    | The advisor reviews the student plan, warnings, and progress summary.             |
| Academic Staff/Admin → U005 Manage Course Data | Academic staff/admin users manage course and prerequisite data.                   |
| U003 → Retrieve Course Catalog                 | The system retrieves available course data from MySQL.                            |
| U003 → Check Prerequisites                     | The system checks whether the student satisfies prerequisite rules.               |
| U003 → Track Graduation Progress               | The system calculates completed and missing graduation requirements.              |
| U003 → Detect Academic Risks                   | The system detects risks such as missing prerequisites or overloaded study plans. |
| U003 → Explain Recommended Plan                | The system explains the final study plan in clear language.                       |
| Fallback Planning Mode → U003                  | Fallback mode is used when the LLM provider is unavailable.                       |
| LLM Provider → Explain Recommended Plan        | The LLM provider supports explanation generation when available.                  |

## 6. Notes

- **Student** is the primary actor for U001, U002, and U003.
- **LLM Provider** is a supporting external service, not the primary actor.
- The study plan must be checked by internal tools before being shown to the student.
- If the LLM provider fails, the system can still generate a rule-based study plan through fallback planning mode.
- U001, U002, and U003 are specified in separate use case specification files.
- U004 and U005 are included in the diagram to show the full system scope.
