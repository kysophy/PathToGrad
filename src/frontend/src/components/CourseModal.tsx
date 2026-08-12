import { useEffect } from 'react';
import type { Course } from '../services/Course';

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
        className="relative w-full max-w-md rounded-2xl bg-[#67DE53] p-6 font-body text-neutral-900 shadow-xl sm:p-8"
        style={{
          backgroundImage:
            'repeating-linear-gradient(to bottom, transparent, transparent 35px, rgba(0,0,0,0.55) 35px, rgba(0,0,0,0.55) 37px)',
        }}
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

        <div className="flex flex-col gap-1 pr-8">
          <p className="font-heading text-lg leading-[35px]">Course information:</p>
          <p className="leading-[35px]">Course name: {course.name}</p>
          <p className="leading-[35px]">Course ID: {course.id}</p>
          <p className="leading-[35px]">Credits: {course.credits}</p>

          <p className="mt-2 font-heading text-lg leading-[35px]">Opening classes:</p>
          {course.openingClasses.map((oc) => (
            <p key={oc.section} className="leading-[35px]">
              {oc.section} - {oc.instructor} - {oc.enrolled}/{oc.capacity}
            </p>
          ))}
          {course.openingClasses.length === 0 && <p className="leading-[35px]">...</p>}

          {course.note && (
            <p className="mt-2 leading-[35px]">
              <span className="font-heading text-lg">Note: </span>
              {course.note}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}