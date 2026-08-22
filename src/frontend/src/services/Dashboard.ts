import {
  apiRequest,
} from './api';

import {
  CURRENT_STUDENT_ID,
} from './session';


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
};


export async function getDashboardData():
Promise<DashboardData> {

  const [
    profile,
    progress,
  ] = await Promise.all([
    apiRequest<ProfileApiResponse>(
      `/api/students/` +
      `${CURRENT_STUDENT_ID}/profile`,
    ),

    apiRequest<GraduationProgressApiResponse>(
      `/api/students/` +
      `${CURRENT_STUDENT_ID}/graduation-progress`,
    ),
  ]);

  return {
    studentId:
      profile.student_id,

    programName:
      profile.program_name,

    curriculumVersion:
      profile.curriculum_version,

    profileComplete:
      profile.is_complete,

    earnedCredits:
      progress.earned_credits,

    requiredCredits:
      progress.required_credits,

    remainingCredits:
      progress.remaining_credits,

    graduationPercent:
      progress.progress_percentage,

    graduationCompleted:
      progress.completed,

    completedRequiredCourses:
      progress.completed_required_courses,

    missingRequiredCourses:
      progress.missing_required_courses,
  };
}