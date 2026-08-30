# Backend

FastAPI + SQLAlchemy 2 + Alembic, MySQL 8.

## Setup

From `src/backend` (this folder):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirement.txt
copy .env.example .env
```

`.env` must define `DATABASE_URL` (copy from `.env.example`). Alembic reads that value in `alembic/env.py`; do not put a real password in `alembic.ini`. The example matches `docker-compose.yml` at the repo root:

```
mysql+pymysql://root:pathtograd@localhost:3306/pathtograd
```

Bring MySQL up from the **repository root**: `docker compose up -d`.

## Schema and demo data

```powershell
alembic upgrade head
Get-Content ..\database\seed.sql | docker exec -i pathtograd-mysql mysql -uroot -ppathtograd pathtograd
python -m app.scripts.import_courses
```

`import_courses` reads `PathToGrad/data/Courses.csv` and `PathToGrad/data/offerings.csv`. It expects seed rows `CURR-TEST-2024` and term name `2026.1`. To regenerate those CSVs, see [`../../data/README.md`](../../data/README.md).

Optional testing seed data (five demo students covering specific engine scenarios: soft-lock top-up, backlog, failed retakes, over-cap deferral, and near-graduation) lives in `../database/seed_demo_students.sql`. Load it the same way, after `seed.sql`:

```powershell
Get-Content ..\database\seed_demo_students.sql | docker exec -i pathtograd-mysql mysql -uroot -ppathtograd pathtograd
```

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/health`

## Tests

```powershell
pytest
```

## Layout

- `app/api/`: HTTP routes
- `app/services/`: use-case logic
- `app/repositories/`: SQLAlchemy access
- `app/models/`: tables
- `app/deterministic/`: graduation progress and prerequisite rules
- `app/scripts/import_courses.py`: CSV loader
- `alembic/versions/`: schema migrations (source of truth)
