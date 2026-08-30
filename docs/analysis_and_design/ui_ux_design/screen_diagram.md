# Screen Diagram

## 1. Overview
The screen flow describes the navigation pathways across PathToGrad for each user role: Student, Academic Advisor, and Academic Staff/Admin.

                +-------------------------+
                |     SCR-01: Log In      |
                +-------------------------+
                   /          |          \
        (Student) /  (Advisor)|           \ (Admin)
                 v            v            v
+-----------------------+  +----------------------+  +-------------------------+
| SCR-02: Student's     |  | SCR-08: Student Plans|  | SCR-10: Course Data     |
| Dashboard             |  | Dashboard            |  | Management Interface    |
+-----------------------+  +----------------------+  +-------------------------+
   |    |    |                     |                               |
   |    |    +--> SCR-05: Course   | Select a student's plan       | Import CSV / Update
   |    |         Catalog          v                               v
   |    |                  +----------------------+  +-------------------------+
   |    +-------> SCR-06:  | SCR-09: Advisor Plan |  | SCR-10A: CSV Validation |
   |              Study    | Review               |  | and Preview             |
   |              Plan     +----------------------+  +-------------------------+
   |                |                                              |
   |                v                                              v
   |         +-------------+                         +-------------------------+
   |         | SCR-07: Plan|                         | SCR-11: Agent & Import  |
   |         | History     |                         | Logs                    |
   |         +-------------+                         +-------------------------+
   v
+-----------------------+
| SCR-03: Manage        |
| Academic Profile      |
+-----------------------+