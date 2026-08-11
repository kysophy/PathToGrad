import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import Login from './pages/Login';
import AppShell from './components/AppShell';
import StudentDashboardPage from './pages/StudentDashboard';
import AdvisorDashboardPage from './pages/AdvisorDashboard';
import CourseCatalogPage from './pages/CourseCatalog';
import StudyPlanPage from './pages/StudyPlan';
const queryClient = new QueryClient();

export default function PathToGrad() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>

          {/* Unwrapped Route: The Login Screen stands alone */}
          <Route path="/" element={<Login />} />
          
          {/* Student INterface Wrapped Routes: Everything inside here gets the Header and Chat Panel */}
           <Route element={<AppShell />}>
            <Route path="/student-dashboard" element={<StudentDashboardPage />} />
            <Route path="/course" element={<CourseCatalogPage />} />
            <Route path="/study-plan" element={<StudyPlanPage />} />

            <Route path="/advisor-dashboard" element={<AdvisorDashboardPage />} />
          </Route>
          
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}