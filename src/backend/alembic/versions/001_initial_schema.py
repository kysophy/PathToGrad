from alembic import op
import sqlalchemy as sa


revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.String(36), primary_key=True),
        sa.Column("full_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("Student", "Advisor", "Admin", name="user_role"),
            nullable=False,
        ),
        sa.Column(
            "account_status",
            sa.Enum("Active", "Suspended", name="account_status"),
            nullable=False,
        ),
    )

    op.create_table(
        "faculty",
        sa.Column("faculty_id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
    )

    op.create_table(
        "program_track",
        sa.Column("track_id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("min_credits_per_term", sa.Integer(), nullable=False),
        sa.Column("max_credits_per_term", sa.Integer(), nullable=False),
        sa.Column("min_courses", sa.Integer(), nullable=False),
        sa.Column("max_courses", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "min_credits_per_term > 0",
            name="chk_track_min_credits",
        ),
        sa.CheckConstraint(
            "max_credits_per_term >= min_credits_per_term",
            name="chk_track_max_credits",
        ),
        sa.CheckConstraint(
            "min_courses > 0",
            name="chk_track_min_courses",
        ),
        sa.CheckConstraint(
            "max_courses >= min_courses",
            name="chk_track_max_courses",
        ),
    )

    op.create_table(
        "academic_program",
        sa.Column("program_id", sa.String(36), primary_key=True),
        sa.Column("faculty_id", sa.String(36), nullable=False),
        sa.Column("track_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty.faculty_id"]),
        sa.ForeignKeyConstraint(["track_id"], ["program_track.track_id"]),
    )

    op.create_table(
        "curriculum",
        sa.Column("curriculum_id", sa.String(36), primary_key=True),
        sa.Column("program_id", sa.String(36), nullable=False),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("required_credits", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["academic_program.program_id"],
        ),
        sa.UniqueConstraint(
            "program_id",
            "version",
            name="uq_curriculum_program_version",
        ),
        sa.CheckConstraint(
            "required_credits > 0",
            name="chk_required_credits",
        ),
    )

    op.create_table(
        "class_group",
        sa.Column("class_id", sa.String(36), primary_key=True),
        sa.Column("class_code", sa.String(20), nullable=False),
        sa.Column("program_id", sa.String(36), nullable=False),
        sa.Column("intake_year", sa.Integer(), nullable=False),
        sa.Column("advisor_user_id", sa.String(36), nullable=False),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["academic_program.program_id"],
        ),
        sa.ForeignKeyConstraint(["advisor_user_id"], ["users.user_id"]),
        sa.UniqueConstraint("class_code"),
        sa.CheckConstraint(
            "intake_year > 1900",
            name="chk_class_intake_year",
        ),
    )

    op.create_table(
        "student_profile",
        sa.Column("student_id", sa.String(20), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("intake_year", sa.Integer(), nullable=False),
        sa.Column("current_semester", sa.Integer(), nullable=False),
        sa.Column("target_credit_load", sa.Integer(), nullable=False),
        sa.Column("program_id", sa.String(36), nullable=True),
        sa.Column("spec_code", sa.String(10), nullable=True),
        sa.Column("class_id", sa.String(36), nullable=True),
        sa.Column("curriculum_id", sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["academic_program.program_id"],
        ),
        sa.ForeignKeyConstraint(["class_id"], ["class_group.class_id"]),
        sa.ForeignKeyConstraint(
            ["curriculum_id"],
            ["curriculum.curriculum_id"],
        ),
        sa.UniqueConstraint("user_id"),
        sa.CheckConstraint("intake_year > 1900", name="chk_intake_year"),
        sa.CheckConstraint(
            "current_semester > 0",
            name="chk_current_semester",
        ),
    )

    op.create_table(
        "course",
        sa.Column("course_id", sa.String(36), primary_key=True),
        sa.Column("course_code", sa.String(15), nullable=False),
        sa.Column("name_vi", sa.String(255), nullable=False),
        sa.Column("name_en", sa.String(255), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("Active", "Archived", name="course_status"),
            nullable=False,
        ),
        sa.UniqueConstraint("course_code"),
        sa.CheckConstraint("credits > 0", name="chk_course_credits"),
    )

    op.create_table(
        "academic_term",
        sa.Column("term_id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column(
            "term_type",
            sa.Enum(
                "Semester1",
                "Semester2",
                "Summer",
                name="term_type",
            ),
            nullable=False,
        ),
        sa.Column("term_no", sa.Integer(), nullable=False),
        sa.CheckConstraint("term_no > 0", name="chk_term_no"),
    )

    op.create_table(
        "academic_record",
        sa.Column("record_id", sa.String(36), primary_key=True),
        sa.Column("student_id", sa.String(20), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student_profile.student_id"],
        ),
        sa.UniqueConstraint("student_id"),
    )

    op.create_table(
        "course_attempt",
        sa.Column("attempt_id", sa.String(36), primary_key=True),
        sa.Column("record_id", sa.String(36), nullable=False),
        sa.Column("course_id", sa.String(36), nullable=False),
        sa.Column("term_id", sa.String(36), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("grade", sa.Numeric(3, 1), nullable=True),
        sa.Column(
            "result_status",
            sa.Enum("Passed", "Failed", "InProgress", name="result_status"),
            nullable=False,
        ),
        sa.Column("credits_earned", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["academic_record.record_id"],
        ),
        sa.ForeignKeyConstraint(["course_id"], ["course.course_id"]),
        sa.ForeignKeyConstraint(["term_id"], ["academic_term.term_id"]),
        sa.UniqueConstraint(
            "record_id",
            "course_id",
            "attempt_number",
            name="uq_course_attempt",
        ),
        sa.CheckConstraint(
            "attempt_number IN (1, 2)",
            name="chk_attempt_number",
        ),
        sa.CheckConstraint(
            "credits_earned >= 0",
            name="chk_credits_earned",
        ),
    )

    op.create_table(
        "curriculum_course",
        sa.Column("curr_course_id", sa.String(36), primary_key=True),
        sa.Column("curriculum_id", sa.String(36), nullable=False),
        sa.Column("course_id", sa.String(36), nullable=False),
        sa.Column(
            "requirement_type",
            sa.Enum("Core", "Elective", name="requirement_type"),
            nullable=False,
        ),
        sa.Column("assigned_semester", sa.Integer(), nullable=False),
        sa.Column("spec_code", sa.String(10), nullable=True),
        sa.ForeignKeyConstraint(
            ["curriculum_id"],
            ["curriculum.curriculum_id"],
        ),
        sa.ForeignKeyConstraint(["course_id"], ["course.course_id"]),
        sa.UniqueConstraint(
            "curriculum_id",
            "course_id",
            name="uq_curriculum_course",
        ),
        sa.CheckConstraint(
            "assigned_semester > 0",
            name="chk_assigned_semester",
        ),
    )

    op.create_table(
        "prerequisite",
        sa.Column("prereq_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("course_id", sa.String(36), nullable=False),
        sa.Column("required_course_id", sa.String(36), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["course.course_id"]),
        sa.ForeignKeyConstraint(
            ["required_course_id"],
            ["course.course_id"],
        ),
        sa.UniqueConstraint(
            "course_id",
            "required_course_id",
            name="uq_prerequisite_rule",
        ),
        sa.CheckConstraint(
            "course_id <> required_course_id",
            name="chk_prerequisite_not_self",
        ),
    )

    op.create_table(
        "course_offering",
        sa.Column("offering_id", sa.String(36), primary_key=True),
        sa.Column("course_id", sa.String(36), nullable=False),
        sa.Column("term_id", sa.String(36), nullable=False),
        sa.Column(
            "status",
            sa.Enum("Active", "Canceled", "Archived", name="offering_status"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["course_id"], ["course.course_id"]),
        sa.ForeignKeyConstraint(["term_id"], ["academic_term.term_id"]),
        sa.UniqueConstraint(
            "course_id",
            "term_id",
            name="uq_course_offering",
        ),
    )

    op.create_table(
        "class_section",
        sa.Column("section_id", sa.String(36), primary_key=True),
        sa.Column("offering_id", sa.String(36), nullable=False),
        sa.Column("section_code", sa.String(20), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("Active", "Inactive", "Archived", name="section_status"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["offering_id"],
            ["course_offering.offering_id"],
        ),
        sa.UniqueConstraint(
            "offering_id",
            "section_code",
            name="uq_section_code_per_offering",
        ),
        sa.CheckConstraint("capacity >= 0", name="chk_section_capacity"),
    )

    op.create_table(
        "section_meeting",
        sa.Column("meeting_id", sa.String(36), primary_key=True),
        sa.Column("section_id", sa.String(36), nullable=False),
        sa.Column(
            "meeting_type",
            sa.Enum("LT", "TH", name="meeting_type"),
            nullable=False,
        ),
        sa.Column(
            "day_of_week",
            sa.Enum(
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
                name="day_of_week",
            ),
            nullable=False,
        ),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("room", sa.String(50), nullable=False),
        sa.Column("instructor", sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["class_section.section_id"],
        ),
        sa.CheckConstraint("end_time > start_time", name="chk_meeting_time"),
    )

    op.create_table(
        "study_plan",
        sa.Column("plan_id", sa.String(36), primary_key=True),
        sa.Column("student_id", sa.String(20), nullable=False),
        sa.Column("term_id", sa.String(36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "Draft",
                "PendingReview",
                "Approved",
                "NeedsRevision",
                "Superseded",
                name="plan_status",
            ),
            nullable=False,
        ),
        sa.Column(
            "generation_mode",
            sa.Enum("LLM", "Fallback", name="generation_mode"),
            nullable=False,
        ),
        sa.Column("target_credit_load", sa.Integer(), nullable=False),
        sa.Column("total_credits", sa.Integer(), nullable=False),
        sa.Column("previous_version_id", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student_profile.student_id"],
        ),
        sa.ForeignKeyConstraint(["term_id"], ["academic_term.term_id"]),
        sa.ForeignKeyConstraint(
            ["previous_version_id"],
            ["study_plan.plan_id"],
        ),
        sa.CheckConstraint("version_number >= 1", name="chk_plan_version"),
        sa.CheckConstraint(
            "target_credit_load > 0",
            name="chk_plan_target_credits",
        ),
        sa.CheckConstraint(
            "total_credits >= 0",
            name="chk_plan_total_credits",
        ),
    )

    op.create_table(
        "study_plan_item",
        sa.Column("item_id", sa.String(36), primary_key=True),
        sa.Column("plan_id", sa.String(36), nullable=False),
        sa.Column("section_id", sa.String(36), nullable=False),
        sa.Column(
            "selection_reason",
            sa.Enum(
                "ASSIGNED_THIS_SEMESTER",
                "BACKLOG_FROM_SEMESTER_N",
                "ELECTIVE_FILL",
                "RETAKE_AFTER_FAIL",
                "RETAKE_IMPROVEMENT",
                name="selection_reason",
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["plan_id"], ["study_plan.plan_id"]),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["class_section.section_id"],
        ),
    )

    op.create_table(
        "plan_review",
        sa.Column("review_id", sa.String(36), primary_key=True),
        sa.Column("plan_id", sa.String(36), nullable=False),
        sa.Column("advisor_id", sa.String(36), nullable=False),
        sa.Column(
            "decision",
            sa.Enum("Approved", "NeedsRevision", name="review_decision"),
            nullable=False,
        ),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("review_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["study_plan.plan_id"]),
        sa.ForeignKeyConstraint(["advisor_id"], ["users.user_id"]),
    )

    op.create_table(
        "agent_run",
        sa.Column("run_id", sa.String(36), primary_key=True),
        sa.Column("student_id", sa.String(20), nullable=False),
        sa.Column(
            "generation_mode",
            sa.Enum("LLM", "Fallback", name="agent_generation_mode"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(50), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "Started",
                "Completed",
                "Failed",
                "Fallback",
                name="agent_run_status",
            ),
            nullable=False,
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student_profile.student_id"],
        ),
    )

    op.create_table(
        "tool_call",
        sa.Column("tool_call_id", sa.String(36), primary_key=True),
        sa.Column("run_id", sa.String(36), nullable=False),
        sa.Column("tool_name", sa.String(100), nullable=False),
        sa.Column("input_json", sa.JSON(), nullable=True),
        sa.Column("output_json", sa.JSON(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["agent_run.run_id"]),
    )


def downgrade() -> None:
    op.drop_table("tool_call")
    op.drop_table("agent_run")
    op.drop_table("plan_review")
    op.drop_table("study_plan_item")
    op.drop_table("study_plan")
    op.drop_table("section_meeting")
    op.drop_table("class_section")
    op.drop_table("course_offering")
    op.drop_table("prerequisite")
    op.drop_table("curriculum_course")
    op.drop_table("course_attempt")
    op.drop_table("academic_record")
    op.drop_table("student_profile")
    op.drop_table("class_group")
    op.drop_table("curriculum")
    op.drop_table("academic_program")
    op.drop_table("program_track")
    op.drop_table("faculty")
    op.drop_table("academic_term")
    op.drop_table("course")
    op.drop_table("users")
