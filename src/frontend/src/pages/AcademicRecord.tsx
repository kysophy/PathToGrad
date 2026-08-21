import {
  FormEvent,
  useEffect,
  useState,
} from 'react';

import {
  AcademicRecord,
  AcademicTerm,
  addAttempt,
  CourseOption,
  getAcademicRecord,
  getCourseOptions,
  getTerms,
  ResultStatus,
} from '../services/AcademicRecord';


export default function AcademicRecordPage() {
  const [record, setRecord] =
    useState<AcademicRecord | null>(null);

  const [courses, setCourses] =
    useState<CourseOption[]>([]);

  const [terms, setTerms] =
    useState<AcademicTerm[]>([]);


  const [courseCode, setCourseCode] =
    useState('');

  const [termId, setTermId] =
    useState('');

  const [attemptNumber, setAttemptNumber] =
    useState('1');

  const [grade, setGrade] =
    useState('');

  const [status, setStatus] =
    useState<ResultStatus>('Passed');

  const [creditsEarned, setCreditsEarned] =
    useState('');


  const [error, setError] =
    useState('');

  const [message, setMessage] =
    useState('');


  async function reloadRecord() {
    const result =
      await getAcademicRecord();

    setRecord(result);
  }


  useEffect(() => {
    async function load() {
      try {
        const [
          courseData,
          termData,
        ] = await Promise.all([
          getCourseOptions(),
          getTerms(),
        ]);

        setCourses(courseData);
        setTerms(termData);

        await reloadRecord();

      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load Academic Record.',
        );
      }
    }

    load();
  }, []);


  async function handleSubmit(
    event: FormEvent,
  ) {
    event.preventDefault();

    setError('');
    setMessage('');

    try {
      const result = await addAttempt({
        course_code: courseCode,
        term_id: termId,

        attempt_number:
          Number(attemptNumber),

        grade:
          grade.trim() === ''
            ? null
            : Number(grade),

        result_status: status,

        credits_earned:
          Number(creditsEarned),
      });

      setRecord(result);

      setMessage(
        'Course attempt saved successfully.',
      );

      setCourseCode('');
      setAttemptNumber('1');
      setGrade('');
      setCreditsEarned('');

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to save course attempt.',
      );
    }
  }


  return (
    <div className="p-6">

      <h1 className="font-heading text-4xl">
        Academic Record
      </h1>


      <div className="mt-5 rounded-2xl bg-[#FCFF61] p-5">

        <p className="font-heading text-2xl">
          Earned Credits
        </p>

        <p className="font-heading text-5xl">
          {record?.earned_credits ?? 0}
        </p>

      </div>


      {error && (
        <div className="mt-4 rounded-lg bg-red-100 p-3 text-red-700">
          {error}
        </div>
      )}


      {message && (
        <div className="mt-4 rounded-lg bg-green-100 p-3 text-green-700">
          {message}
        </div>
      )}


      <form
        onSubmit={handleSubmit}
        className="mt-6 grid gap-4 rounded-2xl bg-[#FEE1E7] p-5 md:grid-cols-3"
      >

        <label className="grid gap-1">
          <span>Course Code</span>

          <input
            list="course-list"
            value={courseCode}
            onChange={(e) =>
              setCourseCode(e.target.value)
            }
            className="rounded-lg border bg-white p-2"
            required
          />

          <datalist id="course-list">
            {courses.map((course) => (
              <option
                key={course.course_code}
                value={course.course_code}
              >
                {course.course_name}
              </option>
            ))}
          </datalist>
        </label>


        <label className="grid gap-1">
          <span>Academic Term</span>

          <select
            value={termId}
            onChange={(e) =>
              setTermId(e.target.value)
            }
            className="rounded-lg border bg-white p-2"
            required
          >

            <option value="">
              Select term
            </option>

            {terms.map((term) => (
              <option
                key={term.term_id}
                value={term.term_id}
              >
                {term.name}
              </option>
            ))}
          </select>
        </label>


        <label className="grid gap-1">
          <span>Attempt Number</span>

          <input
            type="number"
            value={attemptNumber}
            onChange={(e) =>
              setAttemptNumber(e.target.value)
            }
            className="rounded-lg border bg-white p-2"
            required
          />
        </label>


        <label className="grid gap-1">
          <span>Grade</span>

          <input
            type="number"
            step="0.1"
            value={grade}
            onChange={(e) =>
              setGrade(e.target.value)
            }
            className="rounded-lg border bg-white p-2"
          />
        </label>


        <label className="grid gap-1">
          <span>Status</span>

          <select
            value={status}
            onChange={(e) =>
              setStatus(e.target.value as ResultStatus)
            }
            className="rounded-lg border bg-white p-2"
          >

            <option value="Passed">
              Passed
            </option>

            <option value="Failed">
              Failed
            </option>

            <option value="InProgress">
              InProgress
            </option>

          </select>
        </label>


        <label className="grid gap-1">
          <span>Earned Credits</span>

          <input
            type="number"
            value={creditsEarned}
            onChange={(e) =>
              setCreditsEarned(
                e.target.value,
              )
            }
            className="rounded-lg border bg-white p-2"
            required
          />
        </label>


        <button
          type="submit"
          className="rounded-xl bg-[#0085FF] p-3 font-heading text-xl text-white md:col-span-3"
        >
          Add Attempt
        </button>

      </form>


      <div className="mt-8 overflow-x-auto">

        <table className="w-full border-collapse">

          <thead>
            <tr className="bg-[#D7D7D7]">

              <th className="border p-2">
                Course
              </th>

              <th className="border p-2">
                Term
              </th>

              <th className="border p-2">
                Attempt
              </th>

              <th className="border p-2">
                Grade
              </th>

              <th className="border p-2">
                Status
              </th>

              <th className="border p-2">
                Credits
              </th>

            </tr>
          </thead>


          <tbody>

            {record?.attempts.map(
              (attempt) => (
                <tr key={attempt.attempt_id}>

                  <td className="border p-2">
                    <strong>
                      {attempt.course_code}
                    </strong>

                    <br />

                    {attempt.course_name}
                  </td>

                  <td className="border p-2">
                    {attempt.term_name}
                  </td>

                  <td className="border p-2">
                    {attempt.attempt_number}
                  </td>

                  <td className="border p-2">
                    {attempt.grade ?? '—'}
                  </td>

                  <td className="border p-2">
                    {attempt.result_status}
                  </td>

                  <td className="border p-2">
                    {attempt.credits_earned}
                  </td>

                </tr>
              ),
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}
