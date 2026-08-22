import { apiRequest } from './api';
import { CURRENT_STUDENT_ID } from './session';


export type GraduationProgress = {
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


export function getGraduationProgress() {
  return apiRequest<GraduationProgress>(
    `/api/students/${CURRENT_STUDENT_ID}/graduation-progress`,
  );
}