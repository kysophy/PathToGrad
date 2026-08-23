"""Duck-typed repository bundle for the engine.

The engine never opens a SQLAlchemy Session. Callers (services, tests) build
repositories and pass them in. Tests can pass in-memory fakes with the same
method names — no MySQL required.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlanningRepos:
    students: Any
    courses: Any
    curriculum: Any
    attempts: Any
    offerings: Any
