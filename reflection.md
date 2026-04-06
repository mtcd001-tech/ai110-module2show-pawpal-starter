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

The scheduler considers two main constraints: the owner's available minutes per day, and each task's priority level. Tasks are sorted by a composite key that ranks daily recurring tasks first, then orders by time preference (morning before afternoon before evening), then by priority (high before medium before low). Completed tasks are filtered out before scheduling begins.

I decided that time preference and recurrence mattered most because they reflect the natural structure of a pet care day. A feeding task that must happen in the morning should not be pushed aside by a low-priority afternoon task just because it was added to the list later.

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

I used AI tools throughout the project for design brainstorming, generating class skeletons, implementing scheduling logic, writing tests, and refining the UI. The most helpful prompts were specific ones that referenced actual files using `#file:` or `#codebase`, and prompts that asked for comparisons between approaches rather than just a single solution. For example, asking Copilot to compare two sorting strategies helped me understand the tradeoffs before choosing one.

**b. Judgment and verification**

When Copilot reviewed my skeleton, it suggested adding `Task.assigned_to: Owner` and `Task.pet: Pet` fields to create a stronger association between tasks and their owners. I rejected this suggestion because the app only supports a single owner and a single pet. Adding those fields would have introduced unnecessary complexity and required changes throughout the codebase with no practical benefit for the current scope.

I evaluated the suggestion by asking whether it would change any observable behavior in the app. Since the scheduler already receives the owner and pet directly, the extra fields on Task would have been redundant. I kept the simpler design and noted the change as a potential future improvement if the app ever needs to support multiple pets.

I also chose not to accept Copilot's suggestion to inline the sort key as a lambda directly inside `sorted()`. The named helper function `task_sort_key` is slightly more verbose but significantly easier to read and modify. Readability mattered more than conciseness here.

Using separate chat sessions for different phases helped keep context focused. The design session stayed on UML and class structure. The algorithm session stayed on sorting, filtering, and conflict logic. The testing session stayed on edge cases and fixtures. Mixing these concerns in a single session would have made it harder to get precise, relevant suggestions.



## 4. Testing and Verification

**a. What you tested**

I tested five core behaviors: task completion status via `mark_complete()`, task addition via `add_task()`, sorting correctness via `sort_by_time()`, recurring task rescheduling after completion, and conflict detection when two HIGH priority tasks share a time slot. These tests were important because they cover the behaviors most likely to break silently — a sort that returns the wrong order, a recurring task that fails to reschedule, or a conflict that goes undetected would all produce incorrect plans without raising an exception.

**b. Confidence**

I am moderately confident the core scheduling logic works correctly for the happy path and the cases I tested. The areas I would test next are: weekly recurrence with date boundary conditions, a scheduler where available minutes is zero, tasks where duration exactly equals remaining time, and the interaction between filtering and scheduling when some tasks are already completed.

---

## 5. Reflection

**a. What went well**

The scheduling logic came together cleanly. The decision to use a single composite sort key for recurrence, time preference, and priority made `generate_plan()` easy to read and extend. The CLI-first workflow of building and verifying logic in `main.py` before connecting to Streamlit also prevented UI issues from masking backend bugs.

**b. What you would improve**

If I had another iteration, I would add a time slot model to replace the bucket-based conflict detection. Rather than grouping tasks into morning, afternoon, evening, and any, I would assign actual start and end times and check for duration-based overlaps. This would eliminate false conflict warnings for tasks that fit comfortably in the same part of the day.

**c. Key takeaway**

The most important thing I learned is that AI tools are most useful when the developer has already made the key architectural decisions. Copilot generated better code once I had defined the class structure, chosen the data types, and decided how the scheduler should work. When I asked open-ended questions without context, the suggestions were generic. When I asked specific questions grounded in my actual files, the suggestions were precise and actionable. The lead architect role is not about writing every line of code — it is about making decisions that give the AI enough structure to be genuinely helpful.
