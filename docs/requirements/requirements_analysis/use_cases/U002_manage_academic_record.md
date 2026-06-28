# U002 - Manage Academic Record

## 1. Use Case Information

| Field                          | Description                |
| ------------------------------ | -------------------------- |
| Use Case ID                    | U002                       |
| Use Case Name                  | Manage Academic Record     |
| Actor                          | Student                    |
| Related Functional Requirement | FR-02                      |
| Related Feature                | Academic Record Management |

## 2. Brief Description

This use case allows students to enter and update academic records, including completed courses, failed courses, grades, and credits. The system uses this data for prerequisite checking and graduation progress tracking.

## 3. Pre-Condition

* The student profile already exists in the system.
* Course data is available in the system.

## 4. Result

* The academic record is saved.
* The academic record can be used by the planning tools.

## 5. Main Scenario

1. The student opens the academic record page.
2. The system displays the academic record form or course list.
3. The student enters completed courses, failed courses, grades, and credits.
4. The student submits the academic record.
5. The system validates the entered data.
6. The system saves the academic record.
7. The system updates prerequisite status and graduation progress data.

## 6. Alternative Scenarios

### A1. Course not found

1. The student enters a course that does not exist in the course catalog.
2. The system shows a warning message.
3. The student selects a valid course from the available course list.

### A2. Missing grade or credit information

1. The student submits a record with missing grade or credit information.
2. The system asks the student to complete the missing fields.
3. The student updates the record.
4. The student submits the record again.

## 7. Non-Functional Constraints

- The system should store academic record data in MySQL.
- The system should protect student academic information.
- The system should show clear warnings when data is missing or uncertain.


