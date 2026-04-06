from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TimePreference

owner = Owner(name="Alex", available_minutes=90)
pet = Pet(name="Mochi", species="dog")

tasks = [
    Task(name="Morning walk", category="exercise", duration_minutes=30, priority=Priority.HIGH, time_preference=TimePreference.MORNING),
    Task(name="Feeding", category="nutrition", duration_minutes=10, priority=Priority.HIGH, time_preference=TimePreference.MORNING),
    Task(name="Enrichment play", category="enrichment", duration_minutes=20, priority=Priority.MEDIUM, time_preference=TimePreference.AFTERNOON),
    Task(name="Grooming", category="grooming", duration_minutes=15, priority=Priority.LOW, time_preference=TimePreference.ANY),
]

scheduler = Scheduler(owner=owner, pet=pet, tasks=tasks)
plan = scheduler.generate_plan()
print(plan.summary())