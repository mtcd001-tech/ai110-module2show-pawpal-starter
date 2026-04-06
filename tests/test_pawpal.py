import pytest
from datetime import date, timedelta

from pawpal_system import Owner, Pet, Priority, TimePreference, Task, Scheduler


def test_mark_complete_sets_completed_true() -> None:
    task = Task(
        name="Feed Bella",
        category="feeding",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        time_preference=TimePreference.MORNING,
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


@pytest.fixture
def scheduler_fixture() -> Scheduler:
    owner = Owner(name="Alex", available_minutes=120)
    pet = Pet(name="Bella", species="dog")
    tasks = [
        Task(
            name="Morning meds",
            category="care",
            duration_minutes=10,
            priority=Priority.MEDIUM,
            time_preference=TimePreference.MORNING,
        ),
        Task(
            name="Afternoon walk",
            category="exercise",
            duration_minutes=30,
            priority=Priority.LOW,
            time_preference=TimePreference.AFTERNOON,
        ),
        Task(
            name="Evening grooming",
            category="grooming",
            duration_minutes=20,
            priority=Priority.HIGH,
            time_preference=TimePreference.EVENING,
        ),
        Task(
            name="Flexible play",
            category="play",
            duration_minutes=15,
            priority=Priority.MEDIUM,
            time_preference=TimePreference.ANY,
        ),
    ]
    return Scheduler(owner=owner, pet=pet, tasks=list(tasks))


def test_sort_by_time_returns_tasks_in_preference_order(scheduler_fixture: Scheduler) -> None:
    sorted_tasks = scheduler_fixture.sort_by_time()
    assert [task.time_preference for task in sorted_tasks] == [
        TimePreference.MORNING,
        TimePreference.AFTERNOON,
        TimePreference.EVENING,
        TimePreference.ANY,
    ]


def test_daily_task_reschedules_after_completion(scheduler_fixture: Scheduler) -> None:
    daily_task = Task(
        name="Feed Bella",
        category="feeding",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        time_preference=TimePreference.MORNING,
        recurrence="daily",
        due_date=date.today(),
    )
    scheduler_fixture.tasks.append(daily_task)

    daily_task.mark_complete()
    scheduler_fixture.reschedule_recurring()

    new_tasks = [
        task for task in scheduler_fixture.tasks
        if task.name == daily_task.name and not task.completed
    ]
    assert len(new_tasks) == 1
    assert new_tasks[0].due_date == date.today() + timedelta(days=1)


def test_detect_conflicts_returns_warning_for_same_time_high_priority(scheduler_fixture: Scheduler) -> None:
    scheduler_fixture.tasks.extend([
        Task(
            name="Vet visit",
            category="health",
            duration_minutes=20,
            priority=Priority.HIGH,
            time_preference=TimePreference.MORNING,
        ),
        Task(
            name="Walk Bella",
            category="exercise",
            duration_minutes=30,
            priority=Priority.HIGH,
            time_preference=TimePreference.MORNING,
        ),
    ])

    warnings = scheduler_fixture.detect_conflicts()
    assert len(warnings) == 1
    assert "high-priority tasks share morning" in warnings[0]


def test_add_task_increases_scheduler_task_count() -> None:
    owner = Owner(name="Alex", available_minutes=90)
    pet = Pet(name="Bella", species="dog")
    scheduler = Scheduler(owner=owner, pet=pet, tasks=[])
    task = Task(
        name="Walk Bella",
        category="exercise",
        duration_minutes=30,
        priority=Priority.HIGH,
        time_preference=TimePreference.AFTERNOON,
    )

    initial_count = len(scheduler.tasks)
    scheduler.tasks.append(task)
    assert len(scheduler.tasks) == initial_count + 1
