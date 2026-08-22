import React from "react";

export interface NotebookPageProps {
  children: React.ReactNode;
  /** Show the bound-notebook spine strip on the left edge. */
  showSpine?: boolean;
  className?: string;
}

/**
 * NotebookPage
 * ------------
 * Full-viewport page shell for the "DIY notebook / sketchbook" theme.
 * - Left "spine" strip mimics a bound notebook edge (flexbox, not absolute).
 * - Main surface gets the grid-paper background pattern (Design System §3C).
 *
 * Layout uses flexbox for the two structural regions (spine + surface) so it
 * reflows fluidly at any viewport width instead of relying on fixed/absolute
 * positioning for the page skeleton. Decorative doodles placed *inside*
 * children are free to use small, percentage-based absolute offsets since
 * they are illustrative overlays, not structural layout.
 */
export default function NotebookPage({
  children,
  showSpine = true,
  className = "",
}: NotebookPageProps) {
  return (
    <div className={`flex min-h-screen w-full bg-white ${className}`}>
      {showSpine && (
        <div
          aria-hidden="true"
          className="hidden shrink-0 rounded-r-lg bg-[#D7D7D7] sm:block sm:w-[clamp(20px,3vw,59px)]"
        />
      )}

      <div
        className="relative min-h-screen w-full flex-1 overflow-hidden
          bg-white
          bg-[repeating-linear-gradient(0deg,#e6e6e6_0_1px,transparent_1px_8px),repeating-linear-gradient(90deg,#e6e6e6_0_1px,transparent_1px_8px),repeating-linear-gradient(0deg,#cfcfcf_0_1px,transparent_1px_80px),repeating-linear-gradient(90deg,#cfcfcf_0_1px,transparent_1px_80px)]"
      >
        {children}
      </div>
    </div>
  );
}