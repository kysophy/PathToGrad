# UC03 - Track Graduation Progress

## Use Case Name

Track Graduation Progress

## Primary Actor

Student

## Supporting Actor

Academic Advisor

## Goal

Allow a student to monitor their graduation progress by comparing completed courses with program requirements.

## Preconditions

- The student's completed course list is available.
- The curriculum and graduation requirements are available.
- Credit requirements are defined in the system.

## Trigger

The student opens the graduation progress tracking feature.

## Main Flow

1. The student opens the graduation progress page.
2. The system retrieves the student's completed courses.
3. The system retrieves the program requirements.
4. The system calculates completed credits and remaining credits.
5. The system identifies completed, in-progress, and missing requirements.
6. The system displays the graduation progress summary.
7. The student reviews the remaining requirements.
8. The student may use the result to update their study plan.

## Alternative Flow

### A1 - Completed course data is incomplete

1. The system detects missing or incomplete course history.
2. The system asks the student to update the missing information.
3. The system recalculates graduation progress after the update.

### A2 - Advisor reviews progress

1. The academic advisor opens the student's progress summary.
2. The advisor checks whether the student is on track.
3. The advisor gives recommendations if needed.

## Postconditions

- The student can see current graduation progress.
- Remaining requirements are clearly listed.
- The result can support study plan generation.

## Business Rules

- Graduation progress must be calculated from official curriculum requirements.
- Completed credits must match approved course records.
- Missing data must be shown as incomplete instead of being assumed.

## Related Functional Requirements

- Track completed courses.
- Calculate completed and remaining credits.
- Display graduation progress.
- Support advisor review.
