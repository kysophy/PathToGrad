Hand-written SQL migrations in this folder are retired.

The canonical schema is Alembic:

    PathToGrad/src/backend/alembic/versions/001_initial_schema.py

From `PathToGrad/src/backend`:

    alembic upgrade head
