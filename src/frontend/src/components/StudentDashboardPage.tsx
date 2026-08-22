import DonutProgress from './DonutProgress';
import LinedRow from './LinedRow';

import type { DashboardData } from '../services/Dashboard';
export type { UpcomingPlan } from '../services/Dashboard';

// Reused from the existing asset library
import bunny from '../assets/Bunny.svg';
import starFilledBlue from '../assets/Blue Stars.svg';
import flowerOrange from '../assets/Small Orange Flower.svg';
import planet from '../assets/planet 3.svg';

import sleepyEgg from '../assets/Perf Egg.svg';
import eggWaving from '../assets/Check this out Egg.svg';
import eggSassy from '../assets/Angry Egg.svg';
import ribbonDoodle from '../assets/BF 3.svg';
import lightningBolt from '../assets/Lightning 2.svg';
import sparkleClusterPink from '../assets/Cool S.svg';
import partyHat from '../assets/Santa hat.svg';
import smileyFace from '../assets/SF Chill.svg';
import blueScribbleFlower from '../assets/Flower 2.svg';
import pinkButterfly from '../assets/BF 1.svg';

export type StudentDashboardProps = {
  data: DashboardData;
};

/**
 * StudentDashboard
 * -----------------------------------------------------------------------
 * Left content area only — meant to be rendered inside AppShell's
 * <Outlet/>. Purely presentational: everything comes from the `data`
 * prop, nothing is fetched here (see services/Dashboard.ts).
 *
 * Combines the two dashboards built in parallel: the decorated stats /
 * study-plan / advisor-note layout, plus the "Academic Context" and
 * "Required Course Status" sections driven by the real profile and
 * graduation-progress API. Fields the backend doesn't expose yet
 * (studentName, currentGPA, academicRisks, planProgress, nextClass,
 * advisorNote, upcomingPlans, workProgress) are optional on DashboardData
 * and fall back to placeholder copy here rather than being dropped.
 */
export default function StudentDashboard({ data }: StudentDashboardProps) {
  const {
    studentName,
    earnedCredits,
    requiredCredits,
    remainingCredits,
    currentGPA,
    academicRisks,
    graduationPercent,
    graduationCompleted,
    planProgress,
    nextClass,
    advisorNote,
    upcomingPlans,
    workProgress,
    programName,
    curriculumVersion,
    profileComplete,
    completedRequiredCourses,
    missingRequiredCourses,
  } = data;

  const risks = academicRisks
    ? Array.isArray(academicRisks)
      ? academicRisks
      : [academicRisks]
    : ['No risk data available yet.'];
  const plans = upcomingPlans ?? [];

  return (
    <div className="flex flex-col gap-6 p-4 sm:p-6">
      <div>
        <h1 className="font-heading text-3xl text-notebook-ink sm:text-4xl">
          Welcome back, {studentName ?? 'Student'}
        </h1>
        <p className="mt-1 font-body text-sm text-neutral-600">Student ID: {data.studentId}</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="relative overflow-hidden rounded-2xl bg-[#FFBA69] p-5">
          <span className="relative z-10 inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            Credits
          </span>
          <p className="relative z-10 mt-4 font-heading text-6xl text-notebook-ink">{earnedCredits}</p>
          <p className="relative z-10 mt-1 font-body text-sm text-neutral-800">
            of {requiredCredits} required
          </p>

          <img src={sleepyEgg} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '47.5%', top: '5.2%', width: '46.3%' }} />
          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute select-none opacity-90" style={{ left: '65.5%', top: '33.3%', width: '34.5%' }} />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#67DE53] p-5">
          <span className="relative z-10 inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            GPA
          </span>
          <p className="relative z-10 mt-4 font-heading text-6xl text-notebook-ink">
            {currentGPA ?? '—'}
          </p>

          <img src={flowerOrange} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '49.7%', top: '0%', width: '50.8%' }} />
          <img src={ribbonDoodle} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '1.7%', top: '29%', width: '48%' }} />
          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute select-none opacity-90" style={{ left: '61%', top: '35.5%', width: '22.6%' }} />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#0085FF] p-5">
          <span className="relative z-10 inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            Academic risks
          </span>
          <div className="relative z-10 mt-4 font-heading text-3xl text-white">
            {risks.length > 1 ? (
              <ul className="flex flex-col gap-1">
                {risks.map((risk) => (
                  <li key={risk}>{risk}</li>
                ))}
              </ul>
            ) : (
              <p>{risks[0]}</p>
            )}
          </div>

          <img src={lightningBolt} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '2.8%', top: '0%', width: '31.1%' }} />
          <img src={sparkleClusterPink} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '79.1%', top: '70.1%', width: '20.9%' }} />
        </div>
      </div>

      {/* Progress row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="relative overflow-hidden rounded-2xl bg-[#FEE1E7] p-5">
          <span className="relative z-10 inline-block rounded-lg bg-white px-3 py-1.5 font-body text-sm text-neutral-800">
            Graduation progress
          </span>
          <img src={partyHat} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '39.6%', top: '0%', width: '8.8%' }} />

          <div className="relative z-10 mt-4 flex items-center gap-6">
            <img src={smileyFace} alt="" aria-hidden="true" className="h-16 w-16 select-none" />
            <DonutProgress percent={graduationPercent} label={`${graduationPercent}%`} />
          </div>

          <p className="relative z-10 mt-4 font-body text-sm text-neutral-800">
            {graduationCompleted ? 'Requirements completed' : `Remaining credits: ${remainingCredits}`}
          </p>

          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute select-none opacity-80" style={{ left: '69.6%', top: '66.7%', width: '26.5%' }} />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#FCFF61] p-5">
          <span className="relative z-10 inline-block rounded-lg bg-white px-3 py-1.5 font-body text-sm text-neutral-800">
            Latest study plan progress
          </span>
          <img src={blueScribbleFlower} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '44.5%', top: '0%', width: '13.7%' }} />

          <div className="relative z-10 mt-4 flex items-center gap-6">
            <img src={eggWaving} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '15.4%', top: '20.1%', width: '18.8%' }} />
            <DonutProgress percent={planProgress ?? 0} label={`${planProgress ?? 0}%`} className="ml-auto" />
          </div>

          <p className="relative z-10 mt-4 font-body text-sm text-neutral-800">
            Upcoming class:
            <br />
            {nextClass ?? 'No upcoming class scheduled.'}
          </p>

          <img src={sparkleClusterPink} alt="" aria-hidden="true" className="pointer-events-none absolute select-none" style={{ left: '80.5%', top: '75.6%', width: '18.8%' }} />
        </div>
      </div>

      {/* Academic context, from the real student profile */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <section className="rounded-2xl border border-neutral-200 bg-white p-6">
          <h2 className="font-heading text-2xl text-notebook-ink">Academic Context</h2>
          <div className="mt-4 grid gap-2 font-body text-sm text-neutral-800">
            <p>
              <strong>Program:</strong> {programName}
            </p>
            <p>
              <strong>Curriculum:</strong> {curriculumVersion ?? 'Unavailable'}
            </p>
            <p>
              <strong>Profile:</strong> {profileComplete ? 'Complete' : 'Incomplete'}
            </p>
          </div>
        </section>

        <section className="rounded-2xl border border-neutral-200 bg-white p-6">
          <h2 className="font-heading text-2xl text-notebook-ink">Required Course Status</h2>
          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-xl bg-green-50 p-4">
              <h3 className="font-heading text-lg">Completed</h3>
              {completedRequiredCourses.length === 0 ? (
                <p className="mt-2 font-body text-sm text-neutral-600">
                  No verified required course has been completed yet.
                </p>
              ) : (
                <ul className="mt-2 list-disc pl-5 font-body text-sm">
                  {completedRequiredCourses.map((courseCode) => (
                    <li key={courseCode}>{courseCode}</li>
                  ))}
                </ul>
              )}
            </div>

            <div className="rounded-xl bg-red-50 p-4">
              <h3 className="font-heading text-lg">Missing</h3>
              {missingRequiredCourses.length === 0 ? (
                <p className="mt-2 font-body text-sm text-neutral-600">No missing required courses.</p>
              ) : (
                <ul className="mt-2 list-disc pl-5 font-body text-sm">
                  {missingRequiredCourses.map((courseCode) => (
                    <li key={courseCode}>{courseCode}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </section>
      </div>

      {/* Lined-paper plans section + overlapping advisor's-feedback note.
          The note overlaps via a negative margin + rotate on lg screens
          (normal flow, not position:absolute) and simply stacks below on
          smaller screens. */}
      <div className="flex flex-col lg:flex-row lg:items-start">
        <div className="min-w-0 flex-1 pb-4">
          <p className="-rotate-6 font-heading text-xl text-[#F291A3]">100%</p>

          <LinedRow bold className="flex items-center justify-between">
            <span className="rounded bg-yellow-200/80 px-2 py-0.5">Upcoming plans:</span>
            <span>Due dates:</span>
          </LinedRow>

          {plans.length === 0 ? (
            <LinedRow className="text-neutral-500">No upcoming plan items.</LinedRow>
          ) : (
            plans.map((plan, i) => (
              <LinedRow key={plan.id} wrap className="flex items-start justify-between gap-4">
                <span>
                  {i + 1}. {plan.taskName}
                </span>
                <span className="shrink-0">{plan.dueDate}</span>
              </LinedRow>
            ))
          )}

          <div className="flex items-center gap-2 border-b border-black/40 py-1">
            <img src={bunny} alt="" aria-hidden="true" className="h-8 w-auto select-none" />
          </div>

          {workProgress && (
            <>
              <LinedRow bold className="mt-2">
                Work progress:
              </LinedRow>

              <div className="mt-3 flex h-2 w-full max-w-md overflow-hidden rounded-full bg-neutral-200">
                <div className="h-full bg-[#67DE53]" style={{ width: `${workProgress.completed}%` }} />
                <div className="h-full bg-[#FD6363]" style={{ width: `${workProgress.atRisk}%` }} />
              </div>
            </>
          )}

          <div className="mt-4 flex items-center gap-3">
            <img src={smileyFace} alt="" aria-hidden="true" className="h-10 w-10 select-none" />
            <img src={starFilledBlue} alt="" aria-hidden="true" className="h-8 w-auto select-none" />
            <img src={starFilledBlue} alt="" aria-hidden="true" className="h-5 w-auto select-none opacity-80" />
          </div>
        </div>

        <div className="relative mt-6 w-full max-w-xs shrink-0 self-center lg:-ml-10 lg:mt-16 lg:w-72 lg:self-start">
          <img
            src={pinkButterfly}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -top-6 left-6 h-12 w-auto select-none"
          />

          <div className="relative rotate-2 rounded-lg bg-[#67DE53] p-6 shadow-lg">
            {/* washi-tape accent, overlapping the note's top edge */}
            <div className="absolute -top-4 right-8 h-9 w-4 -rotate-12 rounded-sm bg-[#0085FF]/80" />

            <p className="-rotate-2 font-heading text-lg text-notebook-ink">
              Advisor's feedback:
              <br />
              {advisorNote ?? 'No note from your advisor yet.'}
            </p>
          </div>

          <img
            src={eggSassy}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-10 -right-4 h-28 w-auto select-none"
          />
        </div>
      </div>
    </div>
  );
}
