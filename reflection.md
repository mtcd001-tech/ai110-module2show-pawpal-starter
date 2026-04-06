# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The app is designed around three core user actions:

+ Manage pet & owner info: The user can enter and update information about themselves and their pet (name, species, age, and preferences). This provides context that the scheduler uses to personalize the daily plan.
+ Add and edit care tasks: The user can create care tasks such as walks, feeding, medication, grooming, and enrichment activities. Each task has at minimum a duration and a priority level.
+ Generate and view a daily plan: The app produces a daily schedule based on the user's available time and task priorities, and explains why tasks were included or excluded.

- What classes did you include, and what responsibilities did you assign to each?
The app is built around five classes:

- Owner: Holds information about the pet owner, including their name and how many minutes they have available in a day. Its main responsibility is providing the scheduler with time constraints.
- Pet: A simple data class storing the pet's name and species. It gives the scheduler context about who is being cared for.
- Task: Represents a single care activity (e.g. walk, feeding, medication). It stores the task name, category, duration in minutes, priority level (high/medium/low), and a preferred time of day. It can report whether it is urgent via `is_urgent()`.
- Scheduler: The core logic class. It holds a reference to the owner, the pet, and a list of tasks. Its main responsibility is generating a `DailyPlan` by sorting tasks by priority and fitting them into the owner's available time.
- DailyPlan: The output of the scheduler. It holds the list of scheduled tasks, the list of skipped tasks, and a reasoning string explaining why each decision was made.

**b. Design changes**

After reviewing the skeleton with Copilot, I made three changes to the design:

- **Added `Priority` and `TimePreference` enums**: Originally `priority` and `time_preference` were plain strings, which made the code fragile and hard to validate. Switching to enums prevents typos and makes the scheduler logic cleaner.
- **Added `last_plan: Optional[DailyPlan]` to `Scheduler`**: Copilot pointed out that `explain_plan()` had no plan to describe, since `Scheduler` never stored the result of `generate_plan()`. Adding this field makes the two methods work together correctly.
- **Changed `remove_task(task_name: str)` to `remove_task(task: Task)`**: Removing by name is ambiguous if two tasks share the same name. Accepting a `Task` object directly is more robust.

I did not add `Task.assigned_to` or time slot structures, as the app only supports one owner and one pet, and `available_minutes` is sufficient for a first version.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**


The scheduler detects conflicts by grouping high-priority tasks into time preference 
buckets (morning, afternoon, evening, any) and warning when more than one HIGH priority 
task shares the same bucket. This is a lightweight O(n) check that returns warning 
messages instead of blocking scheduling.

The tradeoff is that it does not check actual time overlaps based on duration — two 
tasks in the "morning" bucket could realistically fit back-to-back, but the scheduler 
still flags them as a conflict. This is reasonable for a first version because it 
keeps the logic simple and avoids over-engineering, while still giving the owner a 
useful heads-up to review their high-priority tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
