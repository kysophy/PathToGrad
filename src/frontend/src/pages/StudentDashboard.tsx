import { useQuery } from '@tanstack/react-query';
import StudentDashboard from '../components/StudentDashboardPage';
import { getDashboardData, MOCK_DASHBOARD_DATA } from '../services/Dashboard';

export default function StudentDashboardPage() {
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardData,
  });

  if (isLoading) {
    return (
      <div className="flex min-h-full items-center justify-center p-10">
        <p className="font-heading text-xl text-notebook-ink">Loading your dashboard…</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex min-h-full flex-col items-center justify-center gap-3 p-10 text-center">
        <p className="font-heading text-xl text-notebook-ink">Couldn't load your dashboard.</p>
        <p className="font-body text-sm text-neutral-500">{(error as Error).message}</p>
        <button
          type="button"
          onClick={() => refetch()}
          className="rounded-full bg-notebook-ink px-4 py-2 font-body text-sm text-white"
        >
          Try again
        </button>
      </div>
    );
  }

  // TanStack Query has already resolved by this point, but fall back to
  // mock data defensively rather than rendering with `data` possibly
  // undefined.
  return <StudentDashboard {...(data ?? MOCK_DASHBOARD_DATA)} />;
}