import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { AuthProvider } from './utils/AuthContext';
import { ChatProvider } from './utils/ChatContext';
import RoleGuard from './utils/RoleGuard';
import Login from './pages/Login';
import AppShell from './layouts/AppShell';
import StudentDashboardPage from './pages/StudentDashboard';
import AdvisorDashboardPage from './pages/AdvisorDashboard';
import CourseCatalogPage from './pages/CourseCatalog';
import StudyPlanPage from './pages/StudyPlan';
import PlanHistoryPage from './pages/PlanHistory';
import ProfilePage from './pages/Profile';
import AcademicRecordPage from './pages/AcademicRecord';

const queryClient = new QueryClient();

export default function PathToGrad() {
  return (
    <AuthProvider>
      <ChatProvider>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <Routes>
              {/* Public Route */}
              <Route path="/" element={<Login />} />

              {/* Protected Student Routes */}
              <Route element={<RoleGuard allowedRole="Student" />}>
                <Route element={<AppShell />}>
                  <Route path="/student-dashboard" element={<StudentDashboardPage />} />
                  <Route path="/course-catalog" element={<CourseCatalogPage />} />
                  <Route path="/study-plan" element={<StudyPlanPage />} />
                  <Route path="/plan-history" element={<PlanHistoryPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/academic-record" element={<AcademicRecordPage />} />
                </Route>
              </Route>

              {/* Protected Advisor Routes */}
              <Route element={<RoleGuard allowedRole="Advisor" />}>
                <Route path="/advisor-dashboard" element={<AdvisorDashboardPage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </QueryClientProvider>
      </ChatProvider>
    </AuthProvider>
  );
}