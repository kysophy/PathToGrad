"""Numeric conventions for A-18 that the spec left unnamed.

Recorded in docs/DECISIONS.md as well. Change both if the team picks different numbers.
"""

GPA_WARNING_THRESHOLD = 5.0
NEAR_GRADUATION_SEMESTER = 7
BACKLOG_STALE_SEMESTERS = 2

# Substring on GeneratedPlan.warnings — A-18 only fires LOAD_UNDER_MIN /
# COURSE_COUNT_UNDER_MIN when the generator actually emptied the pool.
ELECTIVE_POOL_EXHAUSTED = "after the elective pool was exhausted"
