import {
  useEffect,
  useState,
} from 'react';

import StudentDashboard
  from '../components/StudentDashboardPage';

import {
  DashboardData,
  getDashboardData,
} from '../services/Dashboard';


export default function StudentDashboardPage() {

  const [
    data,
    setData,
  ] = useState<
    DashboardData | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState('');


  useEffect(() => {

    let active = true;

    async function loadDashboard() {

      try {
        setLoading(true);

        const result =
          await getDashboardData();

        if (active) {
          setData(result);
          setError('');
        }

      } catch (err) {

        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : (
                  'Unable to load '
                  + 'student dashboard.'
                ),
          );
        }

      } finally {

        if (active) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      active = false;
    };

  }, []);


  if (loading) {
    return (
      <div
        className="
          p-6
          font-body
          text-neutral-600
        "
      >
        Loading academic overview...
      </div>
    );
  }


  if (error) {
    return (
      <div
        className="
          m-6
          rounded-xl
          bg-red-100
          p-4
          font-body
          text-red-700
        "
      >
        {error}
      </div>
    );
  }


  if (!data) {
    return (
      <div
        className="
          p-6
          font-body
        "
      >
        Academic overview is unavailable.
      </div>
    );
  }


  return (
    <StudentDashboard
      data={data}
    />
  );
}