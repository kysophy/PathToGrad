/**
 * Temporary development session.
 *
 * There is still no `/api/auth/login`. The notebook login screen picks
 * one of these cheat identities and every student API call reads it back
 * from localStorage. Replace with a real session when FR-18 lands.
 */

const STUDENT_KEY = 'pathtograd.dev.studentId';
const USER_KEY = 'pathtograd.dev.userId';

export type DevLogin = {
  studentId: string;
  userId: string;
  name: string;
  /** Short id typed on the login screen. */
  loginId: string;
  semester: number;
  spec: string;
  summary: string;
};

export const DEV_LOGINS: DevLogin[] = [
  {
    loginId: 'test',
    studentId: 'TEST001',
    userId: 'USER-TEST-001',
    name: 'Test User',
    semester: 2,
    spec: 'GEN',
    summary: 'Empty UI profile until you save Profile. No transcript.',
  },
  {
    loginId: 's02',
    studentId: 'DEMO-S02',
    userId: 'USER-DEMO-S02',
    name: 'Demo Student S02',
    semester: 2,
    spec: 'GEN',
    summary: 'On-track first year. Sem-1 passed (~15 cr). Soft-lock this term.',
  },
  {
    loginId: 's05',
    studentId: 'DEMO-S05',
    userId: 'USER-DEMO-S05',
    name: 'Demo Student S05',
    semester: 5,
    spec: 'GEN',
    summary: 'Mid-path plus one backlog.',
  },
  {
    loginId: 'fail',
    studentId: 'DEMO-FAIL',
    userId: 'USER-DEMO-FAIL',
    name: 'Demo Student Fail',
    semester: 5,
    spec: 'GEN',
    summary: 'Failed CSC10012 once; CSC10009 failed twice.',
  },
  {
    loginId: 's08',
    studentId: 'DEMO-S08',
    userId: 'USER-DEMO-S08',
    name: 'Demo Student S08',
    semester: 8,
    spec: 'SE',
    summary: 'A-20 paper senior. CSC13001 is not offered this term.',
  },
  {
    loginId: 'cap',
    studentId: 'DEMO-CAP',
    userId: 'USER-DEMO-CAP',
    name: 'Demo Student Cap',
    semester: 8,
    spec: 'SE',
    summary: 'Assigned + backlog hits the 24-credit / 6-course cap.',
  },
];

const BY_ALIAS = new Map<string, DevLogin>();
for (const account of DEV_LOGINS) {
  BY_ALIAS.set(account.loginId, account);
  BY_ALIAS.set(account.studentId.toLowerCase(), account);
  if (account.studentId.startsWith('DEMO-')) {
    const shortId = account.studentId.slice('DEMO-'.length).toLowerCase();
    BY_ALIAS.set(shortId, account);
    BY_ALIAS.set(`demo-${shortId}`, account);
  }
}

function normalizeLoginId(raw: string): string {
  return raw.trim().toLowerCase().replace(/_/g, '-');
}

export function lookupDevLogin(raw: string): DevLogin | undefined {
  return BY_ALIAS.get(normalizeLoginId(raw));
}

export function setDevSession(studentId: string, userId: string): void {
  localStorage.setItem(STUDENT_KEY, studentId);
  localStorage.setItem(USER_KEY, userId);
}

export function getCurrentStudentId(): string {
  return localStorage.getItem(STUDENT_KEY) ?? 'TEST001';
}

export function getCurrentUserId(): string {
  return localStorage.getItem(USER_KEY) ?? 'USER-TEST-001';
}
