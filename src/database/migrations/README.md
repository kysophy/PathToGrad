Hand-written SQL migrations in this folder are retired.

The canonical schema is Alembic under `PathToGrad/src/backend/alembic/versions/` (`001_initial_schema`, `002_proofreading_fixes`, `003_add_plan_uniques`).

From `PathToGrad/src/backend`:

    alembic upgrade head
    alembic current

Expect `003_add_plan_uniques`.
