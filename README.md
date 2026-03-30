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

## Smarter Scheduling

The scheduler does more than sort tasks by priority. It can sort tasks by actual time so 9:00 AM always comes before 10:00 AM. It checks for conflicts and warns you if two tasks are scheduled at the same time. When you mark a daily or weekly task as done, it automatically creates the next one so nothing gets forgotten. You can also filter tasks by pet or by whether they have been completed.

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

### Confidence Level

**★★★★☆ (4/5)**

The core scheduling behaviors — sorting, recurrence, and conflict detection — are all covered by focused unit tests with both happy-path and edge-case scenarios. Confidence is high that the business logic in `Scheduler` is correct. One star is held back because the Streamlit UI layer (`app.py`) has no automated tests, so end-to-end user flows (form input, session state, rendering) remain unverified.
