import { apiRequest } from './api';
import { getCurrentStudentId, getCurrentUserId } from './session';


export type Faculty = {
  faculty_id: string;
  name: string;
};


export type ProgramTrack = {
  track_id: string;
  name: string;
};


export type AcademicProgram = {
  program_id: string;
  name: string;
};


export type CurriculumInfo = {
  found: boolean;
  curriculum_id: string | null;
  version: string | null;
};


export type ProfileFormData = {
  faculty_id: string;
  track_id: string;
  program_id: string;

  intake_year: number;
  current_semester: number;
  target_credit_load: number;
};


export type ProfileResponse = ProfileFormData & {
  student_id: string;
  user_id: string;

  faculty_name: string;
  track_name: string;
  program_name: string;

  curriculum_id: string | null;
  curriculum_version: string | null;

  is_complete: boolean;
  warning: string | null;
};


export function getFaculties() {
  return apiRequest<Faculty[]>(
    '/api/meta/faculties',
  );
}


export function getTracks() {
  return apiRequest<ProgramTrack[]>(
    '/api/meta/tracks',
  );
}


export function getPrograms(
  facultyId: string,
  trackId: string,
) {
  return apiRequest<AcademicProgram[]>(
    `/api/meta/programs?faculty_id=${encodeURIComponent(
      facultyId,
    )}&track_id=${encodeURIComponent(trackId)}`,
  );
}


export function getCurriculum(
  programId: string,
  intakeYear: number,
) {
  return apiRequest<CurriculumInfo>(
    `/api/meta/curriculum?program_id=${encodeURIComponent(
      programId,
    )}&intake_year=${intakeYear}`,
  );
}


export function getProfile() {
  return apiRequest<ProfileResponse>(
    `/api/students/${getCurrentStudentId()}/profile`,
  );
}


export function saveProfile(
  data: ProfileFormData,
) {
  return apiRequest<ProfileResponse>(
    `/api/students/${getCurrentStudentId()}/profile`,
    {
      method: 'PUT',

      body: JSON.stringify({
        user_id: getCurrentUserId(),
        ...data,
      }),
    },
  );
}
