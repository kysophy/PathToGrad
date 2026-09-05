import { apiRequest } from './api';
import { getCurrentStudentId } from './session';

export const DEFAULT_TERM_ID = 'TERM-2026-1';

export type AgentChatResponse = {
  reply: string;
  intent: string;
  generation_mode: 'LLM' | 'Fallback';
  used_template: boolean;
  run_id: string | null;
};

export type PlanItem = {
  course_id: string;
  course_code: string;
  section_id: string;
  credits: number;
  selection_reason: string;
};

export type PlanExclusion = {
  course_id: string;
  course_code: string;
  reason: string;
};

export type TimetableSlot = {
  section_id: string;
  course_code: string;
  meeting_type: string;
  day_of_week: string;
  start_time: string;
  end_time: string;
  room: string;
};

export type AgentRisk = {
  code: string;
  severity: string;
  message: string;
  course_codes: string[];
};

export type RecommendedCourseView = {
  course_code: string;
  course_name: string;
  note: string;
};

export type ExplainedPlanResponse = {
  student_id: string;
  term_id: string;
  generation_mode: 'LLM' | 'Fallback';
  explanation_source: 'llm' | 'template';
  explanation: string;
  items: PlanItem[];
  exclusions: PlanExclusion[];
  timetable: TimetableSlot[];
  total_credits: number;
  course_count: number;
  warnings: string[];
  risks: AgentRisk[];
  recommended: RecommendedCourseView[];
  names: Record<string, string>;
  run_id: string | null;
};

export function chatWithAgent(message: string, termId = DEFAULT_TERM_ID) {
  return apiRequest<AgentChatResponse>('/api/agent/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      student_id: getCurrentStudentId(),
      term_id: termId,
    }),
  });
}

export function generateExplainedPlan(input: {
  targetCredits?: number;
  note?: string;
  termId?: string;
}) {
  return apiRequest<ExplainedPlanResponse>('/api/agent/plan', {
    method: 'POST',
    body: JSON.stringify({
      student_id: getCurrentStudentId(),
      term_id: input.termId ?? DEFAULT_TERM_ID,
      target_credit_load: input.targetCredits,
      note: input.note || null,
    }),
  });
}
