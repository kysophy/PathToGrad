/**
 * Development session.
 *
 * Real login (POST /api/auth/login) resolves an identifier against the
 * seeded `users` / `student_profile` tables, so which student's data the
 * app loads now depends on who actually logged in instead of one
 * hardcoded id. CURRENT_STUDENT_ID is a live binding (`export let`, not
 * `const`): every module that imports it sees updates made through
 * setCurrentStudentId without re-importing.
 *
 * Advisor/Admin role-based session data is still out of scope (FR-18).
 */

const STORAGE_KEY = "pathtograd.currentStudentId";
const DEFAULT_STUDENT_ID = "TEST001";

function readStoredStudentId(): string {
  try {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_STUDENT_ID;
  } catch {
    return DEFAULT_STUDENT_ID;
  }
}

export let CURRENT_STUDENT_ID = readStoredStudentId();

export const CURRENT_USER_ID = "USER-TEST-001";

export function setCurrentStudentId(studentId: string) {
  CURRENT_STUDENT_ID = studentId;
  try {
    localStorage.setItem(STORAGE_KEY, studentId);
  } catch {
    // localStorage unavailable (private mode, etc.) - session still
    // works for the current tab via the in-memory binding above.
  }
}

export function clearCurrentStudentId() {
  setCurrentStudentId(DEFAULT_STUDENT_ID);
}
