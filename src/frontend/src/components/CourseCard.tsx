import type {
  Course,
} from '../services/Course';

import leaf
  from '../assets/Leafies.svg';

import bunny
  from '../assets/Bunny.svg';

import swoosh
  from '../assets/Planet 2.svg';


type CourseCardProps = {
  course: Course;

  onSelect: (
    course: Course,
  ) => void;
};

const BG_MAP = {
  yellow: 'bg-[#FCFF61]',
  pink: 'bg-[#F7BEC8]',
};


function getStatusLabel(
  course: Course,
): string {

  if (
    course.eligible === null
  ) {
    return 'Cannot verify eligibility';
  }

  if (
    course.eligible === true
  ) {
    return 'Eligible and offered';
  }

  if (
    course.prerequisiteEligible
    === false
  ) {
    return (
      'Prerequisites not satisfied'
    );
  }

  if (
    course.offered === false
  ) {
    return (
      'Not offered in selected term'
    );
  }

  return 'Not eligible';
}


export default function CourseCard({
  course,
  onSelect,
}: CourseCardProps) {

  const status =
    getStatusLabel(course);


  return (
    <button
      type="button"
      onClick={() => {
        onSelect(course);
      }}
      className={
        `
        relative
        flex
        w-[230px]
        shrink-0
        snap-start
        flex-col
        overflow-hidden
        rounded-[28px]
        p-5
        text-left
        font-body
        sm:w-[250px]
        ${BG_MAP[course.color]}
        `
      }
    >

      {
        course.color
        === 'yellow'
        && (
          <img
            src={leaf}
            alt=""
            aria-hidden="true"
            className="
              pointer-events-none
              absolute
              right-3
              top-6
              h-2/3
              w-auto
              select-none
              opacity-40
            "
          />
        )
      }


      {
        course.color
        === 'pink'
        && (
          <>
            <img
              src={swoosh}
              alt=""
              aria-hidden="true"
              className="
                pointer-events-none
                absolute
                bottom-4
                right-2
                w-2/3
                -scale-x-100
                select-none
                opacity-40
              "
            />

            <img
              src={bunny}
              alt=""
              aria-hidden="true"
              className="
                pointer-events-none
                absolute
                bottom-8
                right-4
                w-1/3
                select-none
                opacity-60
              "
            />
          </>
        )
      }


      <div
        className="
          relative
          z-10
          flex
          w-full
          flex-col
          gap-2
        "
      >

        <p
          className="
            text-xs
            text-neutral-600
          "
        >
          Course Code
        </p>

        <p
          className="
            font-heading
            text-lg
            text-neutral-900
          "
        >
          {course.id}
        </p>


        <p
          className="
            mt-1
            text-sm
            text-neutral-800
          "
        >
          {course.name}
        </p>


        <p
          className="
            mt-3
            text-sm
          "
        >
          Credits:
          {' '}
          <strong>
            {course.credits}
          </strong>
        </p>


        <div
          className="
            mt-2
            text-sm
          "
        >
          <p className="font-semibold">
            Prerequisites
          </p>

          {
            course.prerequisiteChain
              .length === 0
              ? (
                  <p>None configured</p>
                )
              : (
                  course
                    .prerequisiteChain
                    .map(
                      (code) => (
                        <p key={code}>
                          {code}
                        </p>
                      ),
                    )
                )
          }
        </div>


        <div
          className="
            mt-3
            rounded-lg
            bg-white/80
            px-3
            py-2
            text-xs
            font-semibold
          "
        >
          {status}
        </div>

      </div>

    </button>
  );
}