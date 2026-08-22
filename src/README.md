# Source

- [`backend/`](backend/README.md) — FastAPI app. Run from `src/backend` with `PYTHONPATH` implied by that working directory (`python -m app…`, `uvicorn app.main:app`, `alembic`).
- [`frontend/`](frontend/README.md) — Vite React app. Proxies `/api` to `http://localhost:8000`.
- [`database/seed.sql`](database/seed.sql) — demo users, faculty, CLC track, curriculum `CURR-TEST-2024`, term `2026.1`. Apply **after** `alembic upgrade head`. Do not load `fixtures/academic_planning_test_data.sql` onto a demo database.
- [`database/migrations/`](database/migrations/README.md) — retired hand-written SQL. Canonical schema is Alembic under `backend/alembic/versions/`.
