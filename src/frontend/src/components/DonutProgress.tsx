type DonutProgressProps = {
  /** 0–100. */
  percent: number;
  size?: number;
  strokeWidth?: number;
  /** Text rendered in the center, e.g. "67%" or "6,7%". Defaults to
   * `${percent}%` if omitted. */
  label?: string;
  className?: string;
};

const TRACK_COLOR = '#6750A4'; // purple
const PROGRESS_COLOR = '#0085FF'; // notebook blue

/**
 * DonutProgress
 * -----------------------------------------------------------------------
 * Two-tone ring: blue arc = `percent` of the circle, purple arc = the
 * remainder, both rounded-cap with a small gap at each seam.
 *
 * Note on fidelity: the visual reference uses a roughly 50/50 blue/purple
 * split on this ring for both the 67% and the 6.7% card alike — i.e. the
 * reference ring is decorative rather than actually proportional to the
 * number next to it. Since this is meant to be a real, data-driven
 * dashboard component (per the brief), this version genuinely reflects
 * `percent` instead of reproducing that inconsistency — at 6.7% the blue
 * arc will correctly read as a small sliver, not a half circle.
 */
export default function DonutProgress({
  percent,
  size = 140,
  strokeWidth = 14,
  label,
  className = '',
}: DonutProgressProps) {
  const clamped = Math.max(0, Math.min(100, percent));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const gap = Math.min(10, circumference * 0.03);

  const progressLength = Math.max(0, (clamped / 100) * circumference - gap);
  const trackLength = Math.max(0, circumference - (clamped / 100) * circumference - gap);

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      width={size}
      height={size}
      className={className}
      role="img"
      aria-label={label ?? `${percent}%`}
    >
      {/* purple track arc, starts right after the progress arc + gap */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={TRACK_COLOR}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={`${trackLength} ${circumference - trackLength}`}
        strokeDashoffset={-(progressLength + gap)}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      {/* blue progress arc */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={PROGRESS_COLOR}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={`${progressLength} ${circumference - progressLength}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        className="fill-notebook-ink font-heading"
        style={{ fontSize: size * 0.22 }}
      >
        {label ?? `${percent}%`}
      </text>
    </svg>
  );
}