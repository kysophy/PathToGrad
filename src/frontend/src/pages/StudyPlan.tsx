import { useEffect, useMemo, useState } from 'react';

import StudyPlan, {
  type DayOfWeek,
  type PlannedCourse,
  type StudyPlanData,
  type StudyPlanIntent,
  type TimetableDay,
} from '../components/StudyPlanPage';
import {
  generateExplainedPlan,
  type ExplainedPlanResponse,
  type TimetableSlot,
} from '../services/Agent';

import { getProfile } from '../services/Profile';

const DAYS: DayOfWeek[] = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

const DAY_MAP: Record<string, DayOfWeek> = {
  Monday: 'MON',
  Tuesday: 'TUE',
  Wednesday: 'WED',
  Thursday: 'THU',
  Friday: 'FRI',
  Saturday: 'SAT',
  Sunday: 'SUN',
};

const EMPTY_PLAN: StudyPlanData = {
  status: 'Draft',
  courses: [],
  timetable: DAYS.map((day) => ({ day, blocks: [] })),
  risks: [],
  recommendedCourses: [],
};

function clock(value: string): string {
  return value.slice(0, 5);
}

function toReason(value: string): PlannedCourse['selectionReason'] {
  if (value === 'ASSIGNED_THIS_SEMESTER') return 'Assigned';
  if (value === 'BACKLOG_FROM_SEMESTER_N') return 'Backlog';
  if (value === 'ELECTIVE_FILL') return 'Elective';
  return 'Retake';
}

function toSeverity(value: string): StudyPlanData['risks'][number]['severity'] {
  if (value === 'critical') return 'blocker';
  if (value === 'info') return 'info';
  return 'warning';
}

function scheduleFor(code: string, slots: TimetableSlot[]): string {
  const hits = slots.filter((slot) => slot.course_code === code);
  if (hits.length === 0) return 'No meeting this term';
  return hits
    .map(
      (slot) =>
        `${slot.day_of_week} · ${clock(slot.start_time)} – ${clock(slot.end_time)}`,
    )
    .join(' · ');
}

function overlaps(
  a: { startTime: string; endTime: string },
  b: { startTime: string; endTime: string },
): boolean {
  return a.startTime < b.endTime && b.startTime < a.endTime;
}

function mapTimetable(slots: TimetableSlot[]): TimetableDay[] {
  const grouped: Record<DayOfWeek, TimetableDay> = {
    MON: { day: 'MON', blocks: [] },
    TUE: { day: 'TUE', blocks: [] },
    WED: { day: 'WED', blocks: [] },
    THU: { day: 'THU', blocks: [] },
    FRI: { day: 'FRI', blocks: [] },
    SAT: { day: 'SAT', blocks: [] },
    SUN: { day: 'SUN', blocks: [] },
  };
  for (const slot of slots) {
    const day = DAY_MAP[slot.day_of_week];
    if (!day) continue;
    grouped[day].blocks.push({
      id: `${slot.section_id}-${slot.meeting_type}-${slot.start_time}`,
      courseCode: slot.course_code,
      startTime: clock(slot.start_time),
      endTime: clock(slot.end_time),
      type: slot.meeting_type === 'TH' ? 'TH' : 'LT',
      hasConflict: false,
    });
  }
  return DAYS.map((day) => {
    const blocks = grouped[day].blocks.map((block) => ({ ...block }));
    for (let i = 0; i < blocks.length; i += 1) {
      for (let j = i + 1; j < blocks.length; j += 1) {
        if (overlaps(blocks[i], blocks[j])) {
          blocks[i].hasConflict = true;
          blocks[j].hasConflict = true;
        }
      }
    }
    return { day, blocks };
  });
}

function mapPlan(payload: ExplainedPlanResponse): StudyPlanData {
  return {
    status: 'Draft',
    courses: payload.items.map((item) => ({
      id: item.course_id,
      courseCode: item.course_code,
      courseName: payload.names[item.course_code] ?? item.course_code,
      credits: item.credits,
      instructor: item.section_id,
      schedule: scheduleFor(item.course_code, payload.timetable),
      selectionReason: toReason(item.selection_reason),
    })),
    timetable: mapTimetable(payload.timetable),
    risks: [
      ...payload.warnings.map((warning, index) => ({
        id: `warn-${index}`,
        message: warning,
        severity: 'warning' as const,
      })),
      ...payload.risks.map((risk) => ({
        id: risk.code,
        message: risk.message,
        severity: toSeverity(risk.severity),
      })),
    ],
    recommendedCourses: payload.recommended.map((row) => ({
      id: row.course_code,
      courseName: row.course_name,
      note: row.note,
    })),
    explanation: payload.explanation,
    explanationSource: payload.explanation_source,
  };
}

export default function StudyPlanPage() {
  const [intent, setIntent] = useState<StudyPlanIntent>({
    preferredSemester: 1,
    targetCredits: 15,
    noteToAgent: '',
  });

  useEffect(() => {
    let active = true;

    getProfile()
      .then((profile) => {
        if (!active) return;

        setIntent((prev) => ({
          ...prev,
          preferredSemester: profile.current_semester,
          targetCredits: profile.target_credit_load,
        }));
      })
      .catch((error) => {
        console.error('Could not load profile for study plan:', error);
      });

    return () => {
      active = false;
    };
  }, []);
  
  const [planData, setPlanData] = useState<StudyPlanData>(EMPTY_PLAN);
  const [isGenerating, setIsGenerating] = useState(false);

  const onGenerate = useMemo(
    () => async (next: StudyPlanIntent) => {
      setIsGenerating(true);
      try {
        const payload = await generateExplainedPlan({
          targetCredits: next.targetCredits,
          note: next.noteToAgent,
        });
        setPlanData(mapPlan(payload));
      } catch (error) {
        const message =
          error instanceof Error ? error.message : 'Could not generate a plan.';
        setPlanData((prev) => ({
          ...prev,
          risks: [
            {
              id: 'generate-error',
              message,
              severity: 'blocker',
            },
          ],
        }));
      } finally {
        setIsGenerating(false);
      }
    },
    [],
  );

  return (
    <StudyPlan
      intent={intent}
      onIntentChange={setIntent}
      onGenerate={onGenerate}
      planData={planData}
      isGenerating={isGenerating}
    />
  );
}
