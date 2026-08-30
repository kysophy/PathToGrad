# Functional Requirements Specification

## Purpose

This document specifies the functional requirements for the PathToGrad course planning system, grouped by feature area. Each requirement is identified with an FR-XX ID.

## FR-S1: Student Data Management
- **FR-01:** The system shall allow students to create and update their academic profile.
- **FR-02:** The system shall allow students to enter completed courses, failed courses, grades, and credits.

## FR-S2: LLM Planning Agent and Tool Interface
- **FR-03:** The system shall allow students to send planning requests to the LLM Planning Agent.
- **FR-04:** The system shall allow the LLM Planning Agent to call internal tools through APIs.
- **FR-05:** The system shall provide an MCP-compatible tool interface with structured tool inputs and outputs.

## FR-S3: Course Data and Academic Checking
- **FR-06:** The system shall retrieve course data from MySQL.
- **FR-07:** The system shall check whether a student satisfies prerequisite rules.
- **FR-08:** The system shall calculate graduation progress.

## FR-S4: Study Plan Generation and Explanation
- **FR-09:** The system shall generate a recommended semester plan.
- **FR-10:** The system shall detect academic risks in a study plan.
- **FR-11:** The system shall explain the recommended plan in clear language.
- **FR-12:** The system shall show warnings when a plan contains academic risks.
- **FR-13:** The system shall provide fallback planning mode when the LLM provider is unavailable.
- **FR-14:** The system shall generate template-based explanations in fallback mode.

## FR-S5: Advisor, Admin, and Traceability
- **FR-15:** The system shall allow academic advisors to view plan summaries and warnings.
- **FR-16:** The system shall allow academic staff or admin users to update course and prerequisite data.
- **FR-17:** The system shall record agent runs, tool calls, provider errors, and fallback actions.