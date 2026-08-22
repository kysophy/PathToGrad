import { useState, type FormEvent } from 'react';

/**
 * Profile
 * -----------------------------------------------------------------------
 * Center content area only — meant to be rendered inside AppShell's
 * <Outlet/>. Does not render the top header or the chat sidebar.
 *
 * Functional form screen (T-109): view + edit student profile info,
 * built against the Student API contract (T-080). Institutional fields
 * (studentId, classId, curriculumId, facultyOf, enrollmentYear) render
 * as read-only; personal fields are editable, controlled inputs.
 *
 * Two additions beyond what's pictured in the design, both flagged here
 * rather than silently added:
 *  - `classId` (e.g. "24CLC06") has its own "Class:" field — the visual
 *    reference doesn't show one, but T-109 explicitly requires it in the
 *    data contract, so it's rendered alongside the other academic fields.
 *  - A Save button + submission state at the bottom, since "handle API
 *    updates gracefully" implies something has to trigger the update.
 */

export type GuardianInfo = {
  fullName: string;
  relationship: string;
  phoneNumber: string;
};

export type ScientificArticle = {
  id: string;
  title: string;
};

export type StudentProfileData = {
  // General information
  /** Read-only. */
  studentId: string;
  /** Editable. */
  fullName: string;
  dateOfBirth: string;
  /** Read-only or mapped via API. */
  facultyOf: string;
  /** Read-only or mapped via API — e.g. "Software Engineering". */
  curriculumId: string;
  /** Read-only or mapped via API — e.g. "24CLC06". */
  classId: string;
  /** Read-only or mapped via API. */
  enrollmentYear: number;
  status: string;
  photoUrl?: string;

  // Detailed information — left card
  citizenIdNumber: string;
  nation: string;
  address: string;
  phoneNumber: string;
  email: string;
  youthUnionAdmissionDate: string;
  guardian: GuardianInfo;

  // Detailed information — right card
  currentCredits: number;
  scientificArticles: ScientificArticle[];
  graduationYear: number | null;
  gpa: number;
};

export type SubmissionState = 'idle' | 'saving' | 'success' | 'error';

export type ProfileProps = {
  data: StudentProfileData;
  /** Called with the edited profile on submit. Wire this up to the real
   * PATCH/PUT call (T-080) — Profile itself only tracks local form state
   * and the idle/saving/success/error lifecycle around calling this. */
  onSave?: (data: StudentProfileData) => Promise<void>;
};

export const MOCK_STUDENT_PROFILE: StudentProfileData = {
  studentId: '21127123',
  fullName: 'Nguyen Van A',
  dateOfBirth: '2003-05-14',
  facultyOf: 'Information Technology',
  curriculumId: 'Software Engineering',
  classId: '24CLC06',
  enrollmentYear: 2021,
  status: 'Undergraduate',
  citizenIdNumber: '079203001234',
  nation: 'Vietnam',
  address: '227 Nguyen Van Cu, District 5, Ho Chi Minh City',
  phoneNumber: '0901234567',
  email: 'nva@student.hcmus.edu.vn',
  youthUnionAdmissionDate: '2019-03-26',
  guardian: {
    fullName: 'Nguyen Van B',
    relationship: 'Father',
    phoneNumber: '0909876543',
  },
  currentCredits: 67,
  scientificArticles: [],
  graduationYear: null,
  gpa: 6.7,
};

const inputClass =
  'w-full border-0 border-b border-black/50 bg-transparent pb-1 font-body text-base text-notebook-ink outline-none focus:border-notebook-blue disabled:text-neutral-500';

const labelClass = 'font-heading text-lg text-notebook-ink';

/** Read-only "field" rendered with the exact same lined-paper baseline
 * as an editable input, so the two don't look visually inconsistent —
 * it's just not a form control since there's nothing to submit. */
function ReadOnlyField({ label, value }: { label: string; value: string | number }) {
  return (
    <p className={labelClass}>
      {label}: <span className="font-body text-base text-neutral-700">{value}</span>
    </p>
  );
}

function TextField({
  label,
  value,
  onChange,
  type = 'text',
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
}) {
  return (
    <label className="flex flex-col gap-1">
      <span className={labelClass}>{label}:</span>
      <input type={type} value={value} onChange={(e) => onChange(e.target.value)} className={inputClass} />
    </label>
  );
}

export default function Profile({ data, onSave }: ProfileProps) {
  const [form, setForm] = useState<StudentProfileData>(data);
  const [submission, setSubmission] = useState<SubmissionState>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  function update<K extends keyof StudentProfileData>(key: K, value: StudentProfileData[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function updateGuardian<K extends keyof GuardianInfo>(key: K, value: GuardianInfo[K]) {
    setForm((prev) => ({ ...prev, guardian: { ...prev.guardian, [key]: value } }));
  }

  function addArticle() {
    setForm((prev) => ({
      ...prev,
      scientificArticles: [...prev.scientificArticles, { id: crypto.randomUUID(), title: '' }],
    }));
  }

  function updateArticle(id: string, title: string) {
    setForm((prev) => ({
      ...prev,
      scientificArticles: prev.scientificArticles.map((a) => (a.id === id ? { ...a, title } : a)),
    }));
  }

  function removeArticle(id: string) {
    setForm((prev) => ({
      ...prev,
      scientificArticles: prev.scientificArticles.filter((a) => a.id !== id),
    }));
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!onSave) return;

    setSubmission('saving');
    setErrorMessage(null);
    try {
      await onSave(form);
      setSubmission('success');
    } catch (err) {
      setSubmission('error');
      setErrorMessage(err instanceof Error ? err.message : 'Something went wrong.');
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6 p-4 sm:p-6">
      <div className="rounded-[32px] bg-notebook-card p-3 sm:p-6">
        {/* General information */}
        <section className="rounded-3xl bg-white p-6 sm:p-10">
          <h1 className="font-heading text-3xl text-notebook-ink sm:text-4xl">General Information</h1>

          <div className="mt-8 flex flex-col gap-6 sm:flex-row sm:gap-10">
            <div className="w-40 shrink-0 sm:w-48">
              <div
                className="aspect-[244/307] w-full overflow-hidden rounded-md bg-notebook-blue"
                style={form.photoUrl ? { backgroundImage: `url(${form.photoUrl})`, backgroundSize: 'cover' } : undefined}
              />
              <p className="mt-3 font-body text-sm text-neutral-700">Status: {form.status}</p>
            </div>

            <div className="flex flex-1 flex-col gap-6 sm:flex-row sm:gap-12">
              <div className="flex flex-1 flex-col gap-4">
                <ReadOnlyField label="Student ID" value={form.studentId} />
                <TextField label="Full name" value={form.fullName} onChange={(v) => update('fullName', v)} />
                <TextField
                  label="Date of birth"
                  type="date"
                  value={form.dateOfBirth}
                  onChange={(v) => update('dateOfBirth', v)}
                />

                <div className="mt-4 flex flex-col gap-4">
                  <ReadOnlyField label="Faculty of" value={form.facultyOf} />
                  <ReadOnlyField label="Degree" value={form.curriculumId} />
                  <ReadOnlyField label="Class" value={form.classId} />
                </div>

                <div className="mt-4">
                  <ReadOnlyField label="Enrollment year" value={form.enrollmentYear} />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Detailed information */}
        <div className="mt-6 px-3 sm:px-4">
          <h2 className="font-heading text-3xl text-notebook-ink sm:text-4xl">Detailed Information</h2>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
          <section className="rounded-3xl bg-white p-6 sm:p-8">
            <div className="flex flex-col gap-4">
              <TextField
                label="Citizen identity number"
                value={form.citizenIdNumber}
                onChange={(v) => update('citizenIdNumber', v)}
              />
              <TextField label="Nation" value={form.nation} onChange={(v) => update('nation', v)} />
              <TextField label="Address" value={form.address} onChange={(v) => update('address', v)} />

              <div className="mt-2 flex flex-col gap-4">
                <TextField label="Phone number" value={form.phoneNumber} onChange={(v) => update('phoneNumber', v)} />
                <TextField label="Email" type="email" value={form.email} onChange={(v) => update('email', v)} />
              </div>

              <div className="mt-2">
                <TextField
                  label="Admission date to Youth Union"
                  type="date"
                  value={form.youthUnionAdmissionDate}
                  onChange={(v) => update('youthUnionAdmissionDate', v)}
                />
              </div>

              <div className="mt-2 flex flex-col gap-4">
                <p className={labelClass}>Guardian information:</p>
                <TextField
                  label="Full name"
                  value={form.guardian.fullName}
                  onChange={(v) => updateGuardian('fullName', v)}
                />
                <TextField
                  label="Relationship"
                  value={form.guardian.relationship}
                  onChange={(v) => updateGuardian('relationship', v)}
                />
                <TextField
                  label="Phone number"
                  value={form.guardian.phoneNumber}
                  onChange={(v) => updateGuardian('phoneNumber', v)}
                />
              </div>
            </div>
          </section>

          <section className="flex flex-col rounded-3xl bg-white p-6 sm:p-8">
            <div className="flex flex-col gap-4">
              <ReadOnlyField label="Current credits" value={form.currentCredits} />

              <div>
                <p className={labelClass}>Scientific Article:</p>
                <div className="mt-2 flex flex-col gap-2">
                  {form.scientificArticles.map((article) => (
                    <div key={article.id} className="flex items-center gap-2 border-b border-black/50 pb-1">
                      <input
                        type="text"
                        value={article.title}
                        onChange={(e) => updateArticle(article.id, e.target.value)}
                        placeholder="Article title"
                        className="w-full border-0 bg-transparent font-body text-base text-notebook-ink outline-none placeholder:text-neutral-400"
                      />
                      <button
                        type="button"
                        onClick={() => removeArticle(article.id)}
                        aria-label="Remove article"
                        className="shrink-0 text-neutral-400 hover:text-neutral-700"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={addArticle}
                    aria-label="Add scientific article"
                    className="flex h-6 w-6 items-center justify-center self-start font-heading text-lg leading-none text-notebook-ink hover:text-notebook-blue"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-auto flex flex-col gap-4 pt-8">
              <ReadOnlyField label="Graduation year" value={form.graduationYear ?? '—'} />
              <ReadOnlyField label="GPA" value={form.gpa} />
            </div>
          </section>
        </div>
      </div>

      {onSave && (
        <div className="flex items-center gap-4">
          <button
            type="submit"
            disabled={submission === 'saving'}
            className="rounded-full bg-notebook-ink px-6 py-2.5 font-body text-sm text-white disabled:opacity-60"
          >
            {submission === 'saving' ? 'Saving…' : 'Save changes'}
          </button>
          {submission === 'success' && (
            <span className="font-body text-sm text-notebook-green">Saved!</span>
          )}
          {submission === 'error' && (
            <span className="font-body text-sm text-red-500">{errorMessage}</span>
          )}
        </div>
      )}
    </form>
  );
}