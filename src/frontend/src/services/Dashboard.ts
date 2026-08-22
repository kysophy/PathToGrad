export type UpcomingPlan = {
  id: string;
  taskName: string;
  dueDate: string;
};

export type GraduationProgress = {
  percent: number;
  remainingCredits: number;
};

export type StudyPlanProgress = {
  percent: number;
  upcomingClass: string;
};

export type WorkProgress = {
  /** Percent of tracked work that's on-track/completed (green segment). */
  completed: number;
  /** Percent that's at risk / behind (red segment). */
  atRisk: number;
};

export type DashboardData = {
  studentName: string;
  earnedCredits: number;
  currentGPA: number;
  academicRisks: string;
  graduationProgress: GraduationProgress;
  studyPlanProgress: StudyPlanProgress;
  upcomingPlans: UpcomingPlan[];
  advisorsFeedback: string;
  workProgress: WorkProgress;
};

/**
 * Mock dashboard data. StudentDashboard is a presentational component
 * that takes `data: DashboardData` as a prop rather than fetching it
 * itself — the page that renders it (see pages/StudentDashboardPage.tsx)
 * owns the data source. Swapping MOCK_DASHBOARD_DATA for a real
 * `useQuery(['dashboard'], getDashboardData)` call later only touches
 * that page, not this file's shape or the component.
 */
export const MOCK_DASHBOARD_DATA: DashboardData = {
  studentName: '------',
  earnedCredits: 67,
  currentGPA: 6.7,
  academicRisks: 'None for now!',
  graduationProgress: {
    percent: 67,
    remainingCredits: 67,
  },
  studyPlanProgress: {
    percent: 6.7,
    upcomingClass: 'Software Engineering',
  },
  upcomingPlans: [
    { id: 'plan-1', taskName: 'Database individual homework', dueDate: '23/07/2026' },
    { id: 'plan-2', taskName: 'Database team bonus homework', dueDate: '23/07/2026' },
    { id: 'plan-3', taskName: 'Template 2 submission', dueDate: '27/07/2026' },
  ],
  advisorsFeedback: 'Keep up the work!',
  workProgress: {
    completed: 46,
    atRisk: 54,
  },
};

/**
 * Stub async accessor — wire this up to a real endpoint later
 * (fetch/axios) or drop it entirely once a TanStack Query hook calls the
 * API directly. Kept here so the rest of the app can already import a
 * consistent "get dashboard data" entry point.
 */
export async function getDashboardData(): Promise<DashboardData> {
  return MOCK_DASHBOARD_DATA;
}