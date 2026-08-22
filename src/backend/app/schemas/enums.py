"""Shared enumerations for Seam 1 (models, API schemas, tool results).

Part 3 `app.deterministic.types` should re-export these rather than
redefining the strings.
"""

from enum import Enum


class UserRole(str, Enum):
    STUDENT = "Student"
    ADVISOR = "Advisor"
    ADMIN = "Admin"


class AccountStatus(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"


class CourseStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class RequirementType(str, Enum):
    CORE = "Core"
    ELECTIVE = "Elective"


class TermType(str, Enum):
    SEMESTER_1 = "Semester1"
    SEMESTER_2 = "Semester2"
    SUMMER = "Summer"


class OfferingStatus(str, Enum):
    ACTIVE = "Active"
    CANCELED = "Canceled"
    ARCHIVED = "Archived"


class SectionStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ARCHIVED = "Archived"


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class MeetingType(str, Enum):
    LT = "LT"
    TH = "TH"


class ResultStatus(str, Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    IN_PROGRESS = "InProgress"


class PlanStatus(str, Enum):
    DRAFT = "Draft"
    PENDING_REVIEW = "PendingReview"
    APPROVED = "Approved"
    NEEDS_REVISION = "NeedsRevision"
    SUPERSEDED = "Superseded"


class GenerationMode(str, Enum):
    LLM = "LLM"
    FALLBACK = "Fallback"


class ReviewDecision(str, Enum):
    APPROVED = "Approved"
    NEEDS_REVISION = "NeedsRevision"


class AgentRunStatus(str, Enum):
    STARTED = "Started"
    COMPLETED = "Completed"
    FAILED = "Failed"
    FALLBACK = "Fallback"


class SelectionReason(str, Enum):
    ASSIGNED_THIS_SEMESTER = "ASSIGNED_THIS_SEMESTER"
    BACKLOG_FROM_SEMESTER_N = "BACKLOG_FROM_SEMESTER_N"
    ELECTIVE_FILL = "ELECTIVE_FILL"
    RETAKE_AFTER_FAIL = "RETAKE_AFTER_FAIL"
    RETAKE_IMPROVEMENT = "RETAKE_IMPROVEMENT"


class ExclusionReason(str, Enum):
    DEFERRED_CREDIT_CAP = "DEFERRED_CREDIT_CAP"
    DROPPED_PREREQ_BLOCKED = "DROPPED_PREREQ_BLOCKED"
    DROPPED_NOT_OFFERED = "DROPPED_NOT_OFFERED"
    DROPPED_ALL_SECTIONS_CONFLICT = "DROPPED_ALL_SECTIONS_CONFLICT"


class RiskSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    INFO = "info"


class RiskCode(str, Enum):
    NO_RETAKE_REMAINING = "NO_RETAKE_REMAINING"
    PREREQ_BLOCKED = "PREREQ_BLOCKED"
    ASSIGNED_OVER_CAP = "ASSIGNED_OVER_CAP"
    COURSE_NOT_OFFERED = "COURSE_NOT_OFFERED"
    FAILED_UNRETAKEN_LATE = "FAILED_UNRETAKEN_LATE"
    LOAD_OVER_CAP = "LOAD_OVER_CAP"
    BACKLOG_STALE = "BACKLOG_STALE"
    TIMETABLE_CONFLICT = "TIMETABLE_CONFLICT"
    GPA_BELOW_THRESHOLD = "GPA_BELOW_THRESHOLD"
    LOAD_UNDER_MIN = "LOAD_UNDER_MIN"
    COURSE_COUNT_UNDER_MIN = "COURSE_COUNT_UNDER_MIN"
    SPECIALIZATION_NOT_SET = "SPECIALIZATION_NOT_SET"
    RETAKE_REPLACES_GRADE = "RETAKE_REPLACES_GRADE"


RISK_SEVERITY: dict[RiskCode, RiskSeverity] = {
    RiskCode.NO_RETAKE_REMAINING: RiskSeverity.CRITICAL,
    RiskCode.PREREQ_BLOCKED: RiskSeverity.HIGH,
    RiskCode.ASSIGNED_OVER_CAP: RiskSeverity.HIGH,
    RiskCode.COURSE_NOT_OFFERED: RiskSeverity.HIGH,
    RiskCode.FAILED_UNRETAKEN_LATE: RiskSeverity.HIGH,
    RiskCode.LOAD_OVER_CAP: RiskSeverity.HIGH,
    RiskCode.BACKLOG_STALE: RiskSeverity.MEDIUM,
    RiskCode.TIMETABLE_CONFLICT: RiskSeverity.MEDIUM,
    RiskCode.GPA_BELOW_THRESHOLD: RiskSeverity.MEDIUM,
    RiskCode.LOAD_UNDER_MIN: RiskSeverity.MEDIUM,
    RiskCode.COURSE_COUNT_UNDER_MIN: RiskSeverity.MEDIUM,
    RiskCode.SPECIALIZATION_NOT_SET: RiskSeverity.MEDIUM,
    RiskCode.RETAKE_REPLACES_GRADE: RiskSeverity.INFO,
}


class ToolStatus(str, Enum):
    OK = "ok"
    WARNING = "warning"
    UNCERTAIN = "uncertain"


class CoursePrimaryStatus(str, Enum):
    ASSIGNED = "Assigned"
    BACKLOG = "Backlog"
    RETAKE = "Retake"
    ELECTIVE = "Elective"
    FUTURE = "Future"
