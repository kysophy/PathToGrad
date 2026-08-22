import DonutProgress from './DonutProgress';

import type {
  DashboardData,
} from '../services/Dashboard';

import bunny from '../assets/Bunny.svg';
import starBlue from '../assets/Blue Stars.svg';
import flowerOrange from '../assets/Small Orange Flower.svg';
import planet from '../assets/planet 3.svg';
import smileyFace from '../assets/SF Chill.svg';


type StudentDashboardProps = {
  data: DashboardData;
};


export default function StudentDashboard({
  data,
}: StudentDashboardProps) {

  const graduationStatus =
    data.graduationCompleted
      ? 'Completed'
      : 'In progress';

  return (
    <div
      className="
        flex
        flex-col
        gap-6
        p-4
        sm:p-6
      "
    >

      <div>
        <h1
          className="
            font-heading
            text-3xl
            text-notebook-ink
            sm:text-4xl
          "
        >
          Academic Overview
        </h1>

        <p
          className="
            mt-1
            font-body
            text-sm
            text-neutral-600
          "
        >
          Student ID: {data.studentId}
        </p>
      </div>


      {/* =====================================================
          SUMMARY CARDS
          ===================================================== */}

      <div
        className="
          grid
          grid-cols-1
          gap-4
          sm:grid-cols-3
        "
      >

        {/* Earned Credits */}

        <div
          className="
            relative
            overflow-hidden
            rounded-2xl
            bg-[#FFBA69]
            p-5
          "
        >
          <span
            className="
              inline-block
              rounded-lg
              bg-white
              px-3
              py-1
              font-body
              text-sm
            "
          >
            Earned Credits
          </span>

          <p
            className="
              mt-4
              font-heading
              text-6xl
              text-notebook-ink
            "
          >
            {data.earnedCredits}
          </p>

          <img
            src={bunny}
            alt=""
            aria-hidden="true"
            className="
              pointer-events-none
              absolute
              bottom-2
              right-3
              h-16
              select-none
            "
          />
        </div>


        {/* Remaining Credits */}

        <div
          className="
            relative
            overflow-hidden
            rounded-2xl
            bg-[#67DE53]
            p-5
          "
        >
          <span
            className="
              inline-block
              rounded-lg
              bg-white
              px-3
              py-1
              font-body
              text-sm
            "
          >
            Remaining Credits
          </span>

          <p
            className="
              mt-4
              font-heading
              text-6xl
              text-notebook-ink
            "
          >
            {data.remainingCredits}
          </p>

          <img
            src={flowerOrange}
            alt=""
            aria-hidden="true"
            className="
              pointer-events-none
              absolute
              right-3
              top-3
              h-14
              select-none
            "
          />
        </div>


        {/* Graduation Status */}

        <div
          className="
            relative
            overflow-hidden
            rounded-2xl
            bg-[#0085FF]
            p-5
            text-white
          "
        >
          <span
            className="
              inline-block
              rounded-lg
              bg-white
              px-3
              py-1
              font-body
              text-sm
              text-neutral-800
            "
          >
            Graduation Status
          </span>

          <p
            className="
              mt-5
              font-heading
              text-3xl
            "
          >
            {graduationStatus}
          </p>

          <img
            src={starBlue}
            alt=""
            aria-hidden="true"
            className="
              pointer-events-none
              absolute
              bottom-3
              right-3
              h-12
              select-none
            "
          />
        </div>

      </div>


      {/* =====================================================
          GRADUATION PROGRESS
          ===================================================== */}

      <div
        className="
          grid
          grid-cols-1
          gap-4
          lg:grid-cols-2
        "
      >

        <section
          className="
            relative
            overflow-hidden
            rounded-2xl
            bg-[#FEE1E7]
            p-6
          "
        >

          <h2
            className="
              font-heading
              text-2xl
            "
          >
            Graduation Progress
          </h2>

          <div
            className="
              mt-5
              flex
              flex-col
              items-center
              gap-5
              sm:flex-row
            "
          >

            <DonutProgress
              percent={
                data.graduationPercent
              }
              label={
                `${data.graduationPercent}%`
              }
            />

            <div
              className="
                font-body
                text-sm
              "
            >
              <p>
                Earned:
                {' '}
                <strong>
                  {data.earnedCredits}
                </strong>
              </p>

              <p className="mt-2">
                Required:
                {' '}
                <strong>
                  {data.requiredCredits}
                </strong>
              </p>

              <p className="mt-2">
                Remaining:
                {' '}
                <strong>
                  {data.remainingCredits}
                </strong>
              </p>
            </div>

          </div>

          <img
            src={planet}
            alt=""
            aria-hidden="true"
            className="
              pointer-events-none
              absolute
              bottom-3
              right-3
              h-14
              opacity-70
            "
          />

        </section>


        {/* ===================================================
            ACADEMIC CONTEXT
            =================================================== */}

        <section
          className="
            rounded-2xl
            bg-[#FCFF61]
            p-6
          "
        >

          <h2
            className="
              font-heading
              text-2xl
            "
          >
            Academic Context
          </h2>

          <div
            className="
              mt-5
              grid
              gap-3
              font-body
              text-sm
            "
          >

            <p>
              <strong>
                Program:
              </strong>
              {' '}
              {data.programName}
            </p>

            <p>
              <strong>
                Curriculum:
              </strong>
              {' '}
              {
                data.curriculumVersion
                ?? 'Unavailable'
              }
            </p>

            <p>
              <strong>
                Profile:
              </strong>
              {' '}
              {
                data.profileComplete
                  ? 'Complete'
                  : 'Incomplete'
              }
            </p>

          </div>

        </section>

      </div>


      {/* =====================================================
          REQUIRED COURSE STATUS
          ===================================================== */}

      <section
        className="
          rounded-2xl
          border
          border-neutral-200
          bg-white
          p-6
        "
      >

        <div
          className="
            flex
            items-center
            gap-3
          "
        >
          <img
            src={smileyFace}
            alt=""
            aria-hidden="true"
            className="
              h-10
              w-10
            "
          />

          <h2
            className="
              font-heading
              text-2xl
            "
          >
            Required Course Status
          </h2>
        </div>


        <div
          className="
            mt-5
            grid
            grid-cols-1
            gap-5
            md:grid-cols-2
          "
        >

          {/* Completed */}

          <div
            className="
              rounded-xl
              bg-green-50
              p-4
            "
          >

            <h3
              className="
                font-heading
                text-lg
              "
            >
              Completed Required Courses
            </h3>

            {
              data.completedRequiredCourses
                .length === 0
                ? (
                    <p
                      className="
                        mt-3
                        font-body
                        text-sm
                        text-neutral-600
                      "
                    >
                      No verified required course
                      has been completed yet.
                    </p>
                  )
                : (
                    <ul
                      className="
                        mt-3
                        list-disc
                        pl-5
                        font-body
                        text-sm
                      "
                    >
                      {
                        data
                          .completedRequiredCourses
                          .map(
                            (courseCode) => (
                              <li
                                key={courseCode}
                              >
                                {courseCode}
                              </li>
                            ),
                          )
                      }
                    </ul>
                  )
            }

          </div>


          {/* Missing */}

          <div
            className="
              rounded-xl
              bg-red-50
              p-4
            "
          >

            <h3
              className="
                font-heading
                text-lg
              "
            >
              Missing Required Courses
            </h3>

            {
              data.missingRequiredCourses
                .length === 0
                ? (
                    <p
                      className="
                        mt-3
                        font-body
                        text-sm
                        text-neutral-600
                      "
                    >
                      No missing required courses.
                    </p>
                  )
                : (
                    <ul
                      className="
                        mt-3
                        list-disc
                        pl-5
                        font-body
                        text-sm
                      "
                    >
                      {
                        data
                          .missingRequiredCourses
                          .map(
                            (courseCode) => (
                              <li
                                key={courseCode}
                              >
                                {courseCode}
                              </li>
                            ),
                          )
                      }
                    </ul>
                  )
            }

          </div>

        </div>

      </section>

    </div>
  );
}