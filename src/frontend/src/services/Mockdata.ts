/**
 * mockData.ts
 * ---------------------------------------------------------------------
 * Visual-fallback / development data, fully decoupled from the UI.
 * Replace these with real `T-083v` versioning API calls (e.g.
 * `useVersionList`, `useVersionDetail`) once available — the shapes
 * match `PlanVersionSummary` / `PlanVersionDetail` exactly so the swap
 * is a drop-in.
 * ---------------------------------------------------------------------
 */
import type { PlanVersionDetail, PlanVersionSummary } from "./Types";

export const MOCK_VERSIONS: PlanVersionSummary[] = [
  {
    versionId: "v4",
    versionNumber: 4,
    createdAt: "2026-07-23T09:12:00Z",
    status: "Draft",
    courseSummary: "Introduction to IT, DSA",
  },
  {
    versionId: "v3",
    versionNumber: 3,
    createdAt: "2026-07-23T09:12:00Z",
    status: "PendingReview",
    courseSummary: "Linear Algebra II, Introduction to Information Technology",
  },
  {
    versionId: "v2",
    versionNumber: 2,
    createdAt: "2026-06-18T14:40:00Z",
    status: "NeedsRequested",
    courseSummary: "Linear Algebra I, Discrete Mathematics",
  },
  {
    versionId: "v1",
    versionNumber: 1,
    createdAt: "2026-05-02T08:05:00Z",
    status: "Superseded",
    courseSummary: "General Physics I, Calculus I",
  },
];

/** Keyed by versionId, standing in for a per-version detail fetch. */
export const MOCK_VERSION_DETAILS: Record<string, PlanVersionDetail> = {
  v4: {
    versionId: "v4",
    versionNumber: 4,
    createdAt: "2026-07-23T09:12:00Z",
    status: "Draft",
    courseSummary: "Introduction to IT, DSA",
    courses: [
      { code: "24C01", name: "Introduction to Information Technology", credits: 3 },
      { code: "24C15", name: "Data Structures & Algorithms", credits: 4 },
    ],
  },
  v3: {
    versionId: "v3",
    versionNumber: 3,
    createdAt: "2026-07-23T09:12:00Z",
    status: "PendingReview",
    courseSummary: "Linear Algebra II, Introduction to Information Technology",
    courses: [
      { code: "24C08", name: "Linear Algebra II", credits: 3 },
      { code: "24C01", name: "Introduction to Information Technology", credits: 3 },
    ],
  },
  v2: {
    versionId: "v2",
    versionNumber: 2,
    createdAt: "2026-06-18T14:40:00Z",
    status: "NeedsRequested",
    courseSummary: "Linear Algebra I, Discrete Mathematics",
    courses: [
      { code: "24C07", name: "Linear Algebra I", credits: 3 },
      { code: "24C22", name: "Discrete Mathematics", credits: 3 },
    ],
    feedback: {
      advisorName: "Dr. Pham Minh D.",
      decisionDate: "2026-06-20T10:00:00Z",
      comment:
        "Please swap Discrete Mathematics for a semester-3 elective — the prerequisite for CS majors isn't satisfied yet.",
    },
  },
  v1: {
    versionId: "v1",
    versionNumber: 1,
    createdAt: "2026-05-02T08:05:00Z",
    status: "Superseded",
    courseSummary: "General Physics I, Calculus I",
    courses: [
      { code: "24C05", name: "General Physics I", credits: 3 },
      { code: "24C02", name: "Calculus I", credits: 4 },
    ],
    feedback: {
      advisorName: "Dr. Le Van K.",
      decisionDate: "2026-05-04T11:30:00Z",
      comment: "Looks good — approved as your baseline semester 1 plan.",
    },
  },
};