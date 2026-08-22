import React, { useMemo, useState } from "react";

// -----------------------------------------------------------------------
// Data layer (kept in separate files so the backend/API team can swap
// mock data for real T-083v versioning API results without touching
// this file)
// -----------------------------------------------------------------------
import type {
  PlanHistoryProps,
  PlanVersionDetail,
  PlanVersionStatus,
  PlanVersionSummary,
  SortKey,
} from "../services/Types";
import { MOCK_VERSIONS, MOCK_VERSION_DETAILS } from "../services/Mockdata";

// -----------------------------------------------------------------------
// Manual asset imports — "Notebook Design System" doodles.
// Swap these paths for wherever the assets actually live in the repo.
// -----------------------------------------------------------------------
import bunnyDoodle from "../assets/Bunny.svg";
import eggCharacter from "../assets/Average Egg.svg";
import flowerPink from "../assets/FLower 1.svg";
import flowerBlue from "../assets/Flower 2.svg";
import tapeStrip from "../assets/Tape Piece.svg";

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

const statusStyles: Record<PlanVersionStatus, string> = {
  Draft: "bg-amber-100 text-amber-700",
  PendingReview: "bg-blue-100 text-blue-700",
  Approved: "bg-emerald-100 text-emerald-700",
  RevisionRequested: "bg-red-100 text-red-700",
  Superseded: "bg-neutral-200 text-neutral-600",
};

const statusLabels: Record<PlanVersionStatus, string> = {
  Draft: "Draft",
  PendingReview: "Pending review",
  Approved: "Approved",
  RevisionRequested: "Revision requested",
  Superseded: "Superseded",
};

const sortOptions: Array<{ key: SortKey; label: string }> = [
  { key: "creationDate", label: "Creation date" },
  { key: "semester", label: "Semester" },
  { key: "course", label: "Course" },
  { key: "credits", label: "Credits" },
  { key: "status", label: "Status" },
];

function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  const dd = String(d.getDate()).padStart(2, "0");
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  return `${dd}/${mm}/${d.getFullYear()}`;
}

function ChevronDownIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M5 7.5 10 12.5 15 7.5" />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M4 10h12M11 5l5 5-5 5" />
    </svg>
  );
}

// -----------------------------------------------------------------------
// Component (frontend only — no fetching; the parent screen owns
// data-fetching and passes props in, falling back to mock data)
// -----------------------------------------------------------------------

export default function PlanHistory({
  versions = MOCK_VERSIONS,
  selectedVersionId: selectedIdProp,
  onSelectVersion,
  versionDetail: versionDetailProp,
  isDetailLoading = false,
  sortKey: sortKeyProp,
  onSortKeyChange,
}: PlanHistoryProps) {
  const [internalSelectedId, setInternalSelectedId] = useState<string | undefined>(
    selectedIdProp,
  );
  const selectedVersionId = selectedIdProp ?? internalSelectedId;

  const [internalSortKey, setInternalSortKey] = useState<SortKey>(
    sortKeyProp ?? "creationDate",
  );
  const sortKey = sortKeyProp ?? internalSortKey;

  // Mobile master-detail toggle: which pane is visible below the `lg` breakpoint.
  const [mobilePane, setMobilePane] = useState<"list" | "detail">("list");

  function handleSelectVersion(versionId: string) {
    setInternalSelectedId(versionId);
    setMobilePane("detail");
    onSelectVersion?.(versionId);
  }

  function handleSortKeyChange(key: SortKey) {
    setInternalSortKey(key);
    onSortKeyChange?.(key);
  }

  // Falls back to the mock detail map keyed by the resolved selection so the
  // component still renders something meaningful without a parent wired up.
  const fallbackDetail: PlanVersionDetail | null = selectedVersionId
    ? MOCK_VERSION_DETAILS[selectedVersionId] ?? null
    : null;
  const versionDetail = versionDetailProp !== undefined ? versionDetailProp : fallbackDetail;

  const sortedVersions = useMemo(() => sortVersions(versions, sortKey), [versions, sortKey]);

  return (
    <div className="font-nunito relative w-full text-neutral-900" style={notebookGridBackground}>
      <div className="mx-auto flex max-w-6xl flex-col gap-6 p-4 sm:p-6 lg:p-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[380px_1fr] lg:items-start">
          {/* ---------------------------------------------------------
              Left pane — version list (Stage: browse history)
          ---------------------------------------------------------- */}
          <section
            className={cn(
              "flex-col gap-6 rounded-2xl bg-[#FCFF61] p-6 shadow-sm ring-1 ring-black/5",
              mobilePane === "detail" ? "hidden lg:flex" : "flex",
            )}
          >
            <header className="flex items-start justify-between gap-3">
              <h1 className="font-patrick-hand text-4xl leading-none sm:text-5xl">
                Plan history
              </h1>
              <img
                src={bunnyDoodle}
                alt=""
                aria-hidden="true"
                className="mt-1 w-14 shrink-0 -rotate-6 select-none"
              />
            </header>

            <SortBar sortKey={sortKey} onChange={handleSortKeyChange} />

            <VersionList
              versions={sortedVersions}
              selectedVersionId={selectedVersionId}
              onSelect={handleSelectVersion}
            />

            {/* Decorative filler, mirrors the reference design's empty
                space under a short list. Purely ornamental. */}
            <div className="mt-2 hidden items-end justify-between gap-4 sm:flex">
              <img
                src={eggCharacter}
                alt=""
                aria-hidden="true"
                className="w-24 -rotate-2 select-none"
              />
              <div className="flex items-end gap-3">
                <img src={flowerPink} alt="" aria-hidden="true" className="w-16 select-none" />
                <img src={flowerBlue} alt="" aria-hidden="true" className="w-16 select-none" />
              </div>
            </div>
          </section>

          {/* ---------------------------------------------------------
              Right pane — read-only detail for the selected version
          ---------------------------------------------------------- */}
          <section
            className={cn(
              "flex-col gap-4",
              mobilePane === "list" ? "hidden lg:flex" : "flex",
            )}
          >
            <button
              type="button"
              onClick={() => setMobilePane("list")}
              className="font-patrick-hand flex items-center gap-1 self-start text-lg text-neutral-700 lg:hidden"
            >
              <ArrowRightIcon className="w-4 rotate-180" />
              Back to versions
            </button>

            {isDetailLoading ? (
              <DetailSkeleton />
            ) : versionDetail ? (
              <VersionDetailPanel detail={versionDetail} />
            ) : (
              <EmptyDetailState />
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

// -----------------------------------------------------------------------
// Sub-components
// -----------------------------------------------------------------------

function sortVersions(versions: PlanVersionSummary[], sortKey: SortKey): PlanVersionSummary[] {
  const copy = [...versions];
  switch (sortKey) {
    case "creationDate":
      return copy.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    case "semester":
      // No explicit semester field on the summary yet; version number is the
      // closest ordinal proxy until the API exposes it directly.
      return copy.sort((a, b) => b.versionNumber - a.versionNumber);
    case "course":
      return copy.sort((a, b) => a.courseSummary.localeCompare(b.courseSummary));
    case "credits":
      return copy; // Credits total isn't on the summary row; API will add it.
    case "status":
      return copy.sort((a, b) => a.status.localeCompare(b.status));
    default:
      return copy;
  }
}

interface SortBarProps {
  sortKey: SortKey;
  onChange: (key: SortKey) => void;
}

function SortBar({ sortKey, onChange }: SortBarProps) {
  return (
    <div className="flex flex-col gap-2">
      <p className="font-patrick-hand text-xl">Sort by</p>
      <div className="flex flex-wrap gap-2">
        {sortOptions.map((option) => {
          const active = option.key === sortKey;
          return (
            <button
              key={option.key}
              type="button"
              onClick={() => onChange(option.key)}
              aria-pressed={active}
              className={cn(
                "font-nunito flex items-center gap-1 rounded-full px-4 py-1.5 text-sm shadow-sm transition",
                active
                  ? "bg-[#0085FF] text-white"
                  : "bg-white text-neutral-800 hover:bg-white/80",
              )}
            >
              {option.label}
              <ChevronDownIcon className="w-4" />
            </button>
          );
        })}
      </div>
    </div>
  );
}

interface VersionListProps {
  versions: PlanVersionSummary[];
  selectedVersionId?: string;
  onSelect: (versionId: string) => void;
}

function VersionList({ versions, selectedVersionId, onSelect }: VersionListProps) {
  if (versions.length === 0) {
    return (
      <p className="font-nunito text-sm text-neutral-600">
        No plan versions yet — generate a plan to start your history.
      </p>
    );
  }

  return (
    <ol className="font-nunito flex flex-col divide-y divide-black/10">
      {versions.map((version) => {
        const isSelected = version.versionId === selectedVersionId;
        const isSuperseded = version.status === "Superseded";
        return (
          <li key={version.versionId}>
            <button
              type="button"
              onClick={() => onSelect(version.versionId)}
              aria-current={isSelected ? "true" : undefined}
              className={cn(
                "flex w-full items-start justify-between gap-4 py-3 text-left transition first:pt-0",
                // Superseded versions are visually desaturated to reinforce
                // that they're read-only historical records.
                isSuperseded && !isSelected && "opacity-50 hover:opacity-80",
                isSelected && "opacity-100",
              )}
            >
              <div className="flex gap-2">
                <span className="font-patrick-hand text-lg">{version.versionNumber}.</span>
                <div className="flex flex-col gap-1">
                  <span
                    className={cn(
                      "text-sm",
                      isSelected ? "font-semibold text-neutral-900" : "text-neutral-800",
                    )}
                  >
                    {version.courseSummary}
                  </span>
                  <span
                    className={cn(
                      "w-fit rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide",
                      statusStyles[version.status],
                    )}
                  >
                    {statusLabels[version.status]}
                  </span>
                </div>
              </div>

              <div className="flex shrink-0 flex-col items-end gap-2">
                <span className="text-xs text-neutral-600">
                  Generated {formatDate(version.createdAt)}
                </span>
                <ArrowRightIcon
                  className={cn("w-5", isSelected ? "text-[#0085FF]" : "text-neutral-500")}
                />
              </div>
            </button>
          </li>
        );
      })}
    </ol>
  );
}

function EmptyDetailState() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-4 rounded-2xl bg-white/60 p-10 text-center ring-1 ring-black/5">
      <img
        src={eggCharacter}
        alt=""
        aria-hidden="true"
        className="w-24 select-none"
      />
      <p className="font-patrick-hand text-2xl">Pick a version to peek inside</p>
      <p className="font-nunito max-w-xs text-sm text-neutral-600">
        Select any entry from the list to see its exact course lineup and, if it was
        reviewed, your advisor's feedback.
      </p>
    </div>
  );
}

function DetailSkeleton() {
  return (
    <div className="flex flex-1 animate-pulse flex-col gap-4 rounded-2xl bg-white p-6 ring-1 ring-black/5">
      <div className="h-6 w-40 rounded bg-neutral-200" />
      <div className="h-4 w-full rounded bg-neutral-100" />
      <div className="h-4 w-5/6 rounded bg-neutral-100" />
      <div className="h-4 w-2/3 rounded bg-neutral-100" />
    </div>
  );
}

interface VersionDetailPanelProps {
  detail: PlanVersionDetail;
}

function VersionDetailPanel({ detail }: VersionDetailPanelProps) {
  // Advisor feedback only renders for versions that actually went through
  // review — matches the "Approved" / "RevisionRequested" data contract.
  const showFeedback =
    (detail.status === "Approved" || detail.status === "RevisionRequested") &&
    detail.feedback;

  const totalCredits = detail.courses.reduce((sum, c) => sum + c.credits, 0);

  return (
    <div className="flex flex-1 flex-col">
      {/* Main read-only plan card */}
      <section className="flex flex-col gap-4 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-neutral-200">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="flex flex-col gap-1">
            <h2 className="font-patrick-hand text-3xl">Version {detail.versionNumber}</h2>
            <p className="text-sm text-neutral-600">
              Generated {formatDate(detail.createdAt)} · {totalCredits} credits
            </p>
          </div>
          <span
            className={cn(
              "rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide",
              statusStyles[detail.status],
            )}
          >
            {statusLabels[detail.status]}
          </span>
        </div>

        <ul className="font-nunito flex flex-col divide-y divide-neutral-200">
          {detail.courses.map((course) => (
            <li
              key={course.code}
              className="flex flex-wrap items-baseline justify-between gap-2 py-3 first:pt-0 last:pb-0"
            >
              <div className="flex flex-col gap-0.5">
                <span className="font-patrick-hand text-lg">{course.name}</span>
                <span className="text-sm text-neutral-600">{course.code}</span>
              </div>
              <span className="text-sm text-neutral-600">{course.credits} credits</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Advisor feedback — a hand-written sticky note that overlaps the
          card above via negative margin + rotation, staying in normal
          document flow rather than using absolute positioning. */}
      {showFeedback && detail.feedback && (
        <div className="-mt-6 ml-6 max-w-md self-start sm:ml-10">
          {/* Note first, tape second: later-in-flow siblings paint over
              earlier ones, so the tape renders in front of the note. The
              tape is pulled up onto the note's top edge with a negative
              margin, so it still overlaps without any absolute positioning. */}
          <div
            className={cn(
              "font-patrick-hand relative flex flex-col gap-2 rounded-md p-5 text-lg text-neutral-900 shadow-lg",
              detail.status === "RevisionRequested" ? "bg-[#FADCE0]" : "bg-[#7ADB6E]",
              "rotate-1",
            )}
          >
            <p className="text-sm font-semibold uppercase tracking-wide opacity-70">
              Advisor's feedback
            </p>
            <p className="font-nunito text-base leading-snug">{detail.feedback.comment}</p>
            <p className="font-nunito text-xs opacity-70">
              {detail.feedback.advisorName} · {formatDate(detail.feedback.decisionDate)}
            </p>
          </div>
          <img
            src={tapeStrip}
            alt=""
            aria-hidden="true"
            className="relative z-10 -mt-6 ml-4 w-12 -translate-y-2 rotate-3 pointer-events-none select-none"
          />
        </div>
      )}
    </div>
  );
}