import {
  apiRequest,
} from './api';

import { getCurrentStudentId } from './session';


export type AcademicTerm = {
  term_id: string;
  name: string;
};


type CourseCatalogApiItem = {
  course_code: string;
  course_name: string;
  credits: number;

  prerequisite_codes: string[];

  prerequisite_eligible:
  boolean | null;

  offered: boolean;

  eligible:
  boolean | null;

  warnings: string[];
};


export type Course = {
  id: string;
  name: string;
  credits: number;

  prerequisiteChain: string[];

  prerequisiteEligible:
  boolean | null;

  offered: boolean;

  eligible:
  boolean | null;

  warnings: string[];

  color:
  | 'yellow'
  | 'pink';
};


export type PrerequisiteItem = {
  course_code: string;
  course_name: string;

  status: string;

  satisfied:
  boolean | null;

  warning:
  string | null;
};


export type PrerequisiteCheck = {
  course_code: string;

  eligible:
  boolean | null;

  prerequisites:
  PrerequisiteItem[];

  warnings: string[];
};


export type Meeting = {
  day_of_week: string;
  start_time: string;
  end_time: string;
};


export type ClassSection = {
  section_id: string;
  section_code: string;

  capacity: number;

  meetings: Meeting[];
};


export type CourseEligibility = {
  course_code: string;
  term_id: string;

  prerequisite_eligible:
  boolean | null;

  offered: boolean;

  eligible:
  boolean | null;

  sections: ClassSection[];

  warnings: string[];
};


export type CourseDetails = {
  prerequisites:
  PrerequisiteCheck;

  eligibility:
  CourseEligibility;
};


export async function getTerms():
  Promise<AcademicTerm[]> {

  return apiRequest<
    AcademicTerm[]
  >(
    '/api/meta/terms',
  );
}


export async function getCourses(
  termId: string,
): Promise<Course[]> {

  const items =
    await apiRequest<
      CourseCatalogApiItem[]
    >(
      `/api/students/` +
      `${getCurrentStudentId()}` +
      `/course-catalog` +
      `?term_id=` +
      `${encodeURIComponent(termId)}`,
    );


  return items.map(
    (
      item,
      index,
    ): Course => ({

      id:
        item.course_code,

      name:
        item.course_name,

      credits:
        item.credits,

      prerequisiteChain:
        item.prerequisite_codes,

      prerequisiteEligible:
        item.prerequisite_eligible,

      offered:
        item.offered,

      eligible:
        item.eligible,

      warnings:
        item.warnings,

      color:
        index % 2 === 0
          ? 'yellow'
          : 'pink',
    }),
  );
}


export async function getCourseDetails(
  courseCode: string,
  termId: string,
): Promise<CourseDetails> {

  const encodedCourse =
    encodeURIComponent(
      courseCode
    );

  const encodedTerm =
    encodeURIComponent(
      termId
    );


  const [
    prerequisites,
    eligibility,
  ] = await Promise.all([

    apiRequest<
      PrerequisiteCheck
    >(
      `/api/students/` +
      `${getCurrentStudentId()}` +
      `/courses/` +
      `${encodedCourse}` +
      `/prerequisites`,
    ),

    apiRequest<
      CourseEligibility
    >(
      `/api/students/` +
      `${getCurrentStudentId()}` +
      `/courses/` +
      `${encodedCourse}` +
      `/eligibility` +
      `?term_id=${encodedTerm}`,
    ),
  ]);


  return {
    prerequisites,
    eligibility,
  };
}