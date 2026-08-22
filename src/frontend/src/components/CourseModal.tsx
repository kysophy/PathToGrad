import {
  useEffect,
  useState,
} from 'react';

import type {
  Course,
  CourseDetails,
} from '../services/Course';

import {
  getCourseDetails,
} from '../services/Course';

import LinedRow
  from './LinedRow';


type CourseModalProps = {
  course: Course | null;

  termId: string;

  termName: string;

  onClose: () => void;
};


function formatEligibility(
  value: boolean | null,
): string {

  if (value === null) {
    return 'Cannot be verified';
  }

  return value
    ? 'Eligible'
    : 'Not eligible';
}


export default function CourseModal({
  course,
  termId,
  termName,
  onClose,
}: CourseModalProps) {

  const [
    details,
    setDetails,
  ] = useState<
    CourseDetails | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState('');


  useEffect(() => {

    if (!course) {
      return;
    }


    function onKeyDown(
      event: KeyboardEvent,
    ) {
      if (
        event.key === 'Escape'
      ) {
        onClose();
      }
    }


    window.addEventListener(
      'keydown',
      onKeyDown,
    );


    return () => {
      window.removeEventListener(
        'keydown',
        onKeyDown,
      );
    };

  }, [
    course,
    onClose,
  ]);


  useEffect(() => {

    let active = true;


    async function loadDetails() {

      if (
        !course
        || !termId
      ) {
        return;
      }


      try {
        setLoading(true);
        setError('');
        setDetails(null);

        const result =
          await getCourseDetails(
            course.id,
            termId,
          );

        if (active) {
          setDetails(result);
        }

      } catch (err) {

        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : (
                  'Unable to load '
                  + 'course details.'
                ),
          );
        }

      } finally {

        if (active) {
          setLoading(false);
        }
      }
    }


    loadDetails();


    return () => {
      active = false;
    };

  }, [
    course,
    termId,
  ]);


  if (!course) {
    return null;
  }


  return (
    <div
      className="
        fixed
        inset-0
        z-50
        flex
        items-center
        justify-center
        bg-black/50
        p-4
      "
      onClick={onClose}
      role="presentation"
    >

      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="course-modal-title"
        onClick={(event) => {
          event.stopPropagation();
        }}
        className="
          relative
          max-h-[90vh]
          w-full
          max-w-2xl
          overflow-y-auto
          rounded-2xl
          bg-[#67DE53]
          p-6
          text-neutral-900
          shadow-xl
          sm:p-8
        "
      >

        <button
          type="button"
          onClick={onClose}
          aria-label="Close"
          className="
            absolute
            right-4
            top-4
            flex
            h-8
            w-8
            items-center
            justify-center
            rounded-full
            bg-black/10
            hover:bg-black/20
          "
        >
          ×
        </button>


        <h2
          id="course-modal-title"
          className="
            pr-10
            font-heading
            text-3xl
          "
        >
          {course.id}
        </h2>

        <p
          className="
            mt-1
            font-body
            text-lg
          "
        >
          {course.name}
        </p>


        <div className="mt-6">

          <LinedRow bold>
            Course Information
          </LinedRow>

          <LinedRow>
            Credits: {course.credits}
          </LinedRow>

          <LinedRow>
            Academic term:
            {' '}
            {termName}
          </LinedRow>

        </div>


        {
          loading
          && (
            <div
              className="
                mt-6
                rounded-lg
                bg-white/70
                p-4
                font-body
                text-sm
              "
            >
              Loading eligibility information...
            </div>
          )
        }


        {
          error
          && (
            <div
              className="
                mt-6
                rounded-lg
                bg-red-100
                p-4
                font-body
                text-sm
                text-red-700
              "
            >
              {error}
            </div>
          )
        }


        {
          details
          && (
            <>

              {/* ===============================================
                  PREREQUISITES
                  =============================================== */}

              <div className="mt-6">

                <LinedRow bold>
                  Prerequisite Validation
                </LinedRow>

                <LinedRow>
                  Overall:
                  {' '}
                  {
                    formatEligibility(
                      details
                        .prerequisites
                        .eligible,
                    )
                  }
                </LinedRow>


                {
                  details
                    .prerequisites
                    .prerequisites
                    .length === 0
                    ? (
                        <LinedRow>
                          No prerequisite is configured.
                        </LinedRow>
                      )
                    : (
                        details
                          .prerequisites
                          .prerequisites
                          .map(
                            (item) => (
                              <LinedRow
                                key={
                                  item.course_code
                                }
                              >
                                {
                                  item.course_code
                                }
                                {' — '}
                                {
                                  item.status
                                }
                              </LinedRow>
                            ),
                          )
                      )
                }

              </div>


              {/* ===============================================
                  OFFERING STATUS
                  =============================================== */}

              <div className="mt-6">

                <LinedRow bold>
                  Course Availability
                </LinedRow>

                <LinedRow>
                  Offered in selected term:
                  {' '}
                  {
                    details
                      .eligibility
                      .offered
                      ? 'Yes'
                      : 'No'
                  }
                </LinedRow>

                <LinedRow>
                  Final eligibility:
                  {' '}
                  {
                    formatEligibility(
                      details
                        .eligibility
                        .eligible,
                    )
                  }
                </LinedRow>

              </div>


              {/* ===============================================
                  CLASS SECTIONS
                  =============================================== */}

              <div className="mt-6">

                <LinedRow bold>
                  Available Class Sections
                </LinedRow>


                {
                  details
                    .eligibility
                    .sections
                    .length === 0
                    ? (
                        <LinedRow>
                          No active class-section data
                          is available for this term.
                        </LinedRow>
                      )
                    : (
                        details
                          .eligibility
                          .sections
                          .map(
                            (section) => (
                              <div
                                key={
                                  section.section_id
                                }
                                className="
                                  mt-4
                                  rounded-xl
                                  bg-white/60
                                  p-4
                                "
                              >

                                <p
                                  className="
                                    font-heading
                                    text-lg
                                  "
                                >
                                  Section
                                  {' '}
                                  {
                                    section.section_code
                                  }
                                </p>

                                <p
                                  className="
                                    mt-1
                                    font-body
                                    text-sm
                                  "
                                >
                                  Capacity:
                                  {' '}
                                  {
                                    section.capacity
                                  }
                                </p>


                                <div
                                  className="
                                    mt-3
                                  "
                                >

                                  <p
                                    className="
                                      font-body
                                      text-sm
                                      font-semibold
                                    "
                                  >
                                    Meeting times
                                  </p>


                                  {
                                    section
                                      .meetings
                                      .length === 0
                                      ? (
                                          <p
                                            className="
                                              mt-1
                                              font-body
                                              text-sm
                                            "
                                          >
                                            No meeting-time
                                            data available.
                                          </p>
                                        )
                                      : (
                                          section
                                            .meetings
                                            .map(
                                              (
                                                meeting,
                                                index,
                                              ) => (
                                                <p
                                                  key={
                                                    `${meeting.day_of_week}-${index}`
                                                  }
                                                  className="
                                                    mt-1
                                                    font-body
                                                    text-sm
                                                  "
                                                >
                                                  {
                                                    meeting
                                                      .day_of_week
                                                  }
                                                  {': '}
                                                  {
                                                    meeting
                                                      .start_time
                                                  }
                                                  {' - '}
                                                  {
                                                    meeting
                                                      .end_time
                                                  }
                                                </p>
                                              ),
                                            )
                                        )
                                  }

                                </div>

                              </div>
                            ),
                          )
                      )
                }

              </div>


              {/* ===============================================
                  WARNINGS
                  =============================================== */}

              {
                (
                  details
                    .prerequisites
                    .warnings
                    .length > 0

                  ||

                  details
                    .eligibility
                    .warnings
                    .length > 0
                )
                && (
                  <div
                    className="
                      mt-6
                      rounded-xl
                      bg-yellow-100
                      p-4
                    "
                  >

                    <p
                      className="
                        font-heading
                        text-lg
                      "
                    >
                      Warnings
                    </p>


                    {
                      Array.from(
                        new Set([
                          ...details
                            .prerequisites
                            .warnings,

                          ...details
                            .eligibility
                            .warnings,
                        ]),
                      ).map(
                        (warning) => (
                          <p
                            key={warning}
                            className="
                              mt-2
                              font-body
                              text-sm
                            "
                          >
                            {warning}
                          </p>
                        ),
                      )
                    }

                  </div>
                )
              }

            </>
          )
        }

      </div>

    </div>
  );
}