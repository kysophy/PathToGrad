import { Outlet } from 'react-router-dom';
import Header from '../components/Header';
import ChatPanel from '../components/ChatPanel';

type NavItem = { label: string; to: string };

type AppShellProps = {
  /** Nav links shown in the header. Defaults to Header's own fallback
   * if omitted — pass this explicitly once you have more than one
   * wrapped route group (e.g. a different set for /advisor-dashboard). */
  navItems?: NavItem[];
};

const defaultStudentLinks: NavItem[] = [
    { label: 'Dashboard', to: '/student-dashboard' },
    { label: 'Course Catalog', to: '/course-catalog' },
    { label: 'Study Plan', to: '/study-plan' },
    { label: 'Plan History', to: '/plan-history' },
    { label: 'Profile', to: '/profile' },
    { label: 'Academic Record', to: '/academic-record' },
  ];

export default function AppShell({ navItems }: AppShellProps) {
  
  // Create a variable that falls back to the defaults if navItems is not provided
  const activeLinks = navItems || defaultStudentLinks;

  return (
    <div className="flex h-screen w-full overflow-hidden bg-white">
      <div className="flex min-w-0 flex-1 flex-col">
        
        {/* Pass the new activeLinks variable here! */}
        <Header navItems={activeLinks} />
        
        <main className="min-h-0 flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      <ChatPanel />
    </div>
  );
}