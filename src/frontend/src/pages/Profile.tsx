import Profile, { MOCK_STUDENT_PROFILE } from '../components/ProfilePage';
import type { StudentProfileData } from '../components/ProfilePage';

export default function ProfilePage() {
  // TODO: replace with a real update call (T-080) — see
  // src/pages/StudentDashboardPage.tsx for the useQuery/useMutation
  // pattern already established for this project.
  async function handleSave(_updated: StudentProfileData) {
    await new Promise((resolve) => setTimeout(resolve, 600));
  }

  return <Profile data={MOCK_STUDENT_PROFILE} onSave={handleSave} />;
}