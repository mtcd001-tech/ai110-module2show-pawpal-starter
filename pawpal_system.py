from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Owner:
    name: str
    available_minutes: int

    def get_available_time(self) -> int:
        ...

    def to_dict(self) -> Dict[str, object]:
        ...


@dataclass
class Pet:
    name: str
    species: str

    def get_info(self) -> str:
        ...

    def to_dict(self) -> Dict[str, str]:
        ...


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str
    time_preference: str

    def is_urgent(self) -> bool:
        ...

    def to_dict(self) -> Dict[str, object]:
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Task":
        ...


class DailyPlan:
    def __init__(self, scheduled: List[Task], skipped: List[Task], reasoning: str) -> None:
        self.scheduled: List[Task] = scheduled
        self.skipped: List[Task] = skipped
        self.reasoning: str = reasoning

    def summary(self) -> str:
        ...

    def total_duration(self) -> int:
        ...


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]) -> None:
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.tasks: List[Task] = tasks

    def generate_plan(self) -> DailyPlan:
        ...

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, task_name: str) -> None:
        ...

    def explain_plan(self) -> str:
        ...
