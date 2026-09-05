import { apiRequest } from './api';
import { getCurrentStudentId } from './session';


export type GraduationProgress = {
  student_id: string;
  earned_credits: number;
  required_credits: number;
  remaining_credits: number;
  mandatory_passed: boolean;
  credit_requirement_met: boolean;
  missing_required_courses: string[];
  gpa: number | null;
  completed: boolean;
};


export function getGraduationProgress() {
  return apiRequest<GraduationProgress>(
    `/api/students/${getCurrentStudentId()}/graduation-progress`,
  );
}