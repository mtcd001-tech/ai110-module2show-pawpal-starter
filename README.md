# PawPal+

PawPal+ is a Streamlit pet scheduling assistant that helps pet owners plan daily care tasks with smarter timing, priority handling, and recurring task automation. It produces a clear daily plan while highlighting conflicts and suggesting better scheduling choices.

## Overview

PawPal+ builds a daily care schedule for a pet owner by organizing tasks around time preference, priority, and available owner time. The app also supports recurring tasks and detects high-priority scheduling conflicts so users can keep care predictable and manageable.

## Features

- **Sorting by time preference**: Orders tasks in the natural daily flow of morning → afternoon → evening → any.
- **Filtering by priority/status**: Lets users view tasks by priority or completion status using scheduler filters.
- **Recurring task automation**: Completed daily or weekly tasks are re-created automatically for the next due date.
- **Conflict detection**: Warns when two or more HIGH priority tasks share the same time preference bucket.
- **Daily plan generation**: Builds a schedule based on available minutes and task constraints, then summarizes scheduled and skipped items.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Testing

Run the automated test suite with:

```bash
python -m pytest
```

## Smarter Scheduling

Phase 3 introduced more intelligent schedule generation by adding:

- time-preference-aware sorting for more natural daily task flow
- priority and completion filtering so users can focus on relevant tasks
- recurring task rescheduling after completion
- conflict detection for competing high-priority tasks
- a `DailyPlan` summary model for scheduled and skipped task reporting

## Demo

<a href="/course_images/ai110/screenshot.webp" target="_blank"><img src='/course_images/ai110/screenshot.webp' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
