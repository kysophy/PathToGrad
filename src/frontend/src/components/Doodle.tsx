import React from "react";

export interface DoodleProps {
  src: string;
  alt?: string;
  top?: string;
  left?: string;
  right?: string;
  bottom?: string;
  /** Minimum rendered width, in px. */
  minPx?: number;
  /** Fluid width, in vw. */
  vw?: number;
  /** Maximum rendered width, in px. */
  maxPx?: number;
  /** Rotation, in degrees. */
  rotate?: number;
  /** Enable the soft blur look. */
  blurred?: boolean;
  /** Blur strength in px when `blurred` is true. */
  blurAmount?: number;
  /** Opacity applied alongside the blur (source doodles read softer than full-opacity). */
  blurOpacity?: number;
  className?: string;
  /** Hide on small viewports to avoid clutter. */
  hideOnMobile?: boolean;
}

/**
 * Doodle
 * ------
 * Positions a single decorative asset (star, flower, cloud, etc.) from
 * src/assets. These are purely illustrative/background elements, so they use
 * percentage-based absolute placement inside a `relative` ancestor -- this is
 * the one place absolute positioning is appropriate, since the doodles have
 * no effect on document flow or structural layout.
 *
 * Sizes are fluid via clamp() so doodles scale gracefully between mobile and
 * desktop instead of jumping between fixed breakpoints. clamp() needs a
 * runtime-computed value, so it's set via `style` rather than a static
 * Tailwind class -- same reasoning applies to the blur filter, so both live
 * together in `style` rather than mixing a Tailwind blur class with inline
 * sizing.
 */
export default function Doodle({
  src,
  alt = "",
  top,
  left,
  right,
  bottom,
  minPx = 28,
  vw = 5,
  maxPx = 90,
  rotate = 0,
  blurred = false,
  blurAmount = 3,
  blurOpacity = 0.85,
  className = "",
  hideOnMobile = false,
}: DoodleProps) {
  return (
    <img
      src={src}
      alt={alt}
      aria-hidden={alt === "" ? "true" : undefined}
      className={`pointer-events-none absolute select-none ${
        hideOnMobile ? "hidden sm:block" : ""
      } ${className}`}
      style={{
        top,
        left,
        right,
        bottom,
        width: `clamp(${minPx}px, ${vw}vw, ${maxPx}px)`,
        height: "auto",
        opacity: blurred ? blurOpacity : 1,
        filter: blurred ? `blur(${blurAmount}px)` : undefined,
        transform: rotate ? `rotate(${rotate}deg)` : undefined,
      }}
    />
  );
}