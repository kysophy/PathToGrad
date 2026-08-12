import type { Course } from '../services/Course';
import leaf from '../assets/Leafies.svg';
import bunny from '../assets/Bunny.svg';
import swoosh from '../assets/Planet 2.svg';

type CourseCardProps = {
  course: Course;
  onSelect: (course: Course) => void;
};

const BG_MAP = {
  yellow: 'bg-[#FCFF61]',
  pink: 'bg-[#F7BEC8]',
};

export default function CourseCard({ course, onSelect }: CourseCardProps) {
  return (
    <button
      type="button"
      onClick={() => onSelect(course)}
      className={`relative flex flex-col overflow-hidden rounded-[28px] p-5 text-left font-body ${BG_MAP[course.color]}`}
    >
      {course.color === 'yellow' && (
        <img
          src={leaf}
          alt=""
          aria-hidden="true"
          className="pointer-events-none absolute right-3 top-6 h-2/3 w-auto select-none opacity-90"
        />
      )}

      {course.color === 'pink' && (
        <>
          <img
            src={swoosh}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute bottom-4 right-2 w-2/3 -scale-x-100 select-none opacity-70"
          />
          <img
            src={bunny}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute bottom-8 right-4 w-1/3 select-none"
          />
        </>
      )}

      <div className="relative z-10 flex flex-col gap-2">
        <p className="text-sm text-neutral-800">Course ID: {course.id}</p>
        <p className="text-sm text-neutral-800">Course name: {course.name}</p>

        <p className="mt-4 text-sm text-neutral-800">Credits: {course.credits}</p>
        <p className="text-sm text-neutral-800">
          Prerequisite chain:
          {course.prerequisiteChain.map((p) => (
            <span key={p} className="block">
              {p}
            </span>
          ))}
        </p>
        <p className="text-sm text-neutral-800">Status: {course.status}</p>
      </div>
    </button>
  );
}