import { useState } from 'react';
import CourseCard from './CourseCard.tsx';
import CourseModal from './CourseModal.tsx';
import LinedRow from './LinedRow.tsx';
import { getCourses, getRecommendedCourseNames, getAvailableCourseNames } from '../services/Course.ts';
import type { Course } from '../services/Course.ts';

import starSparkleYellow from '../assets/Yellow Twinkles.svg';
import starSparkleBlue from '../assets/Blue Stars.svg';
import flowerLoop from '../assets/Small Orange Flower.svg';

/**
 * CourseCatalog
 * -----------------------------------------------------------------------
 * The Course Catalog page content. Meant to be rendered inside AppShell's
 * <Outlet/> at the /course route — it does not render the top header or
 * the chat sidebar itself, only the catalog content (blue "My course"
 * search panel + green recommended-courses panel + the Frame 35 course
 * detail modal).
 *
 * Course data comes from src/services/Course.ts, not from inline
 * constants — the card row maps over whatever getCourses() returns, so
 * adding, removing, or fetching courses from a real API only requires
 * changing that one file.
 */
 
/** Scattered sparkle positions inside the blue panel — percentages of the
 * panel's own box, purely decorative. */
const SPARKLES: { src: string; l: number; t: number; w: number }[] = [
  { src: starSparkleYellow, l: 3, t: 4, w: 5 },
  { src: starSparkleYellow, l: 34, t: 6, w: 4 },
  { src: starSparkleYellow, l: 58, t: 5, w: 4 },
  { src: starSparkleYellow, l: 82, t: 8, w: 6 },
  { src: starSparkleYellow, l: 22, t: 42, w: 4 },
  { src: starSparkleYellow, l: 95, t: 45, w: 4 },
  { src: starSparkleBlue, l: 12, t: 12, w: 8 },
  { src: starSparkleBlue, l: 90, t: 15, w: 8 },
  { src: starSparkleBlue, l: 65, t: 30, w: 7 },
];
 
export default function CourseCatalog() {
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [search, setSearch] = useState('');
  const courses = getCourses();
  const recommended = getRecommendedCourseNames();
  const available = getAvailableCourseNames();
 
  const query = search.trim().toLowerCase();
  const filteredCourses = query
    ? courses.filter(
        (course) =>
          course.name.toLowerCase().includes(query) || course.id.toLowerCase().includes(query),
      )
    : courses;
 
  return (
    <div className="flex flex-col gap-6 p-4 sm:p-6">
      {/* Blue "My course" panel */}
      <section className="relative overflow-hidden rounded-2xl bg-[#0085FF] p-5 sm:p-8">
        <div className="pointer-events-none absolute inset-0">
          {SPARKLES.map((s, i) => (
            <img
              key={i}
              src={s.src}
              alt=""
              className="absolute h-auto select-none"
              style={{ left: `${s.l}%`, top: `${s.t}%`, width: `${s.w}%` }}
            />
          ))}
        </div>
 
        <h1 className="relative z-10 font-heading text-2xl text-white">My course</h1>
 
        <div className="relative z-10 mt-4 flex flex-col gap-3 sm:flex-row">
          <div className="flex flex-1 items-center gap-2 rounded-full bg-[#ECE6F0] px-5 py-3">
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search course"
              aria-label="Search course"
              className="w-full bg-transparent font-body text-sm text-neutral-700 placeholder:text-neutral-500 focus:outline-none"
            />
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="h-4 w-4 shrink-0 text-neutral-600">
              <circle cx="11" cy="11" r="7" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </div>
 
          <button
            type="button"
            className="flex items-center justify-center gap-1.5 rounded-full bg-white px-5 py-3 font-body text-sm text-neutral-800"
          >
            Semester
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-3 w-3">
              <path d="M3 5h18l-7 9v5l-4-2v-3z" />
            </svg>
          </button>
 
          <button
            type="button"
            className="flex items-center justify-center gap-1.5 rounded-full bg-white px-5 py-3 font-body text-sm text-neutral-800"
          >
            Department
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-3 w-3">
              <path d="M3 5h18l-7 9v5l-4-2v-3z" />
            </svg>
          </button>
        </div>
 
        <div className="relative z-10 mt-6 flex snap-x snap-mandatory gap-4 overflow-x-auto pb-2">
          {filteredCourses.map((course) => (
            <CourseCard key={course.id} course={course} onSelect={setSelectedCourse} />
          ))}
          {filteredCourses.length === 0 && (
            <p className="font-body text-sm text-white/80">
              No courses match "{search}".
            </p>
          )}
        </div>
      </section>
 
      {/* Green recommended/available panel, bordered by the repeating
          flower doodle on each side — flex layout, no absolute positioning. */}
      <section className="flex overflow-hidden rounded-2xl">
        <div
          aria-hidden="true"
          className="hidden w-6 shrink-0 bg-[#67DE53] sm:block"
          style={{
            backgroundImage: `url(${flowerLoop})`,
            backgroundRepeat: 'repeat-y',
            backgroundPosition: 'center',
            backgroundSize: '48px auto',
          }}
        />
 
        <div className="flex-1 bg-[#67DE53] p-6 text-neutral-900 sm:p-8">
          <LinedRow bold>Recommended courses:</LinedRow>
          {recommended.map((c) => (
            <LinedRow key={c}>{c}</LinedRow>
          ))}
 
          <LinedRow bold className="mt-2">
            Available courses:
          </LinedRow>
          {available.map((c) => (
            <LinedRow key={c}>{c}</LinedRow>
          ))}
        </div>
 
        <div
          aria-hidden="true"
          className="hidden w-6 shrink-0 bg-[#67DE53] sm:block"
          style={{
            backgroundImage: `url(${flowerLoop})`,
            backgroundRepeat: 'repeat-y',
            backgroundPosition: 'center',
            backgroundSize: '48px auto',
          }}
        />
      </section>
 
      <CourseModal course={selectedCourse} onClose={() => setSelectedCourse(null)} />
    </div>
  );
}
 