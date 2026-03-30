# PawPal+

A Streamlit app that helps pet owners plan and track daily care tasks for their pets.

## Features

- Chronological sorting: Tasks are sorted by actual time of day using time parsing, so `9:00 AM` always appears before `10:00 AM` regardless of input order
- Conflict detection: The scheduler scans all pending tasks and warns you if two tasks are scheduled at the same time, naming both tasks and pets involved
- Automatic recurrence: Marking a `daily` or `weekly` task complete auto-schedules the next occurrence with the correct due date, so nothing gets forgotten
- Completion filtering: A checkbox toggles between showing all tasks or pending-only, powered by the `filter_tasks()` method
- Priority sorting: Tasks can also be ranked by priority (1 = highest) as an alternative view
- Pet management: Add multiple pets, each with their own independent task list
- Date-based scheduling: Tasks can be scheduled for any date; Generate Schedule only shows tasks due today or earlier, so future tasks stay out of the way until their day arrives
- Inline edit and delete: Tasks in the schedule can be edited or deleted directly; changes take effect immediately without needing to regenerate the schedule

## 📸 Demo

<a href="/course_images/ai110/demo_1.png" target="_blank"><img src='/course_images/ai110/demo_1.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/demo_2.png" target="_blank"><img src='/course_images/ai110/demo_2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

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

## Smarter Scheduling

The scheduler does more than sort tasks by priority. It can sort tasks by actual time so 9:00 AM always comes before 10:00 AM. It checks for conflicts and warns you if two tasks are scheduled at the same time. When you mark a daily or weekly task as done, it automatically creates the next one so nothing gets forgotten. You can also filter tasks by pet or by whether they have been completed. Tasks can be added with any future date and will only appear in the generated schedule once their due date arrives.

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

## Testing PawPal+

### Run the test suite

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

- Task completion: Marking a task complete flips `is_complete` to `True`
- Pet task management: Adding a task increases the pet's task count
- Sorting correctness: Tasks are returned in chronological order; `9:00 AM` sorts before `10:00 AM` (guards against broken string comparison); unparseable times land at the end
- Recurrence logic: Completing a `daily` task creates a new task due the next day; `weekly` creates one 7 days later; `once` / non-recurring returns `None` with no new task added
- Conflict detection: Two pending tasks at the same time produce a warning; different times produce none; completed tasks are excluded from conflict checks; no tasks → no crash
- Due date scheduling: `due_date` defaults to today; future-dated tasks are correctly excluded from today's schedule; overdue tasks are included; `filter_tasks` combined with the date filter returns only eligible tasks
- Delete task bug: `remove_task` reduces the task count, removes only the correct task, and raises `ValueError` when the task is not found
- Edit task: `edit_task` replaces the task at the right index without affecting other tasks
- Pet management: `remove_pet` removes the correct pet; `edit_pet` updates the pet in place

### Confidence Level

**★★★★☆ (4/5)**

All core scheduling behaviors and the new date-based scheduling feature are covered by focused unit tests with both happy-path and edge-case scenarios, including the delete and edit bugs that were found and fixed. Confidence is high that the business logic is correct. One star is held back because the Streamlit UI layer (`app.py`) has no automated tests, so end-to-end user flows (form input, session state, rendering) remain unverified.
