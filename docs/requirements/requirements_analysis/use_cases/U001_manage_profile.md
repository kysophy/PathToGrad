# U001 - Manage Profile

## 1. Use Case Information

| Field                              | Description                     |
| ---------------------------------- | -------------------------------- |
| Use Case ID                       | U001                            |
| Use Case Name                     | Manage Profile                  |
| Actor(s)                          | Student                         |
| Related Functional Requirement(s) | FR-01                           |
| Related Feature(s)                | F-01 Student Profile Management |

## 2. Brief Description

This use case allows students to create and update their academic profile. The profile includes major, intake year, current semester, and target credit load. The system uses this information for course planning.

## 3. Pre-Condition

* The student has opened the PathToGrad system.
* The student has access to the profile page.

## 4. Result

* The student profile is saved.
* The profile can be used by the LLM Planning Agent and internal planning tools.

## 5. Main Scenario

1. The student opens the profile page.
2. The system displays the profile form.
3. The student enters major, intake year, current semester, and target credit load.
4. The student submits the form.
5. The system validates the input data.
6. The system saves the student profile.
7. The system shows a success message.

## 6. Alternative Scenarios

### A1. Missing required information

1. The student leaves a required field empty.
2. The system shows an error message.
3. The student corrects the missing information.
4. The student submits the form again.

### A2. Invalid target credit load

1. The student enters an invalid target credit load.
2. The system shows an error message.
3. The student edits the value.
4. The student submits the form again.

## 7. Non-Functional Constraints

- The system should present the profile form in clear and simple language.
- The system should protect student academic information.
- The system should restrict access based on user roles.
