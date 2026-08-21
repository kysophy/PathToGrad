# Screen Specifications

## 1. SCR-01: Log In (Sign In and Role Access)
* **Screen ID:** SCR-01
* **Target Role:** Student, Academic Advisor, Academic Staff/Admin
* **Related Requirements:** NFR-03, NFR-04, FR-01
* **Purpose:** Authenticates system users and routes them to their respective role-based workspaces.
* **Design Concept:** Stylized as a notebook cover with an interactive nametag login field. Includes a role selector dropdown (`Student`, `Advisor`, `Admin`), username/ID and password input fields, a "Forgot Password" link, and a submit navigation button.

## 2. SCR-02: Student's Dashboard
* **Screen ID:** SCR-02
* **Target Role:** Student
* **Related Requirements:** FR-08, FR-12, NFR-02
* **Purpose:** Acts as the primary student dashboard offering a centralized overview of academic status and immediate access to planning tools.
* **Components & Layout:**
  * **Header:** University branding logo (returns to dashboard), navigation links to Course Catalog, Study Plan, notifications bell, profile icon, and light/dark theme toggle.
  * **Left Workspace:** Information dashboard containing total earned credits, cumulative GPA card, academic risk alert banner, graduation progress gauge (%), latest study plan status (%), upcoming assignments/deadlines list, and an advisor feedback sticky note.
  * **Right Workspace:** Fixed split-screen AI Chatbox allowing conversational academic queries and rapid planning assistance.

## 3. SCR-03: Manage Academic Profile
* **Screen ID:** SCR-03
* **Target Role:** Student
* **Related Requirements:** U001, FR-01, NFR-03, NFR-04
* **Purpose:** Enables students to establish and maintain their baseline academic attributes used for curriculum matching and semester planning.
* **Components & Layout:** Clean input card featuring user full name, official Student ID, email address, Major/Program dropdown, Program Track selector, Intake Year field, Current Semester number, and Target Credit Load input (enforcing bounds: 14–24 credits). Includes a prominent "Save Profile" submission button.

## 4. SCR-04: Manage Academic Record
* **Screen ID:** SCR-04
* **Target Role:** Student
* **Related Requirements:** U002, FR-02, FR-07, FR-08
* **Purpose:** Allows students to log and maintain course attempts, grades, and completed credits to build the transcript utilized for prerequisite checking.
* **Components & Layout:** Accumulated credit progress bar across the top. "Quick Add Course" form containing Course Code selector, Academic Term dropdown, Grade input, and Credit value. Dual-tab data table separating "Completed Courses" (Passed) from "Failed / In-Progress Courses" with inline edit/delete controls and prerequisite warning tooltips.

## 5. SCR-05: Course Catalog
* **Screen ID:** SCR-05
* **Target Role:** Student
* **Related Requirements:** FR-06, FR-07
* **Purpose:** Read-only inspection interface for exploring course metadata, prerequisites, and current term offering schedules.
* **Components & Layout:** Search bar with dynamic semester and academic department filters. Course card deck displaying course code, descriptive name, credit weight, prerequisite chain, and eligibility status tags ("Can register", "Unavailable"). Clicking a card reveals modal details including section schedules, class capacity, and assigned instructors.

## 6. SCR-06: Study Plan Generator
* **Screen ID:** SCR-06
* **Target Role:** Student
* **Related Requirements:** U003, FR-03–FR-14, NFR-06, NFR-07
* **Purpose:** Interactive workspace where students request semester schedules and inspect AI-recommended or deterministic fallback course selections.
* **Components & Layout:**
  * **Planning Controls:** Target semester selector, target credit load selector, optional natural-language preferences text box, and a "Generate Plan" action button.
  * **AI Recommendation Card:** Displays reasoning for suggested courses, graduation progress delta, and highlighted yellow risk warning banners.
  * **7-Day Timetable:** Interactive visual calendar displaying non-conflicting Theory (LT) and Lab (TH) time slots.
  * **Actions:** "Save as Draft" button, "Submit for Review" button, and link to Plan History.

## 7. SCR-07: Plan History & Advisor Feedback
* **Screen ID:** SCR-07
* **Target Role:** Student
* **Related Requirements:** FR-23, U003, U004
* **Purpose:** Version repository allowing students to inspect historical plan iterations and attached advisor review outcomes.
* **Components & Layout:** Sorting filters by creation date, semester, credits, and lifecycle status (`Draft`, `PendingReview`, `Approved`, `Needs Revision`). List of historical plan cards displaying timestamp, total credits, selected course list, advisor feedback text box, and "Create Revision" trigger.

## 8. SCR-08: Student Plans Dashboard (Advisor Portal)
* **Screen ID:** SCR-08
* **Target Role:** Academic Advisor
* **Related Requirements:** U004, FR-15
* **Purpose:** Centralized queue for academic advisors to locate and triage submitted student study plans.
* **Components & Layout:** Vertical list of students awaiting plan evaluation. Color-coded status badges: Green (low risk / nearly done), Red (high academic risk / low competence / conflicts), and Blue (checked / approved). Search and filtering bar by student ID or major, with an empty state display when no plans are pending.

## 9. SCR-09: Advisor Plan Review
* **Screen ID:** SCR-09
* **Target Role:** Academic Advisor
* **Related Requirements:** U004, FR-15, NFR-06
* **Purpose:** Detailed review console for evaluating a student's proposed semester plan and rendering formal decisions.
* **Components & Layout:** Top summary pane displaying student profile data, cumulative GPA, and AI Risk Analysis breakdown. Lower pane displaying the proposed 7-day timetable. Bottom action bar containing an Advisor Comments text area, a secondary "Request Revision" button, and a primary "Approve Plan" button.

## 10. SCR-10: Course Data Management
* **Screen ID:** SCR-10
* **Target Role:** Academic Staff / Admin
* **Related Requirements:** U005, FR-16
* **Purpose:** Administrative interface for maintaining course metadata and curriculum definitions.
* **Components & Layout:** Master course data table displaying course codes, course names, credit weights, and prerequisite dependencies. Action header featuring a CSV Drag-and-Drop file upload zone labeled "Import Course Catalog CSV", alongside manual "Add Course", "Edit", and "Delete" buttons.

## 11. SCR-10A: CSV Validation & Preview Modal
* **Screen ID:** SCR-10A
* **Target Role:** Academic Staff / Admin
* **Related Requirements:** U005, FR-16, FR-17
* **Purpose:** Pre-commit validation modal preventing circular prerequisite loops or corrupt data from being committed to MySQL.
* **Components & Layout:** Modal report summarizing uploaded filename, total parsed rows, green success indicators for valid rows, and highlighted red error cards flagging detected circular prerequisite dependencies or syntax anomalies. Features "Cancel" and "Commit to Database" buttons (disabled if blocking errors exist).

## 12. SCR-11: Agent & Import Logs
* **Screen ID:** SCR-11
* **Target Role:** Academic Staff / Admin
* **Related Requirements:** FR-17, NFR-09
* **Purpose:** System traceability console for inspecting agent execution logs, tool calls, fallback switches, and database batch imports.
* **Components & Layout:** Searchable and filterable log grid with columns for Timestamp, User/Session ID, Event Type (`Tool Call`, `LLM Provider Error`, `Fallback Activation`, `CSV Import`), Execution Latency, and Expandable JSON Payload Inspector.