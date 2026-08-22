# Problem Statement

## 2.1 Introduction
To graduate, students must finish a sequence of courses scattered throughout every semester over four years. Manually arranging schedules using scattered PDF files, websites, disjointed catalogs, and spreadsheets is prone to human error. This sometimes leads to delayed graduation timelines, which places an unnecessary financial burden on students and negatively impacts the university's graduation rate. The objective of this software is to build a centralized platform utilizing an LLM to check academic history, calculate course results, and recommend appropriate course plans.

## 2.2 Operating Environment
*   **Client Interface:** Accessed via web browsers using React, Vite, and TypeScript.
*   **Server Environment:** Python and FastAPI backend hosted on a standard cloud-based server capable of handling high access.
*   **Future Enhancement:** Designed to support future secure, read-only integration with the university Registrar and Student Information Systems.

## 2.3 Design & Implementation Constraints
*   **Technical:** Python backend for complex scheduling logic and MySQL to safely store course and student records.
*   **Data:** Logic must follow existing university rules and cannot allow students to register for plans that conflict with constraints.
*   **LLM/AI:** Relies on OpenAI/Gemini API.