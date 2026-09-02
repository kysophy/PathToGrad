# Frontend

React 19 + Vite + Tailwind v4 + TanStack Query. The Vite dev server proxies `/api` to `http://localhost:8000` (see `vite.config.ts`), so the backend must be running for live data.

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

On the login screen, student ID `test` (any password) signs in as `TEST001` without calling `/api/auth/login`. Any other student ID from the seed data (for example `DEMO-CAP`, password `NOT_USED_DAY1`) calls the real endpoint and loads that student instead: `CURRENT_STUDENT_ID` in `services/session.ts` is set from the login response, not hardcoded. Advisor/Admin role-based login is still out of scope.

## Layout

- `src/pages/`: route screens
- `src/components/`: notebook UI
- `src/layouts/AppShell.tsx`: header + chat sidebar
- `src/services/`: API clients
- `src/utils/`: auth / chat / role guards
