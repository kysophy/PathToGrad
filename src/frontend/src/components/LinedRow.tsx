type LinedRowProps = {
  children: React.ReactNode;
  bold?: boolean;
  className?: string;
};

/**
 * LinedRow
 * -----------------------------------------------------------------------
 * One line of "notebook paper" text. Each row owns a fixed height and its
 * own bottom border, instead of relying on a background-image ruled
 * pattern behind free-flowing text. That's what guarantees perfect
 * alignment: a background pattern only lines up as long as every row is
 * exactly one text-line tall, which breaks the moment content wraps or
 * the number of rows changes. Making the border part of the row itself
 * means it's correct for any amount of content — one course or fifty.
 *
 * `truncate` keeps each row to a single line on purpose (ruled paper is
 * one line per row); if a value might overflow, the row clips with an
 * ellipsis rather than wrapping and breaking the rhythm of the lines
 * below it.
 */
export default function LinedRow({ children, bold = false, className = '' }: LinedRowProps) {
  return (
    <div
      className={`h-9 truncate border-b border-black/40 leading-9 ${
        bold ? 'font-heading text-lg' : 'font-body text-base'
      } ${className}`}
    >
      {children}
    </div>
  );
}