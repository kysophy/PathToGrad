import React from "react";

export interface StickyNoteProps {
  children: React.ReactNode;
  /** Rotation angle in degrees, e.g. -2 or 3, for a hand-pasted effect. */
  rotation?: number;
  className?: string;
  as?: keyof React.JSX.IntrinsicElements;
}

/**
 * StickyNote
 * ----------
 * Design System §3A. Used for advisor notes, key callouts, and academic
 * feedback pop-ups. Accepts a `rotation` prop so instances can be given a
 * subtle random angle to recreate a hand-pasted sticky-note effect.
 *
 * Example:
 *   <StickyNote rotation={-2}>Remember to submit your FAFSA by March 1!</StickyNote>
 */
export default function StickyNote({
  children,
  rotation = -2,
  className = "",
  as: Tag = "div",
}: StickyNoteProps) {
  return (
    <Tag
      className={`inline-block rounded-sm bg-[#FFF9B0] px-4 py-3 font-body text-sm text-neutral-900 shadow-md sm:text-base ${className}`}
      style={{ transform: `rotate(${rotation}deg)` }}
    >
      {children}
    </Tag>
  );
}