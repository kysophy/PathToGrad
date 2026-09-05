# Backend

FastAPI + SQLAlchemy 2 + Alembic, MySQL 8. Optional hosted Gemini via `google-genai`.

Root boot order, login aliases, and the Gemini stretch step: [`../../README.md`](../../README.md).

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

Leave `GEMINI_API_KEY` empty for the exam path. Never commit `.env`.

Bring MySQL up from the **repository root**: `docker compose up -d`. Wait until `pathtograd-mysql` is healthy.

## Schema and demo data

```powershell
alembic upgrade head
```

Expect revision `003_add_plan_uniques`.

On Windows, do **not** pipe `.sql` with `Get-Content ... | docker exec` (UTF-16; zero rows, fake success). From the **repository root**:

```powershell
docker cp src/database/seed.sql pathtograd-mysql:/tmp/seed.sql
docker exec pathtograd-mysql sh -c "mysql -uroot -ppathtograd pathtograd < /tmp/seed.sql"
```

Then, back in `src/backend`:

```powershell
python -m app.scripts.import_courses
```

`import_courses` reads `PathToGrad/data/Courses.csv` and `PathToGrad/data/offerings.csv`. It expects seed rows `CURR-TEST-2024` and term name `2026.1`. To regenerate those CSVs, see [`../../data/README.md`](../../data/README.md).

Five demo students (soft-lock, backlog, failed retakes, over-cap, near-graduation) live in `../database/seed_demo_students.sql`. Load them **after** import:

```powershell
docker cp src/database/seed_demo_students.sql pathtograd-mysql:/tmp/seed_demo_students.sql
docker exec pathtograd-mysql sh -c "mysql -uroot -ppathtograd pathtograd < /tmp/seed_demo_students.sql"
```

(`docker cp` paths are from the repository root.) Do not apply `fixtures/academic_planning_test_data.sql` on a demo database.

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/health`

Agent routes (engine always; Gemini optional):

- `POST /api/agent/plan`
- `POST /api/agent/chat`

## Tests

```powershell
python -m pytest tests -q
```

Fake-repo suite. No Docker and no Gemini key required.

## Layout

- `app/api/`: HTTP routes (`profile`, `academic_record`, `course_catalog`, `academic_planning`, `meta`, `agent`)
- `app/services/`: use-case logic (`agent_service` is the three-stage desk)
- `app/repositories/`: SQLAlchemy access
- `app/models/`: tables
- `app/deterministic/`: catalog, generator, risks, graduation, cadence. Do not import `app.llm` here
- `app/llm/`: hosted Gemini adapter, prompts, NFR-06 guard, templates, course briefs
- `app/scripts/import_courses.py`: CSV loader
- `alembic/versions/`: schema migrations (source of truth)
