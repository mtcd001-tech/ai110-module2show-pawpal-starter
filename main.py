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
# Add tasks out of order
scheduler.add_task(Task(
    name="Evening cuddle",
    category="enrichment",
    duration_minutes=15,
    priority=Priority.LOW,
    time_preference=TimePreference.EVENING
))
scheduler.add_task(Task(
    name="Afternoon meds",
    category="medication",
    duration_minutes=5,
    priority=Priority.HIGH,
    time_preference=TimePreference.AFTERNOON
))

# Test sort_by_time
print("\nTasks sorted by time:")
for t in scheduler.sort_by_time():
    print(f"  [{t.time_preference.value}] {t.name}")

# Test filter_tasks
print("\nIncomplete tasks only:")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.name} (done={t.completed})")

# Test conflict detection — two HIGH priority tasks in the same time slot
scheduler.add_task(Task(
    name="Morning bath",
    category="grooming",
    duration_minutes=20,
    priority=Priority.HIGH,
    time_preference=TimePreference.MORNING
))

print("\nConflict detection:")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠ {warning}")
else:
    print("  No conflicts detected.")