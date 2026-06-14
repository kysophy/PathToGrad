Feature Specification - PathToGrad Course Planning System

1. Purpose

   This document defines the main system features of PathToGrad.
   PathToGrad is designed as an LLM-powered course planning system. The LLM Planning Agent is the main interaction layer. It receives student requests, calls internal tools, checks academic rules, and explains the final plan.
   The system also includes fallback planning mode. If the LLM provider is unavailable, the system can still use rule-based tools to generate a valid plan.

2. System Direction

   PathToGrad is not only a web app with AI explanation. The main workflow is controlled by the LLM Planning Agent.
   The agent can call system tools through APIs and an MCP-compatible tool interface. These tools use structured data from MySQL, including student profiles, academic records, courses, prerequisites, and graduation requirements.
   The LLM does not recommend courses from general knowledge only. Each plan must be checked by rule-based tools before being shown to the student.
   If the LLM provider fails, the system switches to fallback planning mode. In this mode, the core planning tools still work, and the system returns template-based explanations.

3. Stakeholder Feature Mapping

   Student:
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
  
   Academic Advisor:
   - Advisor Plan Review View
   - Advisor Summary Skill
  
   Academic Staff / Admin:
   - Course Data Management
   - Course Data Import API
   - Agent Run Log
  
   LLM Planning Agent:
   - API Layer
   - MCP-compatible Tool Interface
   - Planning Skills

4. Main Features

   F-01: Student Profile Management
   Allows students to create and update their academic profile, including major, intake year, current semester, and target credit load.
  
   F-02: Academic Record Management
   Allows students to enter completed courses, failed courses, grades, and credits. This data is used by the planning agent and internal tools.
  
   F-03: LLM Planning Agent
   Acts as the main interaction layer of the system. It receives student requests, decides which tools to use, calls APIs, and explains the final planning result.
  
   F-04: Course Catalog Tool
   Retrieves course information from MySQL, including course code, course name, credits, suggested semester, and prerequisites.
  
   F-05: Prerequisite Checker Tool
   Checks whether a student has completed the required prerequisite courses before a course is recommended.
  
   F-06: Graduation Progress Tracker
   Calculates completed credits, remaining credits, completed required courses, and missing required courses.
  
   F-07: Semester Plan Generator
   Suggests suitable courses for the next semester based on academic record, prerequisite rules, target credit load, and graduation requirements.
  
   F-08: Academic Risk Detector
   Detects possible risks, such as missing prerequisites, overloaded semester plans, delayed required courses, or missing graduation requirements.
  
   F-09: AI Explanation and Warning
   Explains why each course is recommended and shows warnings in clear language.
  
   F-10: Fallback Planning Mode
   Allows the system to continue core planning functions when the LLM provider is unavailable. It uses rule-based tools and template-based explanations.
  
   F-11: Advisor Plan Review View
   Allows academic advisors to view a student’s semester plan, prerequisite warnings, and graduation progress summary.
  
   F-12: Course Data Management
   Allows academic staff or admin users to maintain course information and prerequisite rules through MySQL seed scripts, CSV import, or admin APIs.
  
   F-13: API Layer
   Provides backend endpoints for student data, course data, planning requests, tool calls, advisor view, and admin data updates.
  
   F-14: MCP-compatible Tool Interface
   Defines structured tool names, inputs, and outputs so that the LLM Planning Agent can call tools in a clear and consistent way.
  
   F-15: Planning Skills
   Provides reusable workflows for common planning tasks, including Plan Next Semester, Validate Study Plan, Review Graduation Progress, and Advisor Summary.
  
   F-16: Agent Run Log
   Stores agent runs, tool calls, provider errors, and fallback actions for review and debugging.

5. Tools, APIs, MCP-compatible Interface, and Skills

   Tools:
   - Course Catalog Tool
   - Prerequisite Checker Tool
   - Graduation Progress Tracker
   - Semester Plan Generator
   - Academic Risk Detector
  
   APIs:
   - Student API
   - Course API
   - Agent API
   - Tool API
   - Advisor API
   - Admin API
  
   MCP-compatible Interface:
  
   - Standard tool names
   - Standard input format
   - Standard output format
   - Tool call status
  
   Skills:
   - Plan Next Semester
   - Validate Study Plan
   - Review Graduation Progress
   - Advisor Summary

6. Functional Requirements

   FR-01: The system shall allow students to create and update their academic profile.
   FR-02: The system shall allow students to enter completed courses, failed courses, grades, and credits.
   FR-03: The system shall allow students to send planning requests to the LLM Planning Agent.
   FR-04: The system shall allow the LLM Planning Agent to call internal tools through APIs.
   FR-05: The system shall provide an MCP-compatible tool interface with structured tool inputs and outputs.
   FR-06: The system shall retrieve course data from MySQL.
   FR-07: The system shall check whether a student satisfies prerequisite rules.
   FR-08: The system shall calculate graduation progress.
   FR-09: The system shall generate a recommended semester plan.
   FR-10: The system shall detect academic risks in a study plan.
   FR-11: The system shall explain the recommended plan in clear language.
   FR-12: The system shall show warnings when a plan contains academic risks.
   FR-13: The system shall provide fallback planning mode when the LLM provider is unavailable.
   FR-14: The system shall generate template-based explanations in fallback mode.
   FR-15: The system shall allow academic advisors to view plan summaries and warnings.
   FR-16: The system shall allow academic staff or admin users to update course and prerequisite data.
   FR-17: The system shall record agent runs, tool calls, provider errors, and fallback actions.

7. Non-functional Requirements

   NFR-01: The system should be accessible through modern web browsers.
   NFR-02: The system should present planning results in clear and simple language.
   NFR-03: The system should protect student academic information.
   NFR-04: The system should restrict access based on user roles.
   NFR-05: The system should store course, prerequisite, student, and academic record data in MySQL.
   NFR-06: The system should continue core planning functions when the LLM provider is unavailable.
   NFR-07: The system should verify LLM-generated recommendations using rule-based tools.
   NFR-08: The system should show clear warnings when data is missing, outdated, or uncertain.
   NFR-09: The system should log important agent actions and tool calls for traceability.

8. Constraints

   The system depends on available course data, prerequisite rules, academic records, and curriculum requirements. In the current version, the data may be prepared manually or imported from CSV/MySQL seed scripts.
   The system recommendations are based on the available data in the database. If some course data, prerequisite rules, or curriculum requirements are missing or uncertain, the system should show warnings to users.
   The LLM Planning Agent must not recommend courses from unsupported general knowledge. All course recommendations must be checked by internal rule-based tools before being shown to the student.
   The system may use one LLM provider, such as OpenAI API or Gemini API. If the LLM provider is unavailable, the system should switch to fallback planning mode and continue to provide rule-based planning results.
   In fallback planning mode, the system will not generate AI explanations. Instead, it will use template-based explanations based on tool results.
   The system supports academic planning only. Official course registration is outside the current scope.
   The MCP-compatible interface defines how the LLM calls internal tools. A full external MCP server can be added in a later version.
   Course data can be managed through MySQL seed scripts, CSV import, or admin APIs.
   Real-time integration with the university registrar system is considered a future enhancement.

9. Future Enhancements

   Future versions may include:
   - Full MCP server
   - Real-time integration with university systems
   - Automatic transcript synchronization
   - Advisor approval workflow
   - Full admin dashboard
   - Multi-semester graduation simulation
   - Official course registration support
