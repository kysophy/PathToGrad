import { Outlet } from 'react-router-dom';
import Header from './Header';
import ChatPanel from './ChatPanel';

type NavItem = { label: string; to: string };

type AppShellProps = {
  /** Nav links shown in the header. Defaults to Header's own fallback
   * if omitted — pass this explicitly once you have more than one
   * wrapped route group (e.g. a different set for /advisor-dashboard). */
  navItems?: NavItem[];
};

/**
 * AppShell
 * -----------------------------------------------------------------------
 * Top-level layout: header + routed page content on the left, a
 * persistent ChatPanel docked on the right. Mount this once, above your
 * routes, e.g.:
 *
 *   <Route element={<AppShell />}>
 *     <Route path="/student-dashboard" element={<StudentDashboard />} />
 *   </Route>
 *
 * Because ChatPanel is a sibling of <Outlet/> here rather than part of
 * any individual route, it never unmounts on navigation — its input
 * draft, message history, and scroll position all persist automatically.
 */
export default function AppShell({ navItems }: AppShellProps) {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-white">
      <div className="flex min-w-0 flex-1 flex-col">
        <Header navItems={navItems} />
        <main className="min-h-0 flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      <ChatPanel />
    </div>
  );
}