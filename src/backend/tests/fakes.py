"""In-memory repositories for engine unit tests. No MySQL."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time

from app.deterministic.ports import PlanningRepos


@dataclass
class FakeCourse:
    course_id: str
    course_code: str
    name_vi: str = ""
    name_en: str = ""
    credits: int = 4
    status: str = "Active"

    def __post_init__(self) -> None:
        if not self.name_en:
            self.name_en = self.course_code
        if not self.name_vi:
            self.name_vi = self.course_code


@dataclass
class FakeCurrRow:
    course_id: str
    assigned_semester: int
    requirement_type: str
    spec_code: str = "GEN"


@dataclass
class FakePrereq:
    course_id: str
    required_course_id: str


@dataclass
class FakeAttempt:
    course_id: str
    attempt_number: int
    result_status: str
    grade: float | None = None
    credits_earned: int = 0
    record_id: str = "rec-1"
    term_id: str = "TERM-2026-1"
    attempt_id: str = ""

    def __post_init__(self) -> None:
        if not self.attempt_id:
            self.attempt_id = f"{self.course_id}-a{self.attempt_number}"


@dataclass
class FakeMeeting:
    day_of_week: str
    start_time: time
    end_time: time
    meeting_type: str = "LT"
    room: str = "I.11"
    section_id: str = ""
    meeting_id: str = ""


@dataclass
class FakeSection:
    section_id: str
    offering_id: str
    section_code: str
    capacity: int = 60
    status: str = "Active"
    meetings: list[FakeMeeting] = field(default_factory=list)


@dataclass
class FakeOffering:
    offering_id: str
    course_id: str
    term_id: str
    status: str = "Active"
    sections: list[FakeSection] = field(default_factory=list)


@dataclass
class FakeTerm:
    term_id: str
    name: str
    term_type: str


@dataclass
class FakeTrack:
    track_id: str
    name: str = "CLC"
    min_credits_per_term: int = 14
    max_credits_per_term: int = 24
    min_courses: int = 4
    max_courses: int = 6


@dataclass
class FakeProgram:
    program_id: str
    track: FakeTrack
    name: str = "Software Engineering Test Program"

    @property
    def track_id(self) -> str:
        return self.track.track_id


@dataclass
class FakeCurriculum:
    curriculum_id: str
    required_credits: int = 138
    program_id: str = "PROG-TEST-001"


@dataclass
class FakeProfile:
    student_id: str
    current_semester: int
    spec_code: str | None
    curriculum_id: str
    target_credit_load: int = 18
    program: FakeProgram | None = None
    curriculum: FakeCurriculum | None = None


@dataclass
class FakeRecord:
    record_id: str
    student_id: str


class FakeStudentRepository:
    def __init__(self, profiles: dict[str, FakeProfile]) -> None:
        self.profiles = profiles

    def get_profile(self, student_id: str) -> FakeProfile | None:
        return self.profiles.get(student_id)

    def get_with_policy(self, student_id: str) -> FakeProfile | None:
        return self.profiles.get(student_id)


class FakeCourseRepository:
    def __init__(
        self,
        courses: dict[str, FakeCourse],
        prereqs: list[FakePrereq],
    ) -> None:
        self.courses = courses
        self.prereqs = prereqs
        self._by_code = {c.course_code: c for c in courses.values()}

    def get_by_id(self, course_id: str) -> FakeCourse | None:
        return self.courses.get(course_id)

    def get_by_code(self, course_code: str) -> FakeCourse | None:
        return self._by_code.get(course_code)

    def get_prerequisites(self, course_id: str) -> list[FakeCourse]:
        required_ids = [
            edge.required_course_id
            for edge in self.prereqs
            if edge.course_id == course_id
        ]
        return [self.courses[rid] for rid in required_ids if rid in self.courses]

    def get_graph(self, course_ids: list[str] | None = None) -> list[FakePrereq]:
        if course_ids is None:
            return list(self.prereqs)
        wanted = set(course_ids)
        return [
            edge
            for edge in self.prereqs
            if edge.course_id in wanted or edge.required_course_id in wanted
        ]


class FakeCurriculumRepository:
    def __init__(
        self,
        curricula: dict[str, FakeCurriculum],
        rows: dict[str, list[tuple[FakeCurrRow, FakeCourse]]],
        tracks: dict[str, FakeTrack],
    ) -> None:
        self.curricula = curricula
        self.rows = rows
        self.tracks = tracks

    def get(self, curriculum_id: str) -> FakeCurriculum | None:
        return self.curricula.get(curriculum_id)

    def get_track(self, track_id: str) -> FakeTrack | None:
        return self.tracks.get(track_id)

    def list_courses_for_student(
        self,
        curriculum_id: str,
        spec_code: str | None,
    ) -> list[tuple[FakeCurrRow, FakeCourse]]:
        rows = self.rows.get(curriculum_id, [])
        result = []
        for row, course in rows:
            if row.spec_code == "GEN" or (
                spec_code and row.spec_code == spec_code
            ):
                result.append((row, course))
        return result

    def list_mandatory_courses(
        self,
        curriculum_id: str,
        spec_code: str | None,
    ) -> list[FakeCourse]:
        return [
            course
            for row, course in self.list_courses_for_student(
                curriculum_id, spec_code
            )
            if row.requirement_type == "Core"
        ]


class FakeAttemptRepository:
    def __init__(
        self,
        records: dict[str, FakeRecord],
        attempts: dict[str, list[FakeAttempt]],
        courses: dict[str, FakeCourse],
    ) -> None:
        self.records = records
        self.attempts = attempts
        self.courses = courses

    def get_record(self, student_id: str) -> FakeRecord | None:
        return self.records.get(student_id)

    def list_for_student(self, student_id: str) -> list[FakeAttempt]:
        record = self.get_record(student_id)
        if record is None:
            return []
        return list(self.attempts.get(record.record_id, []))

    def list_for_course(
        self,
        record_id: str,
        course_id: str,
    ) -> list[FakeAttempt]:
        return [
            attempt
            for attempt in self.attempts.get(record_id, [])
            if attempt.course_id == course_id
        ]

    def latest_per_course(self, record_id: str) -> list[FakeAttempt]:
        latest: dict[str, FakeAttempt] = {}
        for attempt in self.attempts.get(record_id, []):
            current = latest.get(attempt.course_id)
            if (
                current is None
                or attempt.attempt_number > current.attempt_number
            ):
                latest[attempt.course_id] = attempt
        return list(latest.values())


class FakeOfferingRepository:
    def __init__(
        self,
        terms: dict[str, FakeTerm],
        offerings: list[FakeOffering],
    ) -> None:
        self.terms = terms
        self.offerings = offerings
        self._sections: dict[str, FakeSection] = {}
        for offering in offerings:
            for section in offering.sections:
                self._sections[section.section_id] = section

    def get_term(self, term_id: str) -> FakeTerm | None:
        return self.terms.get(term_id)

    def get_active_offering(
        self,
        course_id: str,
        term_id: str,
    ) -> FakeOffering | None:
        for offering in self.offerings:
            if (
                offering.course_id == course_id
                and offering.term_id == term_id
                and offering.status == "Active"
            ):
                return offering
        return None

    def list_active_for_term(self, term_id: str) -> list[FakeOffering]:
        return [
            offering
            for offering in self.offerings
            if offering.term_id == term_id and offering.status == "Active"
        ]

    def list_sections_with_meetings(self, offering_id: str) -> list[FakeSection]:
        for offering in self.offerings:
            if offering.offering_id == offering_id:
                return [
                    section
                    for section in offering.sections
                    if section.status == "Active"
                ]
        return []

    def get_meetings(self, section_id: str) -> list[FakeMeeting]:
        section = self._sections.get(section_id)
        if section is None:
            return []
        return list(section.meetings)

    def get_offering_with_sections(
        self,
        course_id: str,
        term_id: str,
    ) -> FakeOffering | None:
        return self.get_active_offering(course_id, term_id)


def make_track(track_id: str = "TRACK-STD-001") -> FakeTrack:
    return FakeTrack(track_id=track_id)


def make_program(track: FakeTrack | None = None) -> FakeProgram:
    return FakeProgram(program_id="PROG-TEST-001", track=track or make_track())


def make_curriculum(curriculum_id: str = "CURR-TEST-2024") -> FakeCurriculum:
    return FakeCurriculum(curriculum_id=curriculum_id)


def default_term() -> FakeTerm:
    return FakeTerm(
        term_id="TERM-2026-1",
        name="2026.1",
        term_type="Semester2",
    )


def meeting(
    day: str,
    start: str,
    end: str,
    meeting_type: str = "LT",
    room: str = "I.11",
) -> FakeMeeting:
    sh, sm = (int(p) for p in start.split(":"))
    eh, em = (int(p) for p in end.split(":"))
    return FakeMeeting(
        day_of_week=day,
        start_time=time(sh, sm),
        end_time=time(eh, em),
        meeting_type=meeting_type,
        room=room,
    )


def section_with(
    section_id: str,
    offering_id: str,
    section_code: str,
    *meetings: FakeMeeting,
) -> FakeSection:
    attached = []
    for item in meetings:
        item.section_id = section_id
        attached.append(item)
    return FakeSection(
        section_id=section_id,
        offering_id=offering_id,
        section_code=section_code,
        meetings=attached,
    )


def offering_with(
    offering_id: str,
    course_id: str,
    term_id: str,
    *sections: FakeSection,
) -> FakeOffering:
    for item in sections:
        item.offering_id = offering_id
    return FakeOffering(
        offering_id=offering_id,
        course_id=course_id,
        term_id=term_id,
        sections=list(sections),
    )


def build_repos(
    *,
    student_id: str = "S1",
    current_semester: int = 5,
    spec_code: str | None = "SE",
    target_credit_load: int = 18,
    courses: list[FakeCourse],
    curr_rows: list[FakeCurrRow],
    prereqs: list[FakePrereq] | None = None,
    attempts: list[FakeAttempt] | None = None,
    offerings: list[FakeOffering] | None = None,
    term: FakeTerm | None = None,
    track: FakeTrack | None = None,
    required_credits: int = 138,
    record_id: str = "rec-1",
) -> PlanningRepos:
    term = term or default_term()
    track = track or make_track()
    program = make_program(track)
    curriculum = make_curriculum()
    curriculum.required_credits = required_credits
    profile = FakeProfile(
        student_id=student_id,
        current_semester=current_semester,
        spec_code=spec_code,
        curriculum_id=curriculum.curriculum_id,
        target_credit_load=target_credit_load,
        program=program,
        curriculum=curriculum,
    )
    course_map = {course.course_id: course for course in courses}
    row_pairs = []
    for row in curr_rows:
        row_pairs.append((row, course_map[row.course_id]))
    record = FakeRecord(record_id=record_id, student_id=student_id)
    attempt_rows = list(attempts or [])
    for attempt in attempt_rows:
        attempt.record_id = record_id
    return PlanningRepos(
        students=FakeStudentRepository({student_id: profile}),
        courses=FakeCourseRepository(course_map, list(prereqs or [])),
        curriculum=FakeCurriculumRepository(
            {curriculum.curriculum_id: curriculum},
            {curriculum.curriculum_id: row_pairs},
            {track.track_id: track},
        ),
        attempts=FakeAttemptRepository(
            {student_id: record},
            {record_id: attempt_rows},
            course_map,
        ),
        offerings=FakeOfferingRepository({term.term_id: term}, list(offerings or [])),
    )
