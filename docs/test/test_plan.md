# Software Test Plan - PathToGrad

## 1. Introduction & Objectives
The objective of this test plan is to define the testing strategy, tools, scope, and execution framework for PathToGrad. The testing lifecycle ensures all 17 Functional Requirements and 9 Non-Functional Requirements are verified without regression.

## 2. Testing Techniques & Strategy

### 2.1 Unit Testing (White-Box)
* **Scope:** Applied strictly to the Core Logic Layer's Rule-Based Python Engine.
* **Focus:** Validates deterministic algorithms independently of the LLM:
  * **Prerequisite Checker DAG:** Directed Acyclic Graph traversal to detect satisfied, missing, and circular prerequisites.
  * **Course Scheduling Engine:** Credit load boundary verification (14–24 credits), section meeting conflict detection, and failed course retake prioritization.
  * **Graduation Progress Tracker:** Accurate calculation of earned credits and missing required curriculum items.

### 2.2 Integration Testing (White-Box & Black-Box)
* **Scope:** Focuses on the Web Router Layer (FastAPI API Gateway) and Orchestration Layer.
* **Focus:**
  * **Active Routing Protocol:** Validates automatic detection of external AI provider timeouts/errors and seamless rerouting of requests to the Fallback Plan Controller.
  * **MCP Interface:** Verifies structured JSON tool call invocation (`callTool`) and parameter validation between the LLM Planning Agent and internal deterministic tools.
  * **Database ORM:** Verifies data integrity during CRUD operations across MySQL tables.

### 2.3 System Testing (Black-Box)
* **Scope:** End-to-end functional testing via the React SPA Client.
* **Focus:** Full operational lifecycle across all core use cases:
  * **U001:** Student profile creation and updates.
  * **U002:** Academic record ingestion and grade tracking.
  * **U003:** Semester plan generation, risk display, and visual 7-day schedule rendering.
  * **U004:** Advisor dashboard triage, review feedback, and status transitions.
  * **U005:** Administrative CSV catalog import and validation.

### 2.4 Security & Access Control Testing
* **Scope:** Role-Based Access Control (RBAC).
* **Focus:** Ensures that endpoints and UI routes are strictly isolated between `Student`, `Advisor`, and `Admin` roles. Confirms that LLM agents possess no direct database access credentials.

## 3. Testing Objects & Environment

| Component | Target Artifacts | Environment / Tools |
| :--- | :--- | :--- |
| **Frontend Client** | React SPA, Chat Workspace UI, 7-Day Calendar, Profile Forms, Advisor Portals. | Google Chrome, Firefox, Vitest, Playwright. |
| **Backend Services** | FastAPI Application Gateway, MCP Tool Interface, Fallback Controller, REST APIs. | Python `pytest`, Postman, Docker. |
| **Database** | MySQL Relational Database schemas, foreign keys, triggers, constraints. | MySQL Server test instance, seed test fixtures. |

## 4. Test Data Definitions (Fixtures)

| Test Data ID | Description |
| :--- | :--- |
| `TD-PROFILE-VALID` | Complete student profile with valid program, intake year, semester, and target credits (14–24). |
| `TD-PROFILE-INCOMPLETE` | Profile data missing one mandatory field. |
| `TD-CURRICULUM` | Test curriculum fixture defining standard required credit totals and mandatory course rules. |
| `TD-COURSE-BASE` | Valid catalog course with zero prerequisite dependencies. |
| `TD-COURSE-DEPENDENT` | Valid catalog course explicitly requiring `TD-COURSE-BASE`. |
| `TD-ATTEMPT-PASSED` | Verified Passed attempt record with grade >= 5.0 and earned credits. |
| `TD-ATTEMPT-FAILED` | Failed attempt record with grade < 5.0 and 0 earned credits. |
| `TD-ATTEMPT-INPROGRESS` | Currently ongoing course attempt with NULL grade and 0 earned credits. |
| `TD-TERM-TARGET` | The academic semester designated for study plan generation. |
| `TD-OFFERING-AVAILABLE` | Course offering in target term with at least one available section and meeting time. |
| `TD-OFFERING-MISSING` | Course offering with no scheduled sections in the selected term. |