import DonutProgress from './DonutProgress';
import LinedRow from './LinedRow';
import type { DashboardData } from '../services/Dashboard';
import { MOCK_DASHBOARD_DATA } from '../services/Dashboard';

// Reused from the existing asset library
import bunny from '../assets/Bunny.svg';
import starFilledBlue from '../assets/Blue Stars.svg';
import flowerOrange from '../assets/Small Orange Flower.svg';
import planet from '../assets/planet 3.svg';

// New placeholders for this screen — see the note inside each file.
// TODO: placeholder assets — swap each for its real Figma doodle export.
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

/**
 * StudentDashboard
 * -----------------------------------------------------------------------
 * Left content area only — meant to be rendered inside AppShell's
 * <Outlet/>. Does not render the top header or the chat sidebar.
 *
 * Purely presentational: takes `data: DashboardData` as a prop instead
 * of fetching anything itself, so the page that mounts this can source
 * `data` from a `useQuery` call once the API exists (see
 * src/services/dashboard.ts) without this file changing at all.
 */
export type StudentDashboardProps = {
  data?: DashboardData;
};

export default function StudentDashboard({ data = MOCK_DASHBOARD_DATA }: StudentDashboardProps) {
  const {
    studentName,
    earnedCredits,
    currentGPA,
    academicRisks,
    graduationProgress,
    studyPlanProgress,
    upcomingPlans,
    advisorsFeedback,
    workProgress,
  } = data;

  return (
    <div className="flex flex-col gap-6 p-4 sm:p-6">
      <h1 className="font-heading text-3xl text-notebook-ink sm:text-4xl">
        Welcome back, {studentName}
      </h1>

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="relative overflow-hidden rounded-2xl bg-[#FFBA69] p-5">
          <span className="inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            Credits
          </span>
          <p className="mt-4 font-heading text-6xl text-notebook-ink">{earnedCredits}</p>
          <img src={sleepyEgg} alt="" aria-hidden="true" className="pointer-events-none absolute right-3 top-4 h-16 w-auto select-none" />
          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute bottom-2 right-2 h-10 w-auto select-none opacity-90" />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#67DE53] p-5">
          <span className="inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            GPA
          </span>
          <p className="mt-4 font-heading text-6xl text-notebook-ink">{currentGPA}</p>
          <img src={flowerOrange} alt="" aria-hidden="true" className="pointer-events-none absolute right-2 top-2 h-14 w-auto select-none" />
          <img src={ribbonDoodle} alt="" aria-hidden="true" className="pointer-events-none absolute bottom-2 left-2 h-10 w-auto select-none" />
          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute bottom-2 right-2 h-8 w-auto select-none opacity-90" />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#0085FF] p-5">
          <span className="inline-block rounded-lg bg-white px-3 py-1 font-body text-sm text-neutral-800">
            Academic risks
          </span>
          <p className="mt-4 font-heading text-3xl text-white">{academicRisks}</p>
          <img src={lightningBolt} alt="" aria-hidden="true" className="pointer-events-none absolute left-3 top-3 h-14 w-auto select-none" />
          <img src={sparkleClusterPink} alt="" aria-hidden="true" className="pointer-events-none absolute bottom-2 right-2 h-14 w-auto select-none" />
        </div>
      </div>

      {/* Progress row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="relative overflow-hidden rounded-2xl bg-[#FEE1E7] p-5">
          <span className="inline-block rounded-lg bg-white px-3 py-1.5 font-body text-sm text-neutral-800">
            Graduation progress
          </span>
          <img src={partyHat} alt="" aria-hidden="true" className="pointer-events-none absolute right-8 top-2 h-8 w-auto select-none" />

          <div className="mt-4 flex items-center gap-6">
            <img src={smileyFace} alt="" aria-hidden="true" className="h-16 w-16 select-none" />
            <DonutProgress percent={graduationProgress.percent} />
          </div>

          <p className="mt-4 font-body text-sm text-neutral-800">
            Remaining credits: {graduationProgress.remainingCredits}
          </p>
          <img src={planet} alt="" aria-hidden="true" className="pointer-events-none absolute -bottom-2 right-10 h-14 w-auto select-none opacity-80" />
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-[#FCFF61] p-5">
          <span className="inline-block rounded-lg bg-white px-3 py-1.5 font-body text-sm text-neutral-800">
            Latest study plan progress
          </span>
          <img src={blueScribbleFlower} alt="" aria-hidden="true" className="pointer-events-none absolute right-8 top-2 h-10 w-auto select-none" />

          <div className="mt-4 flex items-center gap-6">
            <img src={eggWaving} alt="" aria-hidden="true" className="h-20 w-auto select-none" />
            <DonutProgress percent={studyPlanProgress.percent} label={`${studyPlanProgress.percent}%`} />
          </div>

          <p className="mt-4 font-body text-sm text-neutral-800">
            Upcoming class:
            <br />
            {studyPlanProgress.upcomingClass}
          </p>
          <img src={sparkleClusterPink} alt="" aria-hidden="true" className="pointer-events-none absolute bottom-2 right-2 h-12 w-auto select-none" />
        </div>
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

          {upcomingPlans.map((plan, i) => (
            <LinedRow key={plan.id} className="flex items-center justify-between gap-4">
              <span className="truncate">
                {i + 1}. {plan.taskName}
              </span>
              <span className="shrink-0">{plan.dueDate}</span>
            </LinedRow>
          ))}

          <div className="flex items-center gap-2">
            <img src={bunny} alt="" aria-hidden="true" className="h-8 w-auto select-none" />
          </div>

          <LinedRow bold className="mt-4">
            Work progress:
          </LinedRow>

          <div className="flex h-2 w-full max-w-md overflow-hidden rounded-full bg-neutral-200">
            <div className="h-full bg-[#67DE53]" style={{ width: `${workProgress.completed}%` }} />
            <div className="h-full bg-[#FD6363]" style={{ width: `${workProgress.atRisk}%` }} />
          </div>

          <div className="mt-4 flex items-center gap-3">
            <img src={smileyFace} alt="" aria-hidden="true" className="h-10 w-10 select-none" />
            <img src={starFilledBlue} alt="" aria-hidden="true" className="h-8 w-auto select-none" />
            <img src={starFilledBlue} alt="" aria-hidden="true" className="h-5 w-auto select-none opacity-80" />
          </div>
        </div>

        <div className="relative mt-6 w-full max-w-xs shrink-0 self-center lg:-ml-10 lg:mt-16 lg:self-start">
          <img
            src={pinkButterfly}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -top-6 left-6 h-12 w-auto select-none"
          />

          <div className="relative rotate-2 rounded-lg bg-[#67DE53] p-6 shadow-lg">
            {/* washi-tape accent */}
            <div className="absolute -top-3 left-8 h-8 w-4 -rotate-12 rounded-sm bg-[#0085FF]/80" />

            <p className="-rotate-2 font-heading text-lg text-notebook-ink">
              Advisor's feedback:
              <br />
              {advisorsFeedback}
            </p>
          </div>

          <img
            src={eggSassy}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-8 right-0 h-24 w-auto select-none"
          />
        </div>
      </div>
    </div>
  );
}