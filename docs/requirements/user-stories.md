# User Stories

## 1. Purpose

This document describes the main user stories for PathToGrad. Each user story is identified with a US-XX ID and, where applicable, links to the corresponding F-XX feature from the Feature Specification.

PathToGrad is an LLM-powered course planning system. Students can ask the LLM Planning Agent for course planning support. The agent uses internal tools to check prerequisites, review graduation progress, generate a semester plan, detect academic risks, and explain the result.

The system also supports a fallback planning mode. If the LLM provider is unavailable, the rule-based planning tools can still generate a valid plan.

## 2. Stakeholders

Students are primary users. They need support in planning semesters, checking prerequisites, and checking graduation progress.

Academic advisors are supporting users. They may use the system to understand a student's plan and give academic advice.

Academic staff or admin users are data-related users. They are responsible for maintaining course and prerequisite information. In the MVP version, this data may be prepared manually by the development team.

## 3. User Story Map

The student journey starts when a student enters academic records. Then the student asks the LLM Planning Agent for a study plan. The agent calls internal tools, validates the plan, detects risks, and explains the final recommendation.

If the LLM provider is unavailable, fallback planning mode returns a rule-based plan and a template-based explanation.

Academic advisors can review student plans. Academic staff can update course and prerequisite data.

**User Activity 1: Create academic profile**
- **User Need:** Students need the system to understand their academic context.
- **User Story:** As a student, I want to create my academic profile, so that the system can understand my major, intake year, current semester, and credit target.
- **Feature Link:** F-01 Student Profile Management.

**User Activity 2: Enter academic record**
- **User Need:** Students need the system to know completed courses, failed courses, grades, and credits.
- **User Story:** As a student, I want to enter my academic record, so that the system can identify my completed, failed, and remaining courses.
- **Feature Link:** F-02 Academic Record Management.

**User Activity 3: Ask for planning support**
- **User Need:** Students need a smart assistant to guide course planning.
- **User Story:** As a student, I want to ask the LLM Planning Agent for a semester plan, so that I can receive a suitable and explainable recommendation.
- **Feature Link:** F-03 LLM Planning Agent.

**User Activity 4: Retrieve course data**
- **User Need:** The agent needs course data before planning.
- **User Story:** As a student, I want the system to use course catalog data, so that the recommended plan is based on available course information.
- **Feature Link:** F-04 Course Catalog Tool.

**User Activity 5: Check prerequisites**
- **User Need:** Students need to avoid courses they are not eligible to take.
- **User Story:** As a student, I want the system to check prerequisites, so that I only choose courses that match my academic record.
- **Feature Link:** F-05 Prerequisite Checker Tool.

**User Activity 6: Track graduation progress**
- **User Need:** Students need to know completed and missing graduation requirements.
- **User Story:** As a student, I want to track my graduation progress, so that I can know what I still need to complete.
- **Feature Link:** F-06 Graduation Progress Tracker.

**User Activity 7: Generate semester plan**
- **User Need:** Students need a valid plan for the next semester.
- **User Story:** As a student, I want the system to suggest a semester plan, so that I can choose suitable courses.
- **Feature Link:** F-07 Semester Plan Generator.

**User Activity 8: Detect academic risks**
- **User Need:** Students need warnings before making risky planning decisions.
- **User Story:** As a student, I want the system to detect academic risks, so that I can avoid invalid course choices or delayed graduation.
- **Feature Link:** F-08 Academic Risk Detector.

**User Activity 9: Understand recommendation**
- **User Need:** Students need to understand why each course is recommended.
- **User Story:** As a student, I want to see explanations and warnings, so that I can understand the suggested plan.
- **Feature Link:** F-09 AI Explanation and Warning.

**User Activity 10: Use fallback planning**
- **User Need:** Students need the system to remain usable when the LLM provider is unavailable.
- **User Story:** As a student, I want the system to provide fallback planning mode, so that I can still receive a valid course plan.
- **Feature Link:** F-10 Fallback Planning Mode.

**User Activity 11: Review student plan**
- **User Need:** Advisors need to review student plans and risks.
- **User Story:** As an academic advisor, I want to view a student's plan summary, so that I can give suitable academic advice.
- **Feature Link:** F-11 Advisor Plan Review View.

**User Activity 12: Manage course data**
- **User Need:** Academic staff need to keep course and prerequisite data correct.
- **User Story:** As an academic staff member, I want to update course and prerequisite data, so that the system can generate accurate course plans.
- **Feature Link:** F-12 Course Data Management.

## 4. User Stories

**US-01: Create Academic Profile**
As a student, I want to create my academic profile, so that the system can understand my curriculum requirements.

**Acceptance Criteria:**
- The student can enter major, intake year, current semester, and target credit load.
- The system saves the academic profile.
- The LLM Planning Agent can use this profile for planning.

**US-02: Enter Academic Record**
As a student, I want to enter my academic record, so that the system can identify my completed, failed, and remaining courses.

**Acceptance Criteria:**
- The student can enter completed courses, failed courses, grades, and credits.
- The system stores the academic record.
- The system uses the record for prerequisite checking and progress tracking.

**US-03: Ask LLM Planning Agent**
As a student, I want to ask the LLM Planning Agent for a semester plan, so that I can receive a suitable and explainable recommendation.

**Acceptance Criteria:**
- The student can send a planning request.
- The LLM Planning Agent processes the request.
- The agent calls internal tools before giving the final answer.

**US-04: Retrieve Course Catalog**
As a student, I want the system to use course catalog data, so that the recommended plan is based on available course information.

**Acceptance Criteria:**
- The system stores course data in MySQL.
- The Course Catalog Tool can retrieve course code, course name, credits, semester, and prerequisites.
- The LLM Planning Agent can use the retrieved course data.

**US-05: Check Prerequisites**
As a student, I want the system to check prerequisites, so that I only choose courses that match my academic record.

**Acceptance Criteria:**
- The Prerequisite Checker Tool compares selected courses with completed courses.
- The system shows whether the student is eligible for each course.
- Invalid courses are not recommended without warning.

**US-06: Track Graduation Progress**
As a student, I want to track my graduation progress, so that I can know what I still need to complete before graduation.

**Acceptance Criteria:**
- The system shows completed credits.
- The system shows remaining credits.
- The system shows completed and missing required courses.

**US-07: Generate Semester Plan**
As a student, I want the system to suggest a semester plan, so that I can choose suitable courses.

**Acceptance Criteria:**
- The system uses student profile, academic record, course catalog, prerequisite rules, and graduation requirements.
- The suggested courses satisfy prerequisite rules.
- The plan follows the target credit load when possible.

**US-08: Detect Academic Risks**
As a student, I want the system to detect academic risks, so that I can avoid invalid course choices or delayed graduation.

**Acceptance Criteria:**
- The system detects missing prerequisites.
- The system detects overloaded credit plans.
- The system detects important missing required courses.
- The system shows warnings to the student.

**US-09: Explain Recommended Plan**
As a student, I want to see explanations and warnings, so that I can understand the suggested plan.

**Acceptance Criteria:**
- The LLM explains why each course is recommended.
- The explanation is based on tool results and course data.
- The explanation is written in clear language.

**US-10: Use Fallback Planning Mode**
As a student, I want the system to provide a fallback planning mode, so that I can still receive a valid course plan when the LLM provider is unavailable.

**Acceptance Criteria:**
- The system detects LLM provider errors or unavailable responses.
- The system switches to fallback planning mode.
- The rule-based tools still generate a course plan.
- The system provides template-based explanations.

**US-11: Review Student Plan**
As an academic advisor, I want to view a student's plan summary, so that I can give suitable academic advice.

**Acceptance Criteria:**
- The advisor can view the recommended semester plan.
- The advisor can view prerequisite warnings.
- The advisor can view graduation progress summary.

**US-12: Update Course Data**
As an academic staff member, I want to update course and prerequisite data, so that the system can generate accurate course plans.

**Acceptance Criteria:**
- Academic staff can update course data.
- Academic staff can update prerequisite rules.
- The updated data is used by the planning tools.

**US-13: Log Agent Tool Calls**
As a system admin, I want the system to log agent tool calls, so that planning results can be reviewed and debugged.

**Acceptance Criteria:**
- The system records each agent run.
- The system records tool names and tool results.
- The system records provider errors and fallback actions.

## 5. MVP Scope

**Must have**
- Student Profile Management
- Academic Record Management
- LLM Planning Agent
- Course Catalog Tool
- Prerequisite Checker Tool
- Graduation Progress Tracker
- Semester Plan Generator
- Academic Risk Detector
- AI Explanation and Warning
- Fallback Planning Mode

**Should have**
- Advisor Plan Review View
- Course Data Management
- Agent Run Log
- MCP-compatible Tool Interface

**Could have**
- Full MCP server
- Multi-semester simulation
- Advisor comment workflow
- Full admin dashboard

**Out of Scope**
- Official course registration
- Real-time university system integration
- Automatic transcript synchronization
