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
    scheduler.add_task(task)
    assert len(scheduler.tasks) == initial_count + 1
