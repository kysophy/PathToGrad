# Data Specifications

## User Management & Profiles

### 1. USERS
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier (UUID) for the user. |
| `full_name` | NVARCHAR(50) | NOT NULL | Full name of the user. |
| `email` | NVARCHAR(50) | NOT NULL | Contact email of the user. |
| `password` | VARCHAR(255) | NOT NULL | Securely hashed representation of the user's password. |
| `role` | ENUM | NOT NULL | Restricted to 'Student', 'Advisor', or 'Admin'. |
| `account_status` | ENUM | NOT NULL | The current login permission state of the account. Restricted to 'Active' or 'Suspended'. |

### 2. STUDENT_PROFILE
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `student_id` | VARCHAR(20) | PRIMARY KEY, NOT NULL | The official university student ID string. |
| `user_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the USER table. |
| `intake_year` | INT | NOT NULL, > 1900 | The year the student enrolled. |
| `current_semester` | INT | NOT NULL, > 0 | The current study semester number. |
| `target_credit_load` | INT | NOT NULL, >= 14, <= 24 | Expected semester credit load. |
| `program_id` | VARCHAR(36) | NULL | Links to a specific academic program (optional if incomplete). |

## Academic Hierarchy & Curriculum

### 3. FACULTY
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `faculty_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the university faculty/school. |
| `name` | VARCHAR(255) | NOT NULL | Name of the faculty (e.g., Faculty of Information Technology). |

### 4. PROGRAM_TRACK
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `track_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the track. |
| `name` | VARCHAR(255) | NOT NULL | Name of the track (e.g., Standard, High-Quality, Honors). |

### 5. ACADEMIC_PROGRAM
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `program_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the specific major/program. |
| `faculty_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the FACULTY table. |
| `track_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the PROGRAM_TRACK table. |
| `name` | VARCHAR(255) | NOT NULL | Name of the program (e.g., Software Engineering). |

### 6. CURRICULUM
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `curriculum_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the curriculum rule set. |
| `program_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the ACADEMIC_PROGRAM. |
| `version` | VARCHAR(50) | NOT NULL | The specific catalog year (e.g., "2024-2025"). |
| `required_credits` | INT | NOT NULL, > 0 | Total credits required to graduate under this version. |

### 7. CURRICULUM_COURSE
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `curr_course_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier mapping a course to a curriculum. |
| `curriculum_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the CURRICULUM. |
| `course_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the COURSE table. |
| `requirement_type` | ENUM | NOT NULL | Restricted to 'Core' (compulsory) or 'Elective'. |

### 8. COURSE
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `course_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Internal unique system identifier. |
| `course_code` | VARCHAR(15) | UNIQUE, NOT NULL | Official university code (e.g., CSC10001). |
| `course_name` | VARCHAR(255) | NOT NULL | The full descriptive name of the course. |
| `credits` | INT | NOT NULL, > 0 | The credit weight of the course. |
| `status` | ENUM | NOT NULL | Restricted to 'Active' or 'Archived'. |

### 9. PREREQUISITE
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `prereq_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the prerequisite rule. |
| `course_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | The target course a student wants to take. |
| `required_course_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | The course that must be passed first. |

## Temporal & Scheduling

### 10. ACADEMIC_TERM
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `term_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the semester. |
| `name` | VARCHAR(100) | NOT NULL | Human-readable name (e.g., "Fall 2026"). |
| `start_date` | DATE | NOT NULL | The official first day of classes. |
| `end_date` | DATE | NOT NULL | The official last day of final exams. |

### 11. COURSE_OFFERING
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `offering_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for this specific offering. |
| `course_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the base COURSE. |
| `term_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the ACADEMIC_TERM. |
| `status` | ENUM | NOT NULL | Restricted to 'Active', 'Canceled', or 'Archived'. |

### 12. CLASS_SECTION
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `section_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the specific section. |
| `offering_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the specific COURSE_OFFERING for that term. |
| `section_code` | VARCHAR(20) | NOT NULL | The class grouping code (e.g., "Group 1"). |
| `capacity` | INT | NOT NULL, >= 0 | Maximum number of allowable students. |

### 13. SECTION_MEETING
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `meeting_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the time block. |
| `section_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the CLASS_SECTION (e.g., Group 1). |
| `day_of_week` | ENUM | NOT NULL | 'Monday', 'Tuesday', 'Wednesday', etc. |
| `start_time` | TIME | NOT NULL | The exact minute the class begins. |
| `end_time` | TIME | NOT NULL | The exact minute the class ends. |

## Academic Records

### 14. ACADEMIC_RECORD
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `record_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the transcript container. |
| `student_id` | VARCHAR(20) | FOREIGN KEY, UNIQUE, NOT NULL | Links to STUDENT_PROFILE. Enforces a strict 1:1 relationship. |
| `updated_at` | DATETIME | NOT NULL | Timestamp of the last time a grade or attempt was added. |

### 15. COURSE_ATTEMPT
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `attempt_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for this specific attempt. |
| `record_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the student's ACADEMIC_RECORD. |
| `course_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the COURSE taken. |
| `term_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the ACADEMIC_TERM (e.g., Spring 2026). |
| `attempt_number` | INT | NOT NULL, >= 1 | Tracks if this is a first try or a retake. |
| `grade` | DECIMAL(3,1) | NULL | Result grade (NULL if the term is currently in progress). |
| `result_status` | ENUM | NOT NULL | Restricted to 'Passed', 'Failed', or 'InProgress'. |
| `credits_earned` | INT | NOT NULL, >= 0 | Credits gained (0 if failed/in progress). |

## Study Planning & Review

### 16. STUDY_PLAN
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `plan_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the plan version. |
| `student_id` | VARCHAR(20) | FOREIGN KEY, NOT NULL | Links to the requesting student. |
| `version_number` | INT | NOT NULL, >= 1 | Tracks the revision iteration of the plan. |
| `status` | ENUM | NOT NULL | Restricted to 'Draft', 'PendingReview', 'Approved', 'NeedsRevision', or 'Superseded'. |
| `target_credit_load` | INT | NOT NULL | The initial credit limit requested by the student. |
| `total_credits` | INT | NOT NULL | The total credits represented by this plan's items. |

### 17. STUDY_PLAN_ITEM
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `item_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the plan item. |
| `plan_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to STUDY_PLAN. |
| `section_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the scheduled CLASS_SECTION. |

### 18. PLAN_REVIEW
| Attribute Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `review_id` | VARCHAR(36) | PRIMARY KEY, NOT NULL | Unique identifier for the review event. |
| `plan_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the submitted STUDY_PLAN. |
| `advisor_id` | VARCHAR(36) | FOREIGN KEY, NOT NULL | Links to the USER table (Advisor role). |
| `decision` | ENUM | NOT NULL | Restricted to 'Approved' or 'NeedsRevision'. |
| `comment` | TEXT | NULL | Advisor's written feedback. (Enforced as required in the logic layer if the decision is 'NeedsRevision'). |
| `reviewed_at` | DATETIME | NOT NULL | The exact server timestamp of when the review was submitted. |