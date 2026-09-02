# PathToGrad

PathToGrad is a university course-planning system for FIT@HCMUS students. It helps with academic profiles, records, prerequisite checks, graduation progress, course catalogs, and study-plan drafting.

## What you need

- Python 3.11+
- Node.js 20+
- Docker Desktop (MySQL 8; Adminer on port 8080)

The frontend talks to the API through Vite’s `/api` proxy (`http://localhost:8000`). Run **database → backend → frontend**.

## First-time setup

From the repository root:

```powershell
docker compose up -d
```

Wait until `pathtograd-mysql` is healthy. Then:

```powershell
cd src/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirement.txt
copy .env.example .env
alembic upgrade head
Get-Content ..\database\seed.sql | docker exec -i pathtograd-mysql mysql -uroot -ppathtograd pathtograd
python -m app.scripts.import_courses
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd src/frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`). Health check: `http://localhost:8000/api/health`. Database UI: `http://localhost:8080` (system: MySQL, server: `mysql`, user: `root`, password: `pathtograd`).

Login shortcut on the current UI: student ID `test` (any password) always signs in as `TEST001` without a backend call. For any other student, `/api/auth/login` is implemented: log in with a student ID from `seed.sql` or `seed_demo_students.sql` (for example `DEMO-CAP`) and the seeded password `NOT_USED_DAY1`; the app then loads that student's real data instead of `TEST001`. Advisor/Admin role-based login is still out of scope (FR-18).

## Day-to-day

```powershell
docker compose up -d
cd src/backend; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000
cd src/frontend; npm run dev
```

Details: [`src/backend/README.md`](src/backend/README.md), [`src/frontend/README.md`](src/frontend/README.md), [`data/README.md`](data/README.md). Schema choices that later tasks depend on: [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Repository layout

- `/src/backend`: FastAPI, SQLAlchemy, Alembic
- `/src/frontend`: React + Vite + Tailwind
- `/src/database`: demo `seed.sql` (apply after Alembic)
- `/data`: canonical `Courses.csv` / `offerings.csv` (do not hand-edit)
- `/docs`: requirements, design, tests, decisions
- `/pa`: assignment submissions
