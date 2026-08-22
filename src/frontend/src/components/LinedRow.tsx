type LinedRowProps = {
  children: React.ReactNode;
  bold?: boolean;
  /** Allow natural text wrapping instead of single-line truncation.
   * Safe to do without breaking rule alignment as long as the row's
   * line-height (leading-9 = 36px) exactly matches the ruled-line pitch:
   * a wrapped block's height is always lines × line-height, so its
   * bottom border still lands exactly on a rule regardless of how many
   * lines it wraps to. */
  wrap?: boolean;
  className?: string;
};

/**
 * LinedRow
 * -----------------------------------------------------------------------
 * One line (or, with `wrap`, one wrapped block) of "notebook paper"
 * text. Each row owns its own bottom border instead of relying on a
 * background-image ruled pattern behind free-flowing text — a
 * background pattern only lines up as long as every row is exactly one
 * text-line tall, which breaks the moment content wraps or the number
 * of rows changes. Owning the border per-row means it's correct for any
 * amount of content.
 */
export default function LinedRow({ children, bold = false, wrap = false, className = '' }: LinedRowProps) {
  return (
    <div
      className={`${wrap ? '' : 'h-9 truncate'} border-b border-black/40 leading-9 ${
        bold ? 'font-heading text-lg' : 'font-body text-base'
      } ${className}`}
    >
      {children}
    </div>
  );
}