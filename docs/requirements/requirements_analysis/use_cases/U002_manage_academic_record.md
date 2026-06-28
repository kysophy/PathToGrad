# UC02 - Check Prerequisites

## Use Case Name

Check Prerequisites

## Primary Actor

Student

## Goal

Allow a student to check whether they are eligible to take selected courses based on completed courses and prerequisite rules.

## Preconditions

- The course database is available.
- Prerequisite data is available.
- The student has provided completed course information.

## Trigger

The student selects one or more courses to check.

## Main Flow

1. The student opens the prerequisite checking feature.
2. The student selects the course or courses they want to take.
3. The system retrieves prerequisite rules for the selected courses.
4. The system compares the prerequisites with the student's completed courses.
5. The system identifies eligible and ineligible courses.
6. The system explains missing prerequisites if any.
7. The system displays the result to the student.

## Alternative Flow

### A1 - Course has no prerequisite

1. The system detects that the selected course has no prerequisite.
2. The system marks the course as eligible.

### A2 - Prerequisite data is missing

1. The system cannot find prerequisite data for the selected course.
2. The system shows a warning that the result cannot be fully verified.
3. The student may contact an academic advisor for confirmation.

## Postconditions

- The student knows whether each selected course can be taken.
- Missing prerequisite courses are displayed clearly.

## Business Rules

- A course is eligible only if all required prerequisites are satisfied.
- The prerequisite result must be based on official curriculum data.
- If prerequisite data is missing, the system must not give a fully confirmed result.

## Related Functional Requirements

- Search course information.
- Check course prerequisites.
- Display missing prerequisites.
- Warn users when course data is incomplete.
