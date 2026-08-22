"""C-03: uniqueness on study plans and plan items.

`study_plan` had no unique on (student_id, term_id, version_number), so
nothing stopped two rows from claiming the same version of the same
student's plan for the same term. `study_plan_item` had no unique at
all, so the same section could be added to a plan twice.

`study_plan_item` stores `section_id`, not `course_id`, so course-level
uniqueness would need a denormalized column and a repository change —
out of scope for this migration per the checklist's own note. We take
the documented weaker stand-in instead: unique (plan_id, section_id).
That does not stop two sections of the *same course* landing in one
plan; the engine (A-16) must not pick two sections of the same course
for a single student in a single plan, and that invariant lives in
code, not the schema.
"""

from alembic import op


revision = "003_add_plan_uniques"
down_revision = "002_proofreading_fixes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_study_plan_student_term_version",
        "study_plan",
        ["student_id", "term_id", "version_number"],
    )
    op.create_unique_constraint(
        "uq_study_plan_item_plan_section",
        "study_plan_item",
        ["plan_id", "section_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_study_plan_item_plan_section",
        "study_plan_item",
        type_="unique",
    )
    op.drop_constraint(
        "uq_study_plan_student_term_version",
        "study_plan",
        type_="unique",
    )
