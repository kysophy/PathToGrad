# Frontend

React 19 + Vite + Tailwind v4 + TanStack Query. The Vite dev server proxies `/api` to `http://localhost:8000` (see `vite.config.ts`), so the backend must be running for live data.

Root boot order, demo script, and login table: [`../../README.md`](../../README.md).

## Setup

From `src/frontend` (this folder):

```powershell
npm install
npm run dev
```

Then open the URL Vite prints (usually `http://localhost:5173`).

```powershell
npm run build    # production bundle (output is gitignored)
npm run preview  # serve that bundle locally
```

## Demo login

On the login screen, student IDs `test`, `s02`, `s05`, `s08`, `fail`, and `cap` (any password) sign in as a Student without calling `/api/auth/login`. Aliases live in `src/services/session.ts`.

- **`s02`** (`DEMO-S02`) is the Study Plan / chat demo.
- `test` (`TEST001`) is an empty profile until you save Profile. Do not use it for Generate.

The five `DEMO-*` rows need `seed_demo_students.sql` loaded after course import. Real role-based login still expects `/api/auth/login`.

Chat (`ChatPanel`) POSTs `/api/agent/chat` once per message. Study Plan **Generate** POSTs `/api/agent/plan`. If the API is down, the panel says the planner is unreachable and must not invent a course name.

## Layout

- `src/pages/`: route screens (`StudyPlan.tsx` wires Generate)
- `src/components/`: notebook UI (`ChatPanel`, `StudyPlanPage`)
- `src/layouts/AppShell.tsx`: header + chat sidebar
- `src/services/`: API clients (`Agent.ts` for `/api/agent`)
- `src/utils/`: auth / chat / role guards
