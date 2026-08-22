import { useEffect } from 'react';
import type { Course } from '../services/Course';
import LinedRow from './LinedRow';

type CourseModalProps = {
  course: Course | null;
  onClose: () => void;
};

/**
 * CourseModal ("Frame 35")
 * -----------------------------------------------------------------------
 * Green notebook-paper popup shown when a course card is clicked. Not
 * sourced from an SVG/HTML export — rebuilt from the visual reference:
 * bright green background, rounded corners, thin horizontal ruled lines.
 */
export default function CourseModal({ course, onClose }: CourseModalProps) {
  // Escape key closes the modal, same as clicking the backdrop or the X.
  useEffect(() => {
    if (!course) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [course, onClose]);

  if (!course) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="course-modal-title"
        onClick={(e) => e.stopPropagation()}
        className="relative w-full max-w-md rounded-2xl bg-[#67DE53] p-6 text-neutral-900 shadow-xl sm:p-8"
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="Close"
          className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full bg-black/10 text-neutral-900 hover:bg-black/20"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="h-4 w-4">
            <line x1="6" y1="6" x2="18" y2="18" />
            <line x1="18" y1="6" x2="6" y2="18" />
          </svg>
        </button>

        <h2 id="course-modal-title" className="sr-only">
          {course.name} details
        </h2>

        <div className="pr-8">
          <LinedRow bold>Course information:</LinedRow>
          <LinedRow>Course name: {course.name}</LinedRow>
          <LinedRow>Course ID: {course.id}</LinedRow>
          <LinedRow>Credits: {course.credits}</LinedRow>

          <LinedRow bold className="mt-2">
            Opening classes:
          </LinedRow>
          {course.openingClasses.map((oc) => (
            <LinedRow key={oc.section}>
              {oc.section} - {oc.instructor} - {oc.enrolled}/{oc.capacity}
            </LinedRow>
          ))}
          {course.openingClasses.length === 0 && <LinedRow>...</LinedRow>}

          {course.note && (
            <LinedRow className="mt-2">
              <span className="font-heading">Note: </span>
              {course.note}
            </LinedRow>
          )}
        </div>
      </div>
    </div>
  );
}