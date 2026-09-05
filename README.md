# PathToGrad

PathToGrad is a course-planning notebook for FIT@HCMUS students. It keeps an academic profile and transcript, checks prerequisites and graduation progress, shows the term catalog, and drafts a semester plan.

**The engine writes the plan. The LLM only explains it.** A missing Gemini key is a valid exam path: Study Plan **Generate** and chat still return an engine course list plus template prose. The student still adds, drops, and decides. This is not the HCMUS registration portal.

## What this build does

| Area | Status |
| --- | --- |
| Profile | Wired (`GET` / `PUT /api/students/{id}/profile`) |
| Academic record | Wired (list + add attempts) |
| Graduation progress | Wired (`earned_credits`, mandatory / credit flags, GPA). Dashboard donut is derived in the UI |
| Course catalog, prerequisites, eligibility | Wired (A-10). Recommended = Assigned + Backlog |
| Semester plan + risk detector | Wired. `POST /api/agent/plan` always runs the engine |
| Chat | Wired. `POST /api/agent/chat` is single-turn: plan, course brief, engine risks, greet, or a polite refuse. No general Q&A |
| Explanations | Templates always. Hosted Gemini (`gemini-2.0-flash`) is optional stretch, then a course-code guard |
| Demo students | Five `DEMO-*` personas in `src/database/seed_demo_students.sql` |
| Login / roles | UI cheat aliases only. No `/api/auth/login` |
| Save draft, submit, plan history | UI only. No HTTP yet |
| Advisor dashboard, agent-run admin page | UI / table stubs. No advisor API, no `GET /admin/agent-runs` |

Schema choices that later tasks depend on: [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Stack

- **API:** Python 3.11+, FastAPI, SQLAlchemy 2, Alembic
- **UI:** React 19, Vite, Tailwind v4, TanStack Query
- **DB:** MySQL 8 in Docker; Adminer on port 8080
- **LLM (optional):** `google-genai` HTTPS to Gemini. Not PyTorch, not LangChain, not an agents SDK

The frontend talks to `/api/...`. Vite proxies that to `http://localhost:8000`. Run **database → backend → frontend**.

## What you need

- Python 3.11+
- Node.js 20+
- Docker Desktop (`docker compose`, two words)
- PowerShell on Windows (macOS / Linux: same Docker commands; use `source .venv/bin/activate` and `cp` instead of `copy`)

## First-time setup

From the **repository root** (`PathToGrad/`).

### 1. Database

```powershell
docker compose up -d
docker inspect --format "{{.State.Health.Status}}" pathtograd-mysql
```

Wait until that prints `healthy` (often 20-40 seconds on first boot).

Adminer: [http://localhost:8080](http://localhost:8080)

- System: **MySQL**
- Server: **`mysql`** (compose service name, not `localhost`)
- Username: `root`
- Password: `pathtograd`
- Database: `pathtograd`

### 2. Backend env

```powershell
cd src/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirement.txt
copy .env.example .env
```

If `Activate.ps1` is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

`.env` (never commit the real file) should look like:

```
DATABASE_URL=mysql+pymysql://root:pathtograd@localhost:3306/pathtograd
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash
DEFAULT_TERM_ID=TERM-2026-1
```

Leave `GEMINI_API_KEY` empty unless you are doing the stretch step below.

### 3. Schema and seeds

MySQL must already be healthy. **Four commands, in this order.** Do not load `seed_demo_students.sql` before `import_courses` (it `JOIN`s `course` on `course_code`). Do not apply `fixtures/academic_planning_test_data.sql` on a demo database.

From `src/backend` with the venv on:

```powershell
alembic upgrade head
alembic current
```

Expect revision **`003_add_plan_uniques`**.

On Windows, do **not** pipe `.sql` files with `Get-Content ... | docker exec`. PowerShell often sends UTF-16, and the MySQL password warning still prints, so it looks successful while **zero `DEMO-*` rows** land. Copy the file into the container instead. Paths below are from the **repository root**:

```powershell
cd ..\..
docker cp src/database/seed.sql pathtograd-mysql:/tmp/seed.sql
docker exec pathtograd-mysql sh -c "mysql -uroot -ppathtograd pathtograd < /tmp/seed.sql"

cd src/backend
python -m app.scripts.import_courses
```

Want a line like `Import completed`. If you see `No module named 'app'`:

```powershell
$env:PYTHONPATH = "."
python -m app.scripts.import_courses
```

Then the five demo students (**after** import):

```powershell
cd ..\..
docker cp src/database/seed_demo_students.sql pathtograd-mysql:/tmp/seed_demo_students.sql
docker exec pathtograd-mysql sh -c "mysql -uroot -ppathtograd pathtograd < /tmp/seed_demo_students.sql"
```

Prove it landed (six profile ids including five `DEMO-*`, attempts around 68):

```powershell
docker exec pathtograd-mysql mysql -uroot -ppathtograd -e "USE pathtograd; SELECT student_id, current_semester FROM student_profile ORDER BY student_id; SELECT COUNT(*) AS attempts FROM course_attempt;"
```

Fallback: paste the same `.sql` into Adminer’s SQL box, still **after** import.

### 4. API

From `src/backend`, venv on:

```powershell
uvicorn app.main:app --reload --port 8000
```

- Health: [http://localhost:8000/api/health](http://localhost:8000/api/health) → `{"status":"ok"}`
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. UI

In a second terminal:

```powershell
cd src/frontend
npm install
npm run dev
```

Open the URL Vite prints (usually [http://localhost:5173](http://localhost:5173)).

## Login (current UI)

Password is anything. None of these call `/api/auth/login`. Any id **not** in the table hits that missing route and fails. Aliases are defined in `src/frontend/src/services/session.ts`.

| Type this | Lands as | What you should see |
| --- | --- | --- |
| **`s02`** | `DEMO-S02` | Use this for Study Plan / chat. Sem-1 passed (~15 cr). Soft-lock this term |
| `s05` | `DEMO-S05` | Mid-path plus one backlog |
| `fail` | `DEMO-FAIL` | Failed `CSC10012` once; `CSC10009` failed twice |
| `s08` | `DEMO-S08` | SE senior. `CSC13001` is not offered this term |
| `cap` | `DEMO-CAP` | Assigned + backlog hits the 24-credit / 6-course cap |
| `test` | `TEST001` | Empty notebook until you save Profile. Dashboard stays 0 / 138. Bad for Generate |

`test` is the blank identity. The five `DEMO-*` rows 404 until step 3 loaded the demo seed.

## Optional stretch: Gemini key

The demo must work with an empty key. A [Google AI Studio API key](https://aistudio.google.com/docs/api-key) only changes Stage 3 from **Template explanation** to **Gemini explanation** when the guard accepts the prose.

1. Create a key at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey). Google AI Pro is not this key.
2. Put it in `src/backend/.env` as `GEMINI_API_KEY=...` (no quotes). Keep `GEMINI_MODEL=gemini-2.0-flash`.
3. **Restart uvicorn.** Settings are cached at process start.
4. Log in as `s02` → Study Plan → Generate. If Gemini times out or invents a code, you still get an engine plan and templates.

Do not commit `.env`, paste the secret into git, or share it in chat.

## Day-to-day

```powershell
docker compose up -d
cd src/backend; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000
cd src/frontend; npm run dev
```

Do not re-run Alembic, either seed, or import unless you destroyed the volume (`docker compose down -v`) or changed the CSVs. After a volume wipe, repeat first-time step 3 in full.

Stop: Ctrl+C in the API and UI terminals, then `docker compose stop`.

## Tests

Engine and AI tests use a fake repo. No Docker and no Gemini key required.

```powershell
cd src/backend
.\.venv\Scripts\Activate.ps1
python -m pytest tests -q
```

That is not proof MySQL is seeded.

## Quick demo (~5 minutes)

Assume first-time boot already ran.

1. Open [http://localhost:5173](http://localhost:5173). Type **`s02`**, any password, role Student.
2. Dashboard: earned credits should not be 0 / 138. Catalog term **2026.1**: Assigned includes `CSC10004`.
3. **Study Plan → Generate.** Point at **Engine plan**, Assigned/Backlog Recommended, and **Template explanation** (or **Gemini explanation** if a key is set and the guard passed). The preferred-semester dropdown is cosmetic; the engine uses `profile.current_semester` + `TERM-2026-1`.
4. Right-hand chat (bubbles are in-memory; refresh clears them):
   - `What is CSC10004?`: catalog + brief + "illustrative, not the official syllabus"
   - `Generate my plan.`: same engine plan, in sentences
   - `What are my risks?`: engine `detect_risks` only
   - `What is the weather?`: refuse, no invented courses
5. Log out. Type **`s08`**. Chat `What is CSC13001?` is allowed; Generate must **not** place it (no offering this term).

If uvicorn is down, chat must say the planner is unreachable. It must not name a course.

Swagger smoke (same stack, no UI): `POST /api/agent/plan` with `student_id=DEMO-S02` and `term_id=TERM-2026-1` returns engine items. Empty key → `explanation_source: template`.

## If it breaks

| Symptom | Likely cause |
| --- | --- |
| `alembic` connection refused | MySQL not healthy yet |
| `Access denied for user root` | Old Docker volume with another password → `docker compose down -v` and start from “First-time setup” |
| Port 3306 in use | Local MySQL service; stop it or map `3307:3306` and change `.env` |
| UI loads, every page errors | uvicorn not on 8000 |
| Only `TEST001` in `student_profile` | Demo seed never applied (PowerShell pipe / wrong cwd). Re-run the `docker cp` commands |
| Five `DEMO-*` profiles, zero attempts | Demo seed ran **before** import → `docker compose down -v` and redo step 3 |
| Dashboard 0 / 138 | You logged in as `test`. Use **`s02`** |
| Login fails with a random id | Expected. Only the aliases in the login table work |
| Generate still says Template after pasting a key | Uvicorn not restarted, `.env` not in `src/backend/`, or Gemini failed the guard / timed out |

## Repository layout

- `/src/backend`: FastAPI, SQLAlchemy, Alembic. Deterministic engine in `app/deterministic/`. Optional Gemini adapter, guard, and templates in `app/llm/`
- `/src/frontend`: React + Vite + Tailwind. Chat is `ChatPanel`; Generate is `pages/StudyPlan.tsx`
- `/src/database`: `seed.sql` then `seed_demo_students.sql` (apply after Alembic and `import_courses`)
- `/data`: canonical `Courses.csv` / `offerings.csv` (do not hand-edit). Illustrative `course_briefs.json` for chat
- `/docs`: requirements, design, tests, decisions
- `/pa`: assignment submissions

More setup detail: [`src/backend/README.md`](src/backend/README.md), [`src/frontend/README.md`](src/frontend/README.md), [`data/README.md`](data/README.md).
