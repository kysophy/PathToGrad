# Conceptual Model

## 2.1 Overview
The conceptual model presents the main semantic entities of PathToGrad and their relationships. The model covers user access, academic structure, student Academic Records, curriculum rules, course offerings, weekly timetables, study plans, advisor reviews, and agent traceability. 

*   A **Student Profile** is linked to an Academic Program and a Curriculum. 
*   The student's **Academic Record** contains Course Attempts used for prerequisite checking and graduation-progress calculation. 
*   **Course Offerings**, **Class Sections**, and **Section Meetings** provide the schedule data required to generate a weekly timetable.

## 2.2 Study Plan & Reviews
A generated **Study Plan** is stored as a versioned record. A new plan is saved as Draft and may be submitted for advisor review. 
*   The advisor may approve the plan or request revision and provide a comment. 
*   When revision is requested, the student creates a new plan version while the earlier plan and review record remain unchanged. 

Advisor approval provides academic planning guidance only and does not perform official course registration. The LLM Planning Agent coordinates internal tools, while prerequisite checks, timetable conflicts, graduation progress, and review records are based on structured system data.