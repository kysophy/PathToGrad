# U005 - Course Data & Prerequisite Management

## 1. Use Case Information

| Field                              | Description                           |
| ---------------------------------- | ---------------------------------------- |
| Use Case ID                       | U005                                  |
| Use Case Name                     | Course Data & Prerequisite Management |
| Actor(s)                          | Academic Staff / Admin                |
| Related Functional Requirement(s) | FR-16                                 |
| Related Feature(s)                | F-12 Course Data Management           |

## 2. Brief Description

Allows Academic Staff to maintain the university's course catalog by importing CSV files or using the Admin API to update course codes, credits, and prerequisite chains in the MySQL database.

## 3. Pre-Condition

* The Admin is authenticated with administrative privileges.

## 4. Result

* The MySQL database is successfully updated with the latest course catalog and prerequisite rules, making them immediately available to the LLM Planning Agent.

## 5. Main Scenario

1. The Admin accesses the "Course Data Management" portal.
2. The Admin chooses to upload a new CSV file containing course metadata and prerequisite rules.
3. The system parses the file and executes a deterministic validation check (Core Logic Layer) to ensure there are no formatting errors or circular prerequisite loops.
4. The system displays a preview of the changes (e.g., "5 courses added, 2 prerequisites updated").
5. The Admin clicks "Confirm Update".
6. The system commits the changes to the MySQL database and logs the import action.

## 6. Alternative Scenarios

### A1. Invalid data format or logic conflict

1. In step 3, if the system detects circular dependencies (e.g., Course A requires B, B requires A) or missing required fields, it halts the import.
2. The system highlights the specific rows with errors.
3. The system prompts the Admin to fix them before proceeding.

### A2. API update

1. Instead of a CSV upload in step 2, the Admin pushes an update via the Admin API.
2. The system performs the same validation (step 3) and returns a JSON success or error response.

## 7. Non-Functional Constraints

- No use case-specific non-functional constraints were documented for this use case in the source requirements; the system-wide non-functional requirements (NFR-01 to NFR-09 in the Non-Functional Requirements Specification) still apply, including data protection and role-based access control.
