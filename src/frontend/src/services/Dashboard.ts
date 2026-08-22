import type { StudentDashboardProps } from '../components/StudentDashboardPage';

/**
 * Mock dashboard data, typed against the same StudentDashboardProps
 * interface the component itself defines (T-101). Still exported and
 * used as a fallback/dev-preview value — see StudentDashboardPage.tsx.
 */
export const MOCK_DASHBOARD_DATA: StudentDashboardProps = {
  studentName: '------',
  earnedCredits: 67,
  currentGPA: 6.7,
  academicRisks: 'None for now!',
  graduationProgress: 67,
  remainingCredits: 67,
  planProgress: 6.7,
  nextClass: 'Software Engineering',
  advisorNote: 'Keep up the work!',
  upcomingPlans: [
    { id: 'plan-1', taskName: 'Database individual homework', dueDate: '23/07/2026' },
    { id: 'plan-2', taskName: 'Database team bonus homework', dueDate: '23/07/2026' },
    { id: 'plan-3', taskName: 'Template 2 submission', dueDate: '27/07/2026' },
  ],
  workProgress: {
    completed: 46,
    atRisk: 54,
  },
};

// TODO: point this at your real API base — env var keeps it out of
// source control and different per environment (dev/staging/prod).
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

/**
 * Raw shape the backend actually returns. This is very unlikely to be
 * identical to StudentDashboardProps (different casing, different
 * nesting, extra fields the frontend doesn't need) — keep it separate
 * and go through mapDashboardResponse() below rather than trying to
 * force the backend to match the component's prop names.
 */
type DashboardApiResponse = {
  student_name: string;
  earned_credits: number;
  current_gpa: number;
  academic_risks: string | string[];
  graduation_progress_percent: number;
  remaining_credits: number;
  plan_progress_percent: number;
  next_class: string;
  advisor_note: string;
  upcoming_plans: { id: string; task_name: string; due_date: string }[];
  work_progress?: { completed_percent: number; at_risk_percent: number };
};

/**
 * Adapter: backend shape -> StudentDashboardProps. This is the one place
 * that needs to change if the API's field names/shape change — nothing
 * in StudentDashboard.tsx or this function's callers does.
 */
function mapDashboardResponse(res: DashboardApiResponse): StudentDashboardProps {
  return {
    studentName: res.student_name,
    earnedCredits: res.earned_credits,
    currentGPA: res.current_gpa,
    academicRisks: res.academic_risks,
    graduationProgress: res.graduation_progress_percent,
    remainingCredits: res.remaining_credits,
    planProgress: res.plan_progress_percent,
    nextClass: res.next_class,
    advisorNote: res.advisor_note,
    upcomingPlans: res.upcoming_plans.map((p) => ({
      id: p.id,
      taskName: p.task_name,
      dueDate: p.due_date,
    })),
    workProgress: res.work_progress
      ? {
          completed: res.work_progress.completed_percent,
          atRisk: res.work_progress.at_risk_percent,
        }
      : undefined,
  };
}

/**
 * Real fetch, used by the useQuery call in StudentDashboardPage.tsx.
 * Throws on a non-OK response so TanStack Query's `isError`/`error`
 * state picks it up automatically — don't swallow errors here.
 */
export async function getDashboardData(): Promise<StudentDashboardProps> {
  const res = await fetch(`${API_BASE_URL}/api/dashboard`, {
    credentials: 'include', // drop this if you're using a bearer token instead of cookies
  });

  if (!res.ok) {
    throw new Error(`Failed to load dashboard data: ${res.status} ${res.statusText}`);
  }

  const json: DashboardApiResponse = await res.json();
  return mapDashboardResponse(json);
}