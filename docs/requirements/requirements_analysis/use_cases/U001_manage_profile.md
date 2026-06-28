# UC01 - Generate Study Plan

## Use Case Name

Generate Study Plan

## Primary Actor

Student

## Supporting Actor

LLM Service

## Goal

Allow a student to generate a suggested semester-by-semester study plan based on their completed courses, remaining courses, prerequisites, and graduation requirements.

## Preconditions

- The student has entered or uploaded their academic information.
- Curriculum data and prerequisite rules are available in the system.
- The system has access to the course list and graduation requirements.

## Trigger

The student selects the option to generate a study plan.

## Main Flow

1. The student opens the study planning feature.
2. The system asks for required information, such as completed courses, current semester, target graduation time, and preferred course load.
3. The student submits the information.
4. The system checks completed and remaining courses.
5. The system checks prerequisite rules.
6. The LLM Service generates a suggested study plan.
7. The system validates the plan using rule-based prerequisite checking.
8. The system displays the suggested plan to the student.
9. The student reviews and edits the plan if needed.
10. The system saves the final plan.

## Alternative Flow

### A1 - Missing student information

1. The system detects missing academic information.
2. The system asks the student to complete the missing fields.
3. The student updates the information.
4. The use case continues from Step 4.

### A2 - LLM Service is unavailable

1. The system detects that the LLM Service is unavailable.
2. The system generates a basic plan using rule-based logic.
3. The system informs the student that the plan may have limited explanation.

## Postconditions

- A study plan is generated and saved.
- The student can view, edit, or submit the plan for advisor review.

## Business Rules

- A course cannot be planned before its prerequisite is completed.
- The study plan must follow curriculum and graduation requirements.
- The system must not rely only on LLM output for prerequisite validation.

## Related Functional Requirements

- Generate study plan.
- Check prerequisite conflicts.
- Track remaining courses.
- Save and update study plan.
