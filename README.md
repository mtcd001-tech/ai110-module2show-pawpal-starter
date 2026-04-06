# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes several intelligent scheduling features:

- **Sort by time preference**: Tasks are automatically ordered morning → afternoon → evening → any for a natural daily flow.
- **Filter tasks**: Filter by priority level or completion status to focus on what matters.
- **Recurring tasks**: Daily and weekly tasks auto-reschedule after being marked complete, using `timedelta` to calculate the next due date.
- **Conflict detection**: The scheduler warns when two or more HIGH priority tasks share the same time slot, helping owners avoid overbooking.

## Testing PawPal+

To run the test suite:
```bash
python -m pytest
```

### What the tests cover

- **Task completion**: Verifying that `mark_complete()` changes the task status to `True`
- **Task addition**: Verifying that adding a task increases the scheduler's task count
- **Sorting correctness**: Verifying that `sort_by_time()` returns tasks in order morning → afternoon → evening → any
- **Recurrence logic**: Verifying that a daily task gets a new copy with `due_date = today + 1` after `reschedule_recurring()`
- **Conflict detection**: Verifying that `detect_conflicts()` flags two HIGH priority tasks in the same time slot

### Confidence level

 (4/5) — Core scheduling logic is well tested. Edge cases like weekly recurrence and exact-fit scheduling could use more coverage.