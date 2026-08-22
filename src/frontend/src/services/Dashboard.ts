import { apiRequest } from './api';
import { CURRENT_STUDENT_ID } from './session';

export type UpcomingPlan = {
  id: string;
  taskName: string;
  dueDate: string;
};

type ProfileApiResponse = {
  student_id: string;
  user_id: string;

  faculty_id: string;
  faculty_name: string;

  track_id: string;
  track_name: string;

  program_id: string;
  program_name: string;

  intake_year: number;
  current_semester: number;
  target_credit_load: number;

  curriculum_id: string | null;
  curriculum_version: string | null;

  is_complete: boolean;

  warning: string | null;
};

type GraduationProgressApiResponse = {
  student_id: string;
  curriculum_id: string;

  required_credits: number;
  earned_credits: number;
  remaining_credits: number;

  credit_requirement_met: boolean;

  completed_required_courses: string[];
  missing_required_courses: string[];

  completed: boolean;

  progress_percentage: number;
};

/**
 * DashboardData
 * -----------------------------------------------------------------------
 * Backend-provided fields (studentId through missingRequiredCourses) come
 * straight from the profile + graduation-progress endpoints below. The
 * remaining fields (studentName through workProgress) drive the study-plan
 * / advisor-note parts of the dashboard design but have no backing API yet
 * — they stay optional so the page renders correctly either way, and
 * PLACEHOLDER_DASHBOARD_EXTRAS below fills them with sensible defaults
 * until FR work adds real endpoints for them.
 */
export type DashboardData = {
  studentId: string;

  programName: string;
  curriculumVersion: string | null;

  profileComplete: boolean;

  earnedCredits: number;
  requiredCredits: number;
  remainingCredits: number;

  graduationPercent: number;
  graduationCompleted: boolean;

  completedRequiredCourses: string[];
  missingRequiredCourses: string[];

  studentName?: string;
  currentGPA?: number;
  academicRisks?: string | string[];
  planProgress?: number;
  nextClass?: string;
  advisorNote?: string;
  upcomingPlans?: UpcomingPlan[];
  workProgress?: {
    completed: number;
    atRisk: number;
  };
};

/** Placeholder values for the fields not yet exposed by the backend. */
export const PLACEHOLDER_DASHBOARD_EXTRAS: Required<
  Pick<
    DashboardData,
    | 'studentName'
    | 'currentGPA'
    | 'academicRisks'
    | 'planProgress'
    | 'nextClass'
    | 'advisorNote'
    | 'upcomingPlans'
    | 'workProgress'
  >
> = {
  studentName: 'Student',
  currentGPA: 0,
  academicRisks: 'No risk data available yet.',
  planProgress: 0,
  nextClass: 'No upcoming class scheduled.',
  advisorNote: 'No note from your advisor yet.',
  upcomingPlans: [],
  workProgress: {
    completed: 0,
    atRisk: 0,
  },
};

export async function getDashboardData(): Promise<DashboardData> {
  const [profile, progress] = await Promise.all([
    apiRequest<ProfileApiResponse>(`/api/students/${CURRENT_STUDENT_ID}/profile`),
    apiRequest<GraduationProgressApiResponse>(
      `/api/students/${CURRENT_STUDENT_ID}/graduation-progress`,
    ),
  ]);

  return {
    ...PLACEHOLDER_DASHBOARD_EXTRAS,

    studentId: profile.student_id,

    programName: profile.program_name,
    curriculumVersion: profile.curriculum_version,

    profileComplete: profile.is_complete,

    earnedCredits: progress.earned_credits,
    requiredCredits: progress.required_credits,
    remainingCredits: progress.remaining_credits,

    graduationPercent: progress.progress_percentage,
    graduationCompleted: progress.completed,

    completedRequiredCourses: progress.completed_required_courses,
    missingRequiredCourses: progress.missing_required_courses,
  };
}
