export type OpeningClass = {
  section: string;
  instructor: string;
  enrolled: number;
  capacity: number;
};

export type Course = {
  id: string;
  name: string;
  credits: number;
  prerequisiteChain: string[];
  status: string;
  color: 'yellow' | 'pink';
  openingClasses: OpeningClass[];
  note?: string;
};

/**
 * Mock course catalog. The dashboard grid and modal both read from this
 * file rather than hardcoding data inline, so:
 *  - adding/removing a course here is the only change needed to update
 *    the grid — CourseCard/StudentDashboard just map over whatever this
 *    returns, however many entries that is.
 *  - swapping this out for a real API call later (e.g. wiring up
 *    getCourses() to `fetch`/react-query) doesn't require touching any
 *    component.
 */
const COURSES: Course[] = [
  {
    id: 'MTH00015',
    name: 'Computational Algebra',
    credits: 4,
    prerequisiteChain: ['Linear Algebra I', 'Linear Algebra II'],
    status: 'Unavailable',
    color: 'yellow',
    openingClasses: [
      { section: '24C10', instructor: 'Nguyen Van A', enrolled: 20, capacity: 45 },
      { section: '24C07', instructor: 'Le Thi A', enrolled: 40, capacity: 45 },
    ],
    note: 'This course is currently unavailable for you!',
  },
  {
    id: 'CSC00067',
    name: 'DSA',
    credits: 4,
    prerequisiteChain: ['Programming Fundamentals'],
    status: 'Can register',
    color: 'pink',
    openingClasses: [
      { section: '24C03', instructor: 'Tran Van B', enrolled: 30, capacity: 50 },
      { section: '24C04', instructor: 'Pham Thi C', enrolled: 18, capacity: 50 },
    ],
  },
  {
    id: 'MTH00007',
    name: 'Linear Algebra II',
    credits: 4,
    prerequisiteChain: ['Linear Algebra I'],
    status: 'Unavailable',
    color: 'yellow',
    openingClasses: [{ section: '24C02', instructor: 'Hoang Van D', enrolled: 45, capacity: 45 }],
    note: 'This course is currently unavailable for you!',
  },
  {
    id: 'CSC00012',
    name: 'Introduction to Information Technology',
    credits: 3,
    prerequisiteChain: [],
    status: 'Can register',
    color: 'pink',
    openingClasses: [{ section: '24C01', instructor: 'Vo Thi E', enrolled: 42, capacity: 60 }],
  },
  {
    id: 'MTH00003',
    name: 'Linear Algebra I',
    credits: 4,
    prerequisiteChain: [],
    status: 'Can register',
    color: 'yellow',
    openingClasses: [
      { section: '24C05', instructor: 'Dang Van F', enrolled: 50, capacity: 50 },
      { section: '24C06', instructor: 'Ly Thi G', enrolled: 12, capacity: 50 },
    ],
  },
];

const RECOMMENDED_COURSE_NAMES = ['DSA', 'Linear Algebra I', 'Introduction to Information Technology'];
const AVAILABLE_COURSE_NAMES = ['DSA', 'Introduction to Information Technology'];

// Accessor functions rather than exporting the arrays directly, so
// swapping these for real async calls later (fetch/react-query) is a
// change in this file only — call sites already treat this as the
// single source of truth for course data.
export function getCourses(): Course[] {
  return COURSES;
}

export function getRecommendedCourseNames(): string[] {
  return RECOMMENDED_COURSE_NAMES;
}

export function getAvailableCourseNames(): string[] {
  return AVAILABLE_COURSE_NAMES;
}