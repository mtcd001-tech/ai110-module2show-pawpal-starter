from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TimePreference(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    ANY = "any"


@dataclass
class Owner:
    name: str
    available_minutes: int

    def get_available_time(self) -> int:
        """Return available minutes for the owner."""
        return self.available_minutes

    def to_dict(self) -> Dict[str, object]:
        """Return owner data as a dictionary."""
        return {
            "name": self.name,
            "available_minutes": self.available_minutes,
        }


@dataclass
class Pet:
    name: str
    species: str

    def get_info(self) -> str:
        """Return formatted pet info."""
        return f"{self.name} the {self.species}"

    def to_dict(self) -> Dict[str, str]:
        """Return pet data as a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
        }


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: Priority
    time_preference: TimePreference
    completed: bool = False

    def is_urgent(self) -> bool:
        """Return True when the task priority is high."""
        return self.priority == Priority.HIGH

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def to_dict(self) -> Dict[str, object]:
        """Return task data as a dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority.value,
            "time_preference": self.time_preference.value,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            name=str(data["name"]),
            category=str(data["category"]),
            duration_minutes=int(data["duration_minutes"]),
            priority=Priority(str(data["priority"])),
            time_preference=TimePreference(str(data["time_preference"])),
            completed=bool(data.get("completed", False)),
        )


class DailyPlan:
    def __init__(self, scheduled: List[Task], skipped: List[Task], reasoning: str) -> None:
        self.scheduled: List[Task] = scheduled
        self.skipped: List[Task] = skipped
        self.reasoning: str = reasoning

    def summary(self) -> str:
        """Return a readable summary of scheduled and skipped tasks."""
        scheduled_lines = [
            f"- {task.name} ({task.category}, {task.duration_minutes} min, {task.priority.name})"
            for task in self.scheduled
        ]
        skipped_lines = [
            f"- {task.name} ({task.category}, {task.duration_minutes} min, {task.priority.name})"
            for task in self.skipped
        ]

        parts: List[str] = ["Daily Plan Summary:"]

        if scheduled_lines:
            parts.append("Scheduled tasks:")
            parts.extend(scheduled_lines)
        else:
            parts.append("No tasks were scheduled.")

        if skipped_lines:
            parts.append("Skipped tasks:")
            parts.extend(skipped_lines)
        else:
            parts.append("No tasks were skipped.")

        parts.append(f"Reasoning: {self.reasoning}")
        return "\n".join(parts)

    def total_duration(self) -> int:
        """Return total duration of scheduled tasks."""
        return sum(task.duration_minutes for task in self.scheduled)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]) -> None:
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.tasks: List[Task] = tasks
        self.last_plan: Optional[DailyPlan] = None

    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan from the current tasks."""
        priority_order = {
            Priority.HIGH: 0,
            Priority.MEDIUM: 1,
            Priority.LOW: 2,
        }

        sorted_tasks = sorted(self.tasks, key=lambda task: priority_order[task.priority])
        available = self.owner.get_available_time()
        scheduled: List[Task] = []
        skipped: List[Task] = []
        remaining_minutes = available

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_minutes:
                scheduled.append(task)
                remaining_minutes -= task.duration_minutes
            else:
                skipped.append(task)

        reasoning = (
            f"Scheduled {len(scheduled)} task(s) using {available - remaining_minutes} of {available} available minutes."
        )
        if skipped:
            reasoning += f" Skipped {len(skipped)} task(s) because they did not fit."

        plan = DailyPlan(scheduled=scheduled, skipped=skipped, reasoning=reasoning)
        self.last_plan = plan
        return plan

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduler."""
        if task in self.tasks:
            self.tasks.remove(task)

    def explain_plan(self) -> str:
        """Return the reasoning for the last generated plan."""
        if self.last_plan is None:
            return "No plan has been generated yet."
        return self.last_plan.reasoning
