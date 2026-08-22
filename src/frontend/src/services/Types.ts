/**
 * types.ts
 * ---------------------------------------------------------------------
 * Data contract for the Plan History feature. Kept separate from the
 * UI component so it can be imported by both `PlanHistory.tsx`
 * (frontend) and the versioning API layer (T-083v) without pulling in
 * any React/DOM code.
 * ---------------------------------------------------------------------
 */

/** Lifecycle state of a single plan version, for audit traceability. */
export type PlanVersionStatus =
  | "Draft"
  | "PendingReview"
  | "Approved"
  | "RevisionRequested"
  | "Superseded";

export interface PlanVersionCourse {
  code: string;
  name: string;
  credits: number;
}

/**
 * Lightweight row for the version list. The API returns these cheaply
 * (no full course payload) so the list can render fast; full course
 * data is fetched per-version on selection — see `PlanVersionDetail`.
 */
export interface PlanVersionSummary {
  versionId: string;
  versionNumber: number;
  createdAt: string; // ISO 8601
  status: PlanVersionStatus;
  /** Short, pre-joined preview of course names for the list row, e.g. "Introduction to IT, DSA". */
  courseSummary: string;
}

export interface AdvisorFeedback {
  advisorName: string;
  decisionDate: string; // ISO 8601
  /**
   * Required by the backend whenever the parent version's status is
   * "RevisionRequested"; optional (may be an empty string) when
   * "Approved". The UI does not re-validate this — it trusts the API
   * contract — but always renders the field when present.
   */
  comment: string;
}

/**
 * Full, read-only record for a single historical version — the exact
 * course set that existed at that point in time, plus advisor
 * feedback when applicable. Fetched lazily when a version is selected.
 */
export interface PlanVersionDetail extends PlanVersionSummary {
  courses: PlanVersionCourse[];
  /** Present only when status is "Approved" or "RevisionRequested". */
  feedback?: AdvisorFeedback;
}

export type SortKey = "creationDate" | "semester" | "course" | "credits" | "status";

export interface PlanHistoryProps {
  /** List of versions for the left pane. Falls back to mock data if omitted. */
  versions?: PlanVersionSummary[];
  /** Currently selected version id, drives the right-hand detail pane. */
  selectedVersionId?: string;
  onSelectVersion?: (versionId: string) => void;
  /** Full detail for `selectedVersionId`, fetched separately/lazily by the parent. */
  versionDetail?: PlanVersionDetail | null;
  /** Shows a loading state in the detail pane while a version's detail is being fetched. */
  isDetailLoading?: boolean;
  sortKey?: SortKey;
  onSortKeyChange?: (key: SortKey) => void;
}