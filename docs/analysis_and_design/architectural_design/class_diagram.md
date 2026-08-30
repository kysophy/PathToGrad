# Class Diagram

## 1.2 Overview
The class diagram describes the main object classes of PathToGrad, their responsibilities, and their relationships. To improve readability, the class model is divided into three diagrams:

1.  **Academic Domain:** Includes academic structure, student profiles, Academic Records, course attempts, courses, curricula, and academic terms.
2.  **Course Offerings and Timetables:** Presents course offerings, class sections, weekly timetable data, study plans, plan items, advisor reviews, and agent execution records.
3.  **LLM Agent and Planning Tools:** Presents the LLM Planning Agent, the tool registry, the common planning-tool interface, deterministic planning tools, fallback planning, logging, advisor review, and plan-version services. The LLM Planning Agent coordinates the planning workflow but does not calculate academic rules directly. Prerequisite checking, graduation progress, timetable conflicts, and academic risks are handled by deterministic tools.

*(Insert Class Diagrams Here)*