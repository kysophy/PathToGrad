import { NavLink } from 'react-router-dom';

/** Minimal inline icons — no icon package dependency. */
function BellIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M6 9a6 6 0 1 1 12 0c0 3.4 1 5.2 1.6 6.1a1 1 0 0 1-.85 1.5H5.25a1 1 0 0 1-.85-1.5C5 14.2 6 12.4 6 9Z" />
      <path d="M9.5 18a2.5 2.5 0 0 0 5 0" />
    </svg>
  );
}

function UserIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="12" cy="8" r="3.25" />
      <path d="M5.5 19c1.2-3.2 3.6-4.75 6.5-4.75S17.3 15.8 18.5 19" />
    </svg>
  );
}

type NavItem = { label: string; to: string };

type HeaderProps = {
  navItems?: NavItem[];
};

const DEFAULT_NAV: NavItem[] = [
  { label: 'Student Dashboard', to: '/student-dashboard' },
  { label: 'Course Catalog', to: '/course' },
  { label: 'Study Plan', to: '/study-plan' },
];

export default function Header({ navItems = DEFAULT_NAV }: HeaderProps) {
  return (
    <header className="flex h-[45px] shrink-0 items-center justify-between bg-notebook-line px-5">
      <div className="flex items-center gap-7">
        <span className="font-serif text-lg font-bold tracking-tight text-notebook-ink">
          fit@hcmus
        </span>

        <nav className="flex items-center gap-5">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  'font-heading text-[15px] text-notebook-ink',
                  isActive ? 'underline underline-offset-4' : 'opacity-80 hover:opacity-100',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          aria-label="Notifications"
          className="flex h-8 w-8 items-center justify-center rounded-full text-notebook-ink hover:bg-black/5"
        >
          <BellIcon className="h-5 w-5" />
        </button>

        <button
          type="button"
          aria-label="Account"
          className="flex h-7 w-7 items-center justify-center rounded-full bg-[#937FBD] text-white"
        >
          <UserIcon className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}