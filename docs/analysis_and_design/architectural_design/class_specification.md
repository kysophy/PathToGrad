# Class Specifications

## 1.3.1 Class C1: StudentProfile
**Responsibility:** Stores the academic context used to generate and validate a student's study plan.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `studentId: String` | Private | Required; unique | Identifies the student profile. |
| 2 | `intakeYear: Integer` | Private | Positive year | Stores the student's intake year. |
| 3 | `currentSemester: Integer` | Private | Must be positive | Stores the current study semester. |
| 4 | `targetCreditLoad: Integer` | Private | Must follow configured credit policy | Stores the expected semester credit load. |
| 5 | `academicProgram: AcademicProgram` | Private | May be empty while the profile is incomplete | Stores the selected academic program. |
| 6 | `curriculum: Curriculum` | Private | Must belong to the selected program | Stores the applicable curriculum version. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `updateProfile()` | Public | Input must be valid | Updates academic profile information. |
| 2 | `validateTargetCreditLoad()` | Public | | Checks whether the selected credit load is valid. |
| 3 | `getApplicableCurriculum()` | Public | Program and intake data should exist | Returns the curriculum applied to the student. |
| 4 | `isComplete()` | Public | | Determines whether enough information exists for planning. |

## 1.3.2 Class C2: AcademicRecord
**Responsibility:** Maintains the course attempts used for prerequisite checking and graduation-progress calculation.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `recordId: String` | Private | Required; unique | Identifies the record. |
| 2 | `updatedAt: DateTime` | Private | Automatically updated | Records the latest change time. |
| 3 | `attempts: List<CourseAttempt>` | Private | May be empty | Contains all course attempts. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `addAttempt(attempt)` | Public | Attempt must be valid | Adds a course attempt. |
| 2 | `updateAttempt(attempt)` | Public | Attempt must exist | Updates a course attempt. |
| 3 | `removeAttempt(attemptId)` | Public | Must not remove another student's attempt | Removes a course attempt. |
| 4 | `getPassedCourses()` | Public | | Returns passed courses. |
| 5 | `calculateEarnedCredits()` | Public | Count verified passed attempts only | Calculates earned credits. |

## 1.3.3 Class C3: CourseAttempt
**Responsibility:** Represents one attempt by a student to complete a course.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `attemptId: String` | Private | Required; unique | Identifies the attempt. |
| 2 | `attemptNumber: Integer` | Private | At least 1 | Indicates how many times the course has been attempted. |
| 3 | `grade: Decimal` | Private | Must follow the supported grading scale | Stores the result grade. |
| 4 | `resultStatus: ResultStatus` | Private | Passed, Failed, or InProgress | Stores the attempt status. |
| 5 | `creditsEarned: Integer` | Private | Cannot be negative | Stores credits earned from the attempt. |
| 6 | `course: Course` | Private | Required | Identifies the attempted course. |
| 7 | `term: AcademicTerm` | Private | May be empty for incomplete records | Identifies the academic term. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `isPassed()` | Public | | Returns whether the attempt passed. |
| 2 | `validateAttempt()` | Public | | Validates grade, status, term, and credits. |
| 3 | `calculateEarnedCredits()` | Public | Passed attempts only | Returns earned credits. |

## 1.3.4 Class C4: Course
**Responsibility:** Represents a course and its general academic information.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `courseId: String` | Private | Required; unique | Identifies the course. |
| 2 | `courseCode: String` | Private | Required; unique | Stores the official course code. |
| 3 | `courseName: String` | Private | Required | Stores the course name. |
| 4 | `credits: Integer` | Private | Greater than zero | Stores the number of credits. |
| 5 | `suggestedSemester: Integer` | Private | May be empty | Stores the suggested study semester. |
| 6 | `status: CourseStatus` | Private | Active or Archived | Store availability status. |
| 7 | `prerequisites: List<CoursePrerequisite>` | Private | May be empty | Stores prerequisite courses. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `getPrerequisites()` | Public | | Returns prerequisite courses. |
| 2 | `isActive()` | Public | | Check whether the course is active. |

## 1.3.5 Class C5: Curriculum
**Responsibility:** Defines course and credit requirements for an academic-program version.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `curriculumId: String` | Private | Required; unique | Identifies the curriculum. |
| 2 | `version: String` | Private | Required | Stores the curriculum version. |
| 3 | `requiredCredits: Integer` | Private | Cannot be negative | Stores total required credits. |
| 4 | `effectiveIntakeYear: Integer` | Private | Required | Identifies the intake from which it applies. |
| 5 | `curriculumCourses: List<CurriculumCourse>` | Private | May initially be empty | Stores the course requirements defined for this curriculum. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `getRequiredCourses()` | Public | | Returns compulsory courses. |
| 2 | `getElectiveCourses()` | Public | | Returns elective courses. |
| 3 | `calculateMissingRequirements(record)` | Public | Record must be available | Returns remaining requirements. |
| 4 | `appliesTo(profile)` | Public | | Checks whether the curriculum applies to a profile. |

## 1.3.6 Class C6: CourseOffering
**Responsibility:** Represents the availability of one course in an academic term.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `offeringId: String` | Private | Required; unique | Identifies the offering. |
| 2 | `course: Course` | Private | Required | Identifies the offered course. |
| 3 | `term: AcademicTerm` | Private | Required | Identifies the academic term. |
| 4 | `status: OfferingStatus` | Private | Active, Inactive, or Archived | Stores offering status. |
| 5 | `sections: List<ClassSection>` | Private | May be empty | Stores available class sections. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `getAvailableSections()` | Public | Active sections only | Returns selectable sections. |
| 2 | `addSection(section)` | Public | Section must be valid | Adds a class section. |
| 3 | `isAvailable()` | Public | | Checks whether the offering can be used. |

## 1.3.7 Class C7: ClassSection
**Responsibility:** Represents a selectable class and its meeting schedule.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `sectionId: String` | Private | Required; unique | Identifies the class section. |
| 2 | `sectionCode: String` | Private | Required | Stores the section code. |
| 3 | `courseOffering` | Private | Required; must refer to one course offering | Identifies the course offering to which the section belong to. |
| 4 | `capacity: Integer` | Private | Cannot be negative | Stores planned capacity. |
| 5 | `status: SectionStatus` | Private | Active, Inactive, or Archived | Stores section status. |
| 6 | `meetings: List<SectionMeeting>` | Private | May be empty | Stores meeting times. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `getMeetingTimes(): List<SectionMeeting>` | Public | | Returns section meetings. |
| 2 | `addMeeting(meeting: SectionMeeting): void` | Public | Meeting must be valid | Adds a meeting time to the section. |
| 3 | `conflictsWith(other:ClassSection):Boolean` | Public | | Checks schedule overlap. |
| 4 | `isAvailable(): Boolean` | Public | | Checks whether the section is selectable. |

## 1.3.8 Class C8: StudyPlan
**Responsibility:** Stores a versioned semester plan and controls its review lifecycle.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `planId: String` | Private | Required; unique | Identifies the plan version. |
| 2 | `studentProfile` | Private | Required | Identifies the student who owns the plan. |
| 3 | `targetTerm: AcademicTerm` | Private | May be empty in Draft | Identifies the academic term targeted by the plan. |
| 4 | `versionNumber: Integer` | Private | At least 1 | Stores version number. |
| 5 | `status: PlanStatus` | Private | Draft, PendingReview, Approved, NeedsRevision, or Superseded | Stores lifecycle status. |
| 6 | `generationMode: GenerationMode` | Private | LLM or Fallback | Stores generation mode. |
| 7 | `targetCreditLoad: Integer` | Private | Must follow configured policy | Stores requested credit load. |
| 8 | `totalCredits: Integer` | Private | Derived from plan items | Stores total plan credits. |
| 9 | `previousVersion: StudyPlan` | Private | Optional | Links to the earlier version. |
| 10 | `items: List<StudyPlanItem>` | Private | May be empty in Draft | Stores recommended courses. |
| 11 | `createdAt` | Private | Automatically set when created | Stores the plan creation time. |
| 12 | `updatedAt: DateTime` | Private | Automatically updated | Stores the latest update time. |
| 13 | `submittedAt: DateTime` | Private | | Stores the time the plan was submitted for review. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `addItem(item:StudyPlanItem): void` | Public | Plan must be editable | Adds a course item. |
| 2 | `removeItem(itemId:String): void` | Public | Plan must be Draft | Removes an item. |
| 3 | `calculateTotalCredits(): Integer` | Public | | Calculates total credits. |
| 4 | `validatePlan(): Boolean` | Public | Uses verified rules | Validates prerequisites, load, and timetable. |
| 5 | `saveDraft(): void` | Public | | Saves the plan as Draft. |
| 6 | `submitForReview(): void` | Public | Blocking errors must be resolved | Changes status to PendingReview. |
| 7 | `createRevision(): StudyPlan` | Public | Source should require revision | Creates a new Draft version. |

## 1.3.9 Class C9: PlanReview
**Responsibility:** Stores an advisor's decision and comment for one submitted plan version.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `reviewId: String` | Private | Required; unique | Identifies the review. |
| 2 | `decision: ReviewDecision` | Private | Approved or NeedsRevision | Stores advisor decision. |
| 3 | `comment: String` | Private | Required for NeedsRevision | Stores advisor feedback. |
| 4 | `reviewedAt: DateTime` | Private | Set when decision is recorded | Stores review time. |
| 5 | `advisor: User` | Private | User must have Advisor role | Identifies the reviewer. |
| 6 | `studyPlan: StudyPlan` | Private | Must be PendingReview | Identifies the reviewed plan. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `approve(comment)` | Public | Plan must be PendingReview | Approves the plan. |
| 2 | `requestRevision(comment)` | Public | Comment is required | Requests plan revision. |
| 3 | `validateComment()` | Public | | Check comment requirements. |

## 1.3.10 Class C10: LLMPlanningAgent
**Responsibility:** Coordinates planning requests, selects tools, calls the provider, validates results and activates fallback mode.

| Seq | Property | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `toolRegistry: ToolRegistry` | Private | Required | Provides available planning tools. |
| 2 | `providerAdapter: LLMProviderAdapter` | Private | One configured provider | Connects to the LLM provider. |
| 3 | `fallbackPlanner: FallbackPlanner` | Private | Required | Provides rule-based fallback. |
| 4 | `logService: AgentLogService` | Private | Required | Records runs and tool calls. |

| Seq | Operation | Modifier | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `generateStudyPlan(request)` | Public | Student data must be available | Coordinates plan generation. |
| 2 | `selectTools(request)` | Private | | Selects tools required for the request. |
| 3 | `callTool(name, input)` | Private | Tool must be registered | Executes a planning tool. |
| 4 | `explainPlan(plan)` | Private | Explanation must use verified tool results | Produces the final explanation. |
| 5 | `activateFallback(request)` | Private | Used when the provider is unavailable | Generates a rule-based plan. |
| 6 | `validateFinalResult(plan)` | Private | All recommendations must be verified | Prevents unsupported recommendations. |