from alembic import op
import sqlalchemy as sa


revision = "002_proofreading_fixes"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("chk_term_no", "academic_term", type_="check")
    op.drop_column("academic_term", "term_no")
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    op.execute(
        sa.text(
            "UPDATE curriculum_course SET spec_code = 'GEN' "
            "WHERE spec_code IS NULL"
        )
    )


def downgrade() -> None:
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.add_column(
        "academic_term",
        sa.Column("term_no", sa.Integer(), nullable=False, server_default="1"),
    )
    op.create_check_constraint("chk_term_no", "academic_term", "term_no > 0")
    op.alter_column("academic_term", "term_no", server_default=None)
    op.execute(
        sa.text(
            "UPDATE curriculum_course SET spec_code = NULL "
            "WHERE spec_code = 'GEN'"
        )
    )
