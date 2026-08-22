import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext';

interface RoleGuardProps {
  allowedRole: 'Student' | 'Advisor' | 'Admin';
}

export default function RoleGuard({ allowedRole }: RoleGuardProps) {
  const { isAuthenticated, role } = useAuth();

  // If they aren't logged in at all, kick them to the login screen
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  // If they are logged in but have the wrong role, kick them to an unauthorized error or login
  if (role !== allowedRole) {
    return <Navigate to="/" replace />;
  }

  // If everything matches, render the child routes!
  return <Outlet />;
}