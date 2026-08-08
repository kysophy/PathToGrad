import React from "react";
import tapePiece from "../assets/Tape Piece.svg";

export interface TapeCardProps {
  children: React.ReactNode;
  /** Rotation angle, in degrees, applied to the tape graphic. */
  tapeRotation?: number;
  className?: string;
}

/**
 * TapeCard
 * --------
 * Design System §3B. Used for course items, metric stats, or dashboard
 * modules. A "Tape Piece" asset is anchored at the top edge, slightly
 * rotated, to match the notebook-cover, hand-pasted aesthetic.
 */
export default function TapeCard({
  children,
  tapeRotation = -4,
  className = "",
}: TapeCardProps) {
  return (
    <div className={`relative rounded-xl bg-[#D7D7D7] p-6 shadow-sm ${className}`}>
      <img
        src={tapePiece}
        alt=""
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-0 w-16 -translate-x-1/2 -translate-y-1/2 select-none sm:w-20"
        style={{ transform: `translate(-50%, -50%) rotate(${tapeRotation}deg)` }}
      />
      {children}
    </div>
  );
}