import {
  FormEvent,
  useEffect,
  useState,
} from 'react';

import {
  AcademicProgram,
  Faculty,
  getCurriculum,
  getFaculties,
  getProfile,
  getPrograms,
  getTracks,
  ProfileFormData,
  ProgramTrack,
  saveProfile,
} from '../services/Profile';
import { getCurrentStudentId } from '../services/session';


export default function ProfilePage() {
  const [faculties, setFaculties] =
    useState<Faculty[]>([]);

  const [tracks, setTracks] =
    useState<ProgramTrack[]>([]);

  const [programs, setPrograms] =
    useState<AcademicProgram[]>([]);

  const [facultyId, setFacultyId] =
    useState('');

  const [trackId, setTrackId] =
    useState('');

  const [programId, setProgramId] =
    useState('');

  const [intakeYear, setIntakeYear] =
    useState('2024');

  const [currentSemester, setCurrentSemester] =
    useState('1');

  const [targetCreditLoad, setTargetCreditLoad] =
    useState('18');

  const [curriculumVersion, setCurriculumVersion] =
    useState<string | null>(null);

  const [message, setMessage] =
    useState('');

  const [error, setError] =
    useState('');


  useEffect(() => {
    async function loadOptions() {
      try {
        const [
          facultyData,
          trackData,
        ] = await Promise.all([
          getFaculties(),
          getTracks(),
        ]);

        setFaculties(facultyData);
        setTracks(trackData);

        try {
          const profile = await getProfile();

          setFacultyId(profile.faculty_id);
          setTrackId(profile.track_id);
          setProgramId(profile.program_id);

          setIntakeYear(
            String(profile.intake_year),
          );

          setCurrentSemester(
            String(profile.current_semester),
          );

          setTargetCreditLoad(
            String(profile.target_credit_load),
          );

          setCurriculumVersion(
            profile.curriculum_version,
          );
        } catch {
          // No profile exists yet.
        }

      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load profile options.',
        );
      }
    }

    loadOptions();
  }, []);


  useEffect(() => {
    async function loadPrograms() {
      if (!facultyId || !trackId) {
        setPrograms([]);
        return;
      }

      try {
        const result = await getPrograms(
          facultyId,
          trackId,
        );

        setPrograms(result);

      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load programs.',
        );
      }
    }

    loadPrograms();

  }, [
    facultyId,
    trackId,
  ]);


  useEffect(() => {
    async function loadCurriculum() {
      if (
        !programId
        || !intakeYear
      ) {
        setCurriculumVersion(null);
        return;
      }

      try {
        const result = await getCurriculum(
          programId,
          Number(intakeYear),
        );

        setCurriculumVersion(
          result.version,
        );

      } catch {
        setCurriculumVersion(null);
      }
    }

    loadCurriculum();

  }, [
    programId,
    intakeYear,
  ]);


  async function handleSubmit(
    event: FormEvent,
  ) {
    event.preventDefault();

    setError('');
    setMessage('');

    const payload: ProfileFormData = {
      faculty_id: facultyId,
      track_id: trackId,
      program_id: programId,

      intake_year: Number(intakeYear),
      current_semester:
        Number(currentSemester),

      target_credit_load:
        Number(targetCreditLoad),
    };

    try {
      const result =
        await saveProfile(payload);

      setCurriculumVersion(
        result.curriculum_version,
      );

      if (result.warning) {
        setMessage(result.warning);
      } else {
        setMessage(
          'Profile saved successfully.',
        );
      }

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to save profile.',
      );
    }
  }


  return (
    <div className="p-6">
      <div className="mx-auto max-w-3xl rounded-2xl bg-[#FEE1E7] p-6 shadow-sm">

        <h1 className="font-heading text-4xl">
          Academic Profile
        </h1>

        <p className="mt-1 font-body text-sm">
          Student ID: {getCurrentStudentId()}
        </p>


        {error && (
          <div className="mt-4 rounded-lg bg-red-100 p-3 font-body text-red-700">
            {error}
          </div>
        )}


        {message && (
          <div className="mt-4 rounded-lg bg-yellow-100 p-3 font-body">
            {message}
          </div>
        )}


        <form
          onSubmit={handleSubmit}
          className="mt-6 grid gap-5"
        >

          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Faculty
            </span>

            <select
              value={facultyId}
              onChange={(e) => {
                setFacultyId(e.target.value);
                setProgramId('');
              }}
              className="rounded-lg border bg-white p-3"
              required
            >
              <option value="">
                Select faculty
              </option>

              {faculties.map((item) => (
                <option
                  key={item.faculty_id}
                  value={item.faculty_id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Program Track
            </span>

            <select
              value={trackId}
              onChange={(e) => {
                setTrackId(e.target.value);
                setProgramId('');
              }}
              className="rounded-lg border bg-white p-3"
              required
            >
              <option value="">
                Select track
              </option>

              {tracks.map((item) => (
                <option
                  key={item.track_id}
                  value={item.track_id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Academic Program
            </span>

            <select
              value={programId}
              onChange={(e) =>
                setProgramId(e.target.value)
              }
              className="rounded-lg border bg-white p-3"
              required
            >
              <option value="">
                Select academic program
              </option>

              {programs.map((item) => (
                <option
                  key={item.program_id}
                  value={item.program_id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Intake Year
            </span>

            <input
              type="number"
              value={intakeYear}
              onChange={(e) =>
                setIntakeYear(e.target.value)
              }
              className="rounded-lg border bg-white p-3"
              required
            />
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Curriculum Version
            </span>

            <input
              value={
                curriculumVersion
                ?? 'No matching curriculum'
              }
              readOnly
              className="rounded-lg border bg-gray-100 p-3"
            />
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Current Semester
            </span>

            <input
              type="number"
              value={currentSemester}
              onChange={(e) =>
                setCurrentSemester(
                  e.target.value,
                )
              }
              className="rounded-lg border bg-white p-3"
              required
            />
          </label>


          <label className="grid gap-1">
            <span className="font-heading text-lg">
              Target Credit Load
            </span>

            <input
              type="number"
              value={targetCreditLoad}
              onChange={(e) =>
                setTargetCreditLoad(
                  e.target.value,
                )
              }
              className="rounded-lg border bg-white p-3"
              required
            />
          </label>


          <button
            type="submit"
            className="rounded-xl bg-[#0085FF] px-5 py-3 font-heading text-xl text-white"
          >
            Save Profile
          </button>

        </form>
      </div>
    </div>
  );
}
