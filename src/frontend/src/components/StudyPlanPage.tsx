import React, { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import starCluster from "../assets/Blue Stars.svg";
import tapeStrip from "../assets/Tape Piece.svg";
import arrowDoodle from "../assets/Arrow 1.svg";

/** Stage 1: what the person tells the plan-generator agent. */
export interface StudyPlanIntent {
  /** Which semester the generated plan should target, e.g. 1–8. */
  preferredSemester: number;
  /** Desired credit load for that semester, e.g. 12–21. */
  targetCredits: number;
  /** Free-text guidance passed straight through to the generator. */
  noteToAgent: string;
}

/** Why the generator put a given course into the plan. */
export type CourseSelectionReason =
  | "Assigned"
  | "Backlog"
  | "Elective"
  | "Retake";

/** Stage 2 output: a single course inside a generated plan. */
export interface PlannedCourse {
  id: string;
  courseCode: string;
  courseName: string;
  credits: number;
  instructor: string;
  /** Human-readable schedule summary, e.g. "Tuesday · 7:30 – 11:10". */
  schedule: string;
  selectionReason: CourseSelectionReason;
}

export type DayOfWeek = "MON" | "TUE" | "WED" | "THU" | "FRI" | "SAT" | "SUN";
/** Lecture vs. Lab session. */
export type SessionType = "LT" | "TH";

export interface TimetableBlock {
  id: string;
  courseCode: string;
  startTime: string;
  endTime: string;
  type: SessionType;
  /** True when this block overlaps another block in the same plan. */
  hasConflict: boolean;
}

export interface TimetableDay {
  day: DayOfWeek;
  blocks: TimetableBlock[];
}

export type RiskSeverity = "info" | "warning" | "blocker";

export interface AcademicRisk {
  id: string;
  message: string;
  severity: RiskSeverity;
}

export type PlanStatus = "Draft" | "Submitted for Review";

export interface RecommendedCourse {
  id: string;
  courseName: string;
  note: string;
}

export interface StudyPlanData {
  status: PlanStatus;
  courses: PlannedCourse[];
  timetable: TimetableDay[];
  risks: AcademicRisk[];
  recommendedCourses: RecommendedCourse[];
}

export interface StudyPlanProps {
  /** Stage 1 form state. Uncontrolled (internal state) if omitted. */
  intent?: StudyPlanIntent;
  onIntentChange?: (intent: StudyPlanIntent) => void;
  /** Fired when the person presses "Generate". */
  onGenerate?: (intent: StudyPlanIntent) => void;
  /** Fired when the person presses "Plan history". */
  onViewPlanHistory?: () => void;
  /** Stage 2 output + timetable + risks. Falls back to mock data. */
  planData?: StudyPlanData;
  /** Shows a busy state on the Generate button while a mutation is in flight. */
  isGenerating?: boolean;
  onSubmitPlan?: () => void;
}

// -----------------------------------------------------------------------
// Mock data — visual fallback only, fully decoupled from the UI below
// -----------------------------------------------------------------------

const MOCK_INTENT: StudyPlanIntent = {
  preferredSemester: 1,
  targetCredits: 15,
  noteToAgent: "",
};

const MOCK_COURSES: PlannedCourse[] = [
  {
    id: "c1",
    courseCode: "24C07",
    courseName: "Linear Algebra I",
    credits: 3,
    instructor: "Nguyen Van T.",
    schedule: "Tuesday · 7:30 – 11:10",
    selectionReason: "Assigned",
  },
  {
    id: "c2",
    courseCode: "24C15",
    courseName: "Data Structures & Algorithms",
    credits: 4,
    instructor: "Tran Thi H.",
    schedule: "Wednesday · 13:30 – 17:10",
    selectionReason: "Backlog",
  },
  {
    id: "c3",
    courseCode: "24C22",
    courseName: "Discrete Mathematics",
    credits: 3,
    instructor: "Le Van K.",
    schedule: "Thursday · 7:30 – 10:10",
    selectionReason: "Elective",
  },
  {
    id: "c4",
    courseCode: "24C05",
    courseName: "General Physics I",
    credits: 3,
    instructor: "Pham Minh D.",
    schedule: "Friday · 13:30 – 16:10",
    selectionReason: "Retake",
  },
];

const MOCK_TIMETABLE: TimetableDay[] = [
  { day: "MON", blocks: [] },
  {
    day: "TUE",
    blocks: [
      {
        id: "t1",
        courseCode: "24C07",
        startTime: "07:30",
        endTime: "11:10",
        type: "LT",
        hasConflict: false,
      },
    ],
  },
  {
    day: "WED",
    blocks: [
      {
        id: "t2",
        courseCode: "24C15",
        startTime: "13:30",
        endTime: "17:10",
        type: "LT",
        hasConflict: true,
      },
      {
        id: "t3",
        courseCode: "24C09",
        startTime: "15:00",
        endTime: "17:00",
        type: "TH",
        hasConflict: true,
      },
    ],
  },
  {
    day: "THU",
    blocks: [
      {
        id: "t4",
        courseCode: "24C22",
        startTime: "07:30",
        endTime: "10:10",
        type: "LT",
        hasConflict: false,
      },
    ],
  },
  {
    day: "FRI",
    blocks: [
      {
        id: "t5",
        courseCode: "24C05",
        startTime: "13:30",
        endTime: "16:10",
        type: "LT",
        hasConflict: false,
      },
      {
        id: "t6",
        courseCode: "24C05",
        startTime: "16:30",
        endTime: "18:10",
        type: "TH",
        hasConflict: false,
      },
    ],
  },
  { day: "SAT", blocks: [] },
  { day: "SUN", blocks: [] },
];

const MOCK_RECOMMENDED: RecommendedCourse[] = [
  { id: "r1", courseName: "Linear Algebra I", note: "Prerequisite gap" },
  { id: "r2", courseName: "Data Structures & Algorithms", note: "Keeps you on track" },
];

const MOCK_PLAN_DATA: StudyPlanData = {
  status: "Draft",
  courses: MOCK_COURSES,
  timetable: MOCK_TIMETABLE,
  risks: [],
  recommendedCourses: MOCK_RECOMMENDED,
};

// -----------------------------------------------------------------------
// Small style helpers
// -----------------------------------------------------------------------

function cn(...classes: Array<string | false | undefined | null>): string {
  return classes.filter(Boolean).join(" ");
}

/** Faint graph-paper grid for the page background. */
const notebookGridBackground: React.CSSProperties = {
  backgroundImage:
    "linear-gradient(to right, rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.05) 1px, transparent 1px)",
  backgroundSize: "22px 22px",
};

/** Ruled notebook lines, used behind the timetable + textarea. */
function ruledLinesBackground(lineColor = "rgba(0,0,0,0.16)"): React.CSSProperties {
  return {
    backgroundImage: `repeating-linear-gradient(to bottom, transparent, transparent 27px, ${lineColor} 28px)`,
  };
}

const reasonBadgeStyles: Record<CourseSelectionReason, string> = {
  Assigned: "bg-blue-100 text-blue-700",
  Backlog: "bg-orange-100 text-orange-700",
  Elective: "bg-purple-100 text-purple-700",
  Retake: "bg-red-100 text-red-700",
};

const severityStyles: Record<RiskSeverity, string> = {
  info: "border-l-4 border-sky-400 bg-sky-50 text-sky-800",
  warning: "border-l-4 border-amber-400 bg-amber-50 text-amber-800",
  blocker: "border-l-4 border-red-400 bg-red-50 text-red-800",
};

function planStatusStyles(status: PlanStatus): string {
  return status === "Draft"
    ? "bg-amber-100 text-amber-700"
    : "bg-emerald-100 text-emerald-700";
}

// -----------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------

export default function StudyPlan({
  intent: intentProp,
  onIntentChange,
  onGenerate,
  onSubmitPlan,
  onViewPlanHistory,
  planData = MOCK_PLAN_DATA,
  isGenerating = false,
}: StudyPlanProps) {

  const navigate = useNavigate();

  const [internalIntent, setInternalIntent] = useState<StudyPlanIntent>(
    intentProp ?? MOCK_INTENT,
  );
  const intent = intentProp ?? internalIntent;

  function updateIntent(patch: Partial<StudyPlanIntent>) {
    const next = { ...intent, ...patch };
    setInternalIntent(next);
    onIntentChange?.(next);
  }

  const semesterOptions = useMemo(
    () => Array.from({ length: 8 }, (_, i) => i + 1),
    [],
  );
  const creditOptions = useMemo(
    () => Array.from({ length: 10 }, (_, i) => 12 + i),
    [],
  );

  return (
    <div
      className="font-nunito relative w-full text-neutral-900"
      style={notebookGridBackground}
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-6 p-4 sm:p-6 lg:p-8">
        {/* -------------------------------------------------------------
            Row 1 — Intent form (Stage 1) + Current plan (Stage 2)
        -------------------------------------------------------------- */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[320px_1fr]">
          <IntentPanel
            intent={intent}
            semesterOptions={semesterOptions}
            creditOptions={creditOptions}
            isGenerating={isGenerating}
            onSemesterChange={(v) => updateIntent({ preferredSemester: v })}
            onCreditsChange={(v) => updateIntent({ targetCredits: v })}
            onNoteChange={(v) => updateIntent({ noteToAgent: v })}
            onGenerate={() => onGenerate?.(intent)}
          />
          <CurrentPlanPanel status={planData.status} courses={planData.courses} />
        </div>

        {/* -------------------------------------------------------------
            Row 2 — Weekly timetable, full width
        -------------------------------------------------------------- */}
        <TimetableSection timetable={planData.timetable} />

       {/* -------------------------------------------------------------
            Row 3 — Risk warnings + recommended courses
        -------------------------------------------------------------- */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <RiskPanel risks={planData.risks} />
          <RecommendedPanel recommended={planData.recommendedCourses} />
        </div>

        {/* -------------------------------------------------------------
            Plan history & Submit links (REPLACED SECTION)
        -------------------------------------------------------------- */}
        <div className="mt-4 flex items-center justify-between pb-2">
          
          {/* Left Side: Plan History */}
          <button
            type="button"
            onClick={() => navigate('/plan-history')}
            className="font-patrick-hand group flex items-center gap-2 text-lg text-neutral-800 transition hover:text-[#0085FF]"
          >
            Plan history
            <img
              src={arrowDoodle}
              alt=""
              aria-hidden="true"
              className="w-9 select-none transition-transform duration-200 group-hover:-translate-x-1 rotate-180" 
            />
          </button>

          {/* Right Side: Submit for Review (Task T-107) */}
          {planData.status === "Draft" && planData.courses.length > 0 && (
            <button
              type="button"
              onClick={onSubmitPlan}
              className="font-patrick-hand rounded-full bg-[#937FBD] px-6 py-2 text-lg text-white shadow-sm transition hover:scale-105"
            >
              Submit for review
            </button>
          )}

        </div>
      </div>
    </div>
  );
}

// -----------------------------------------------------------------------
// Sub-sections
// -----------------------------------------------------------------------

interface IntentPanelProps {
  intent: StudyPlanIntent;
  semesterOptions: number[];
  creditOptions: number[];
  isGenerating: boolean;
  onSemesterChange: (value: number) => void;
  onCreditsChange: (value: number) => void;
  onNoteChange: (value: string) => void;
  onGenerate: () => void;
}

function IntentPanel({
  intent,
  semesterOptions,
  creditOptions,
  isGenerating,
  onSemesterChange,
  onCreditsChange,
  onNoteChange,
  onGenerate,
}: IntentPanelProps) {
  return (
    <section className="flex flex-col gap-5 rounded-2xl bg-[#0085FF] p-6 text-white shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <label
          htmlFor="preferred-semester"
          className="font-patrick-hand text-xl leading-tight"
        >
          Preferred
          <br />
          semester
        </label>
        <select
          id="preferred-semester"
          value={intent.preferredSemester}
          onChange={(e) => onSemesterChange(Number(e.target.value))}
          className="w-20 rounded-full bg-white px-3 py-1.5 text-center text-neutral-900 shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
        >
          {semesterOptions.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      <div className="flex items-center justify-between gap-4">
        <label
          htmlFor="target-credits"
          className="font-patrick-hand text-xl leading-tight"
        >
          Target
          <br />
          credits
        </label>
        <select
          id="target-credits"
          value={intent.targetCredits}
          onChange={(e) => onCreditsChange(Number(e.target.value))}
          className="w-20 rounded-full bg-white px-3 py-1.5 text-center text-neutral-900 shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
        >
          {creditOptions.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-1 flex-col gap-2">
        <label htmlFor="note-to-agent" className="font-patrick-hand text-xl">
          Optional planning
        </label>
        <textarea
          id="note-to-agent"
          value={intent.noteToAgent}
          onChange={(e) => onNoteChange(e.target.value)}
          placeholder="e.g. avoid Friday mornings, pair with lab sections…"
          rows={4}
          className="font-nunito min-h-[110px] w-full resize-none bg-transparent px-1 py-1 text-sm text-white placeholder-white/60 focus:outline-none"
          style={ruledLinesBackground("rgba(255,255,255,0.35)")}
        />
      </div>

      <button
        type="button"
        onClick={onGenerate}
        disabled={isGenerating}
        className="font-patrick-hand self-end rounded-full bg-white px-6 py-2 text-lg text-[#0085FF] shadow transition hover:scale-105 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isGenerating ? "Generating…" : "Generate"}
      </button>
    </section>
  );
}

interface CurrentPlanPanelProps {
  status: PlanStatus;
  courses: PlannedCourse[];
}

function CurrentPlanPanel({ status, courses }: CurrentPlanPanelProps) {
  return (
    <section className="relative flex flex-col gap-4 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-neutral-200">
      <div className="flex items-start justify-between gap-4">
        <h2 className="font-patrick-hand text-3xl">Current plan</h2>
        <span
          className={cn(
            "rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide",
            planStatusStyles(status),
          )}
        >
          {status}
        </span>
        {/* Decorative star cluster: overlaps the corner via negative
            margins + rotation rather than absolute positioning, so it
            stays part of normal document flow. */}
        <img
          src={starCluster}
          alt=""
          aria-hidden="true"
          className="pointer-events-none -mt-8 -mr-4 hidden w-16 rotate-6 select-none sm:block"
        />
      </div>

      {courses.length === 0 ? (
        <p className="font-nunito text-sm text-neutral-500">
          No courses yet — fill in your intent and press Generate.
        </p>
      ) : (
        <ul className="font-nunito flex flex-col divide-y divide-neutral-200">
          {courses.map((course) => (
            <li key={course.id} className="flex flex-col gap-1 py-3 first:pt-0">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <p className="font-patrick-hand text-xl">{course.courseName}</p>
                <span
                  className={cn(
                    "rounded-full px-2 py-0.5 text-[11px] font-semibold",
                    reasonBadgeStyles[course.selectionReason],
                  )}
                >
                  {course.selectionReason}
                </span>
              </div>
              <p className="text-sm text-neutral-600">
                {course.courseCode} · {course.instructor}
              </p>
              <p className="text-sm text-neutral-600">
                {course.schedule} · {course.credits} credits
              </p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

interface TimetableSectionProps {
  timetable: TimetableDay[];
}

function TimetableSection({ timetable }: TimetableSectionProps) {
  return (
    <section
      className="rounded-2xl bg-[#FCFF61]/70 p-6 shadow-sm ring-1 ring-black/5"
      style={ruledLinesBackground("rgba(0,0,0,0.08)")}
    >
      <h2 className="font-patrick-hand mb-4 text-2xl">Weekly timetable</h2>

      {/* Horizontal scroll on small screens; full 7-column grid on desktop. */}
      <div className="overflow-x-auto">
        <div className="grid min-w-[720px] grid-cols-7 gap-3">
          {timetable.map((day) => (
            <div key={day.day} className="flex flex-col gap-2">
              <p className="font-patrick-hand text-center text-lg">{day.day}</p>
              <div className="flex flex-col gap-2">
                {day.blocks.length === 0 ? (
                  <p className="font-nunito text-center text-xs text-neutral-500">
                    —
                  </p>
                ) : (
                  day.blocks.map((block) => (
                    <div
                      key={block.id}
                      className={cn(
                        "font-nunito rounded-lg border px-2 py-2 text-xs shadow-sm",
                        block.hasConflict
                          ? "border-red-400 bg-red-100 text-red-700"
                          : "border-neutral-300 bg-white/90 text-neutral-800",
                      )}
                    >
                      <p className="font-semibold">{block.courseCode}</p>
                      <p>
                        {block.startTime} – {block.endTime}
                      </p>
                      <p className="text-[10px] uppercase tracking-wide opacity-70">
                        {block.type === "LT" ? "Lecture" : "Lab"}
                      </p>
                      {block.hasConflict && (
                        <p className="mt-1 font-semibold text-red-600">
                          Conflict
                        </p>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

interface RiskPanelProps {
  risks: AcademicRisk[];
}

function RiskPanel({ risks }: RiskPanelProps) {
  return (
    <section className="relative flex -rotate-1 flex-col gap-3 rounded-md bg-[#FADCE0] p-6 shadow-md">
      {/* Tape doodle overlaps the top edge via negative margin + rotation,
          not absolute positioning, so it stays in normal flow. */}
      <img
        src={tapeStrip}
        alt=""
        aria-hidden="true"
        className="pointer-events-none -mt-10 -mb-4 ml-6 w-14 rotate-3 self-start select-none"
      />
      <h2 className="font-patrick-hand text-2xl">Risk warning</h2>
      {risks.length === 0 ? (
        <p className="font-nunito text-neutral-700">None for now!</p>
      ) : (
        <ul className="font-nunito flex flex-col gap-2 text-sm text-neutral-800">
          {risks.map((risk) => (
            <li
              key={risk.id}
              className={cn("rounded-r-md px-3 py-2", severityStyles[risk.severity])}
            >
              {risk.message}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

interface RecommendedPanelProps {
  recommended: RecommendedCourse[];
}

function RecommendedPanel({ recommended }: RecommendedPanelProps) {
  return (
    <section className="flex flex-col gap-3 rounded-2xl bg-[#0085FF] p-6 text-white shadow-sm">
      <h2 className="font-patrick-hand text-2xl">Recommended courses</h2>
      {recommended.length === 0 ? (
        <p className="font-nunito text-sm text-white/80">
          Nothing to recommend right now.
        </p>
      ) : (
        <ul className="font-nunito flex flex-col gap-2 text-sm">
          {recommended.map((rec) => (
            <li
              key={rec.id}
              className="flex items-center justify-between gap-4 border-b border-white/20 pb-2 last:border-b-0 last:pb-0"
            >
              <span>{rec.courseName}</span>
              <span className="text-white/70">{rec.note}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}