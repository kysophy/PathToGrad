import { useEffect, useMemo, useState } from 'react';

import CourseCard from './CourseCard';
import CourseModal from './CourseModal';

import {
  getCourses,
  getTerms,
  type AcademicTerm,
  type Course,
} from '../services/Course';


export default function CourseCatalogPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [terms, setTerms] = useState<AcademicTerm[]>([]);

  const [selectedTermId, setSelectedTermId] = useState('');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);

  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');


  useEffect(() => {
    async function loadTerms() {
      try {
        const result = await getTerms();

        setTerms(result);

        if (result.length > 0) {
          setSelectedTermId(result[0].term_id);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load academic terms.',
        );
      }
    }

    loadTerms();
  }, []);


  useEffect(() => {
    async function loadCourses() {
      if (!selectedTermId) {
        return;
      }

      try {
        setLoading(true);
        setError('');
        setSelectedCourse(null);

        const result = await getCourses(selectedTermId);
        setCourses(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load course catalog.',
        );
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, [selectedTermId]);


  const selectedTerm = terms.find(
    (term) => term.term_id === selectedTermId,
  );


  const filteredCourses = useMemo(() => {
    const keyword = search.trim().toLowerCase();

    if (!keyword) {
      return courses;
    }

    return courses.filter((course) => {
      return (
        course.id.toLowerCase().includes(keyword) ||
        course.name.toLowerCase().includes(keyword)
      );
    });
  }, [courses, search]);


  const eligibleCourses = courses.filter(
    (course) => course.eligible === true,
  );


  return (
    <div className="flex flex-col gap-6 p-4 sm:p-6">

      <section className="rounded-2xl bg-[#0085FF] p-6">

        <h1 className="font-heading text-3xl text-white">
          Course Catalog
        </h1>


        <div className="mt-5 flex flex-col gap-3 md:flex-row">

          <input
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search by course code or name"
            className="flex-1 rounded-full bg-white px-5 py-3 font-body text-sm outline-none"
          />


          <select
            value={selectedTermId}
            onChange={(event) => setSelectedTermId(event.target.value)}
            className="rounded-full bg-white px-5 py-3 font-body text-sm"
          >
            {terms.length === 0 && (
              <option value="">
                No academic term
              </option>
            )}

            {terms.map((term) => (
              <option
                key={term.term_id}
                value={term.term_id}
              >
                {term.name}
              </option>
            ))}
          </select>

        </div>


        {loading && (
          <p className="mt-5 font-body text-sm text-white">
            Loading course catalog...
          </p>
        )}


        {error && (
          <div className="mt-5 rounded-xl bg-red-100 p-4 font-body text-sm text-red-700">
            {error}
          </div>
        )}


        {!loading && !error && (
          <div className="mt-6 flex gap-4 overflow-x-auto pb-3">

            {filteredCourses.map((course) => (
              <CourseCard
                key={course.id}
                course={course}
                onSelect={setSelectedCourse}
              />
            ))}


            {filteredCourses.length === 0 && (
              <p className="font-body text-sm text-white">
                No matching courses.
              </p>
            )}

          </div>
        )}

      </section>


      <section className="rounded-2xl bg-[#67DE53] p-6">

        <h2 className="font-heading text-2xl">
          Academic Term
        </h2>

        <p className="mt-2 font-body">
          {selectedTerm?.name ?? 'No term selected'}
        </p>


        <h2 className="mt-6 font-heading text-2xl">
          Eligible and Offered Courses
        </h2>


        {eligibleCourses.length === 0 ? (
          <p className="mt-2 font-body text-sm">
            No course is currently verified as both eligible and offered.
          </p>
        ) : (
          <div className="mt-3 grid gap-2">

            {eligibleCourses.map((course) => (
              <p
                key={course.id}
                className="font-body text-sm"
              >
                <strong>{course.id}</strong>
                {' — '}
                {course.name}
              </p>
            ))}

          </div>
        )}


        <p className="mt-6 font-body text-sm">
          Total active courses: {courses.length}
        </p>

      </section>


      <CourseModal
        course={selectedCourse}
        termId={selectedTermId}
        termName={selectedTerm?.name ?? selectedTermId}
        onClose={() => setSelectedCourse(null)}
      />

    </div>
  );
}