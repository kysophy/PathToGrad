import { apiRequest } from './api';
import { getCurrentStudentId } from './session';


export type CourseOption = {
  course_code: string;
  course_name: string;
  credits: number;
};


export type AcademicTerm = {
  term_id: string;
  name: string;
};


export type ResultStatus =
  | 'Passed'
  | 'Failed'
  | 'InProgress';


export type CourseAttempt = {
  attempt_id: string;

  course_code: string;
  course_name: string;

  term_id: string;
  term_name: string;

  attempt_number: number;

  grade: number | null;

  result_status: ResultStatus;

  credits_earned: number;
};


export type AcademicRecord = {
  record_id: string;
  student_id: string;
  updated_at: string;

  earned_credits: number;
  passed_courses: string[];

  attempts: CourseAttempt[];
};


export type AttemptCreate = {
  course_code: string;
  term_id: string;

  attempt_number: number;

  grade: number | null;

  result_status: ResultStatus;

  credits_earned: number;
};


export function getCourseOptions() {
  return apiRequest<CourseOption[]>(
    '/api/meta/courses',
  );
}


export function getTerms() {
  return apiRequest<AcademicTerm[]>(
    '/api/meta/terms',
  );
}


export function getAcademicRecord() {
  return apiRequest<AcademicRecord>(
    `/api/students/${getCurrentStudentId()}/academic-record`,
  );
}


export function addAttempt(
  data: AttemptCreate,
) {
  return apiRequest<AcademicRecord>(
    `/api/students/${getCurrentStudentId()}/academic-record/attempts`,
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
  );
}
