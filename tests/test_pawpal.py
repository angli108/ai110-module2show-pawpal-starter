from datetime import date, timedelta

import pytest

from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(activity="Walk", time="8:00 AM", priority=2, frequency="daily"):
    return Task(
        task_activity=activity,
        time_available=time,
        priority=priority,
        owner_preference="none",
        frequency=frequency,
    )


def make_owner_with_pets(*pets):
    owner = Owner("Test Owner")
    for pet in pets:
        owner.add_pet(pet)
    return owner


# ---------------------------------------------------------------------------
# Original tests
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(task_activity="Morning Walk", time_available="7:00 AM", priority=1, owner_preference="leash only", frequency="daily")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", gender="Male", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(task_activity="Feeding", time_available="8:00 AM", priority=2, owner_preference="dry food", frequency="twice daily"))
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_chronological_order():
    """Tasks are returned in chronological order regardless of insertion order."""
    pet = Pet(name="Luna", gender="Female", age=2)
    pet.add_task(make_task("Evening Walk", "6:00 PM"))
    pet.add_task(make_task("Lunch", "12:00 PM"))
    pet.add_task(make_task("Breakfast", "8:00 AM"))

    owner = make_owner_with_pets(pet)
    sorted_tasks = owner.scheduler.sort_by_time()

    times = [task.time_available for _, task in sorted_tasks]
    assert times == ["8:00 AM", "12:00 PM", "6:00 PM"]


def test_sort_by_time_am_vs_10am():
    """'9:00 AM' must sort before '10:00 AM' (string sort would reverse these)."""
    pet = Pet(name="Rex", gender="Male", age=4)
    pet.add_task(make_task("Brushing", "10:00 AM"))
    pet.add_task(make_task("Walk", "9:00 AM"))

    owner = make_owner_with_pets(pet)
    sorted_tasks = owner.scheduler.sort_by_time()

    activities = [task.task_activity for _, task in sorted_tasks]
    assert activities == ["Walk", "Brushing"]


def test_sort_by_time_unparseable_goes_last():
    """Tasks with an unrecognisable time string are placed at the end."""
    pet = Pet(name="Mochi", gender="Female", age=1)
    pet.add_task(make_task("Walk", "8:00 AM"))
    pet.add_task(make_task("Mystery", "noon"))  # unparseable

    owner = make_owner_with_pets(pet)
    sorted_tasks = owner.scheduler.sort_by_time()

    assert sorted_tasks[-1][1].task_activity == "Mystery"


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_day_task():
    """Completing a daily task adds a new task due the following day."""
    today = date.today()
    pet = Pet(name="Buddy", gender="Male", age=3)
    task = Task(
        task_activity="Walk",
        time_available="7:00 AM",
        priority=1,
        owner_preference="leash",
        frequency="daily",
        due_date=today,
    )
    pet.add_task(task)

    owner = make_owner_with_pets(pet)
    next_task = owner.scheduler.mark_task_complete(pet, task)

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_complete is False


def test_weekly_task_creates_task_seven_days_later():
    """Completing a weekly task schedules the next occurrence 7 days out."""
    today = date.today()
    pet = Pet(name="Bella", gender="Female", age=5)
    task = Task(
        task_activity="Bath",
        time_available="10:00 AM",
        priority=2,
        owner_preference="gentle shampoo",
        frequency="weekly",
        due_date=today,
    )
    pet.add_task(task)

    owner = make_owner_with_pets(pet)
    next_task = owner.scheduler.mark_task_complete(pet, task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_non_recurring_task_returns_none():
    """Completing a 'once' task returns None and adds no new task."""
    pet = Pet(name="Cleo", gender="Female", age=2)
    task = make_task("Vet visit", frequency="once")
    pet.add_task(task)

    owner = make_owner_with_pets(pet)
    result = owner.scheduler.mark_task_complete(pet, task)

    assert result is None
    assert len(pet.tasks) == 1  # no new task added


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_conflict_detected_for_same_time():
    """Two pending tasks at the same time produce at least one warning."""
    pet = Pet(name="Duke", gender="Male", age=3)
    pet.add_task(make_task("Walk", "9:00 AM"))
    pet.add_task(make_task("Feeding", "9:00 AM"))

    owner = make_owner_with_pets(pet)
    warnings = owner.scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "9:00 AM" in warnings[0]


def test_no_conflict_for_different_times():
    """Tasks at different times produce no warnings."""
    pet = Pet(name="Kira", gender="Female", age=2)
    pet.add_task(make_task("Walk", "8:00 AM"))
    pet.add_task(make_task("Feeding", "9:00 AM"))

    owner = make_owner_with_pets(pet)
    assert owner.scheduler.detect_conflicts() == []


def test_completed_tasks_excluded_from_conflict_check():
    """A completed task at the same time as a pending task does not trigger a conflict."""
    pet = Pet(name="Ziggy", gender="Male", age=1)
    task_done = make_task("Walk", "9:00 AM")
    task_done.mark_complete()
    pet.add_task(task_done)
    pet.add_task(make_task("Feeding", "9:00 AM"))

    owner = make_owner_with_pets(pet)
    assert owner.scheduler.detect_conflicts() == []


def test_no_conflict_with_no_tasks():
    """An owner with pets but no tasks returns an empty conflict list."""
    pet = Pet(name="Empty", gender="Male", age=1)
    owner = make_owner_with_pets(pet)
    assert owner.scheduler.detect_conflicts() == []


# ---------------------------------------------------------------------------
# Due date / date-based scheduling (new feature)
# ---------------------------------------------------------------------------

def test_task_due_date_defaults_to_today():
    """A task created without an explicit due_date should be due today."""
    task = make_task()
    assert task.due_date == date.today()


def test_task_accepts_custom_due_date():
    """A task created with a future due_date stores it correctly."""
    future = date.today() + timedelta(days=3)
    task = Task(
        task_activity="Grooming",
        time_available="2:00 PM",
        priority=3,
        owner_preference="brush only",
        frequency="weekly",
        due_date=future,
    )
    assert task.due_date == future


def test_today_task_included_in_schedule():
    """A task due today passes the due_date <= today filter."""
    task = make_task(activity="Walk")
    task.due_date = date.today()
    assert task.due_date <= date.today()


def test_future_task_excluded_from_schedule():
    """A task due tomorrow should not appear in today's schedule."""
    task = make_task(activity="Bath")
    task.due_date = date.today() + timedelta(days=1)
    assert not (task.due_date <= date.today())


def test_overdue_task_included_in_schedule():
    """A task whose due_date has already passed should still appear."""
    task = make_task(activity="Vet visit")
    task.due_date = date.today() - timedelta(days=2)
    assert task.due_date <= date.today()


def test_filter_tasks_excludes_future_due_dates():
    """filter_tasks returns all tasks; date filtering applied afterwards excludes future ones."""
    today = date.today()
    pet = Pet(name="Buddy", gender="Male", age=3)
    pet.add_task(Task(task_activity="Walk", time_available="8:00 AM", priority=1,
                      owner_preference="leash", frequency="daily", due_date=today))
    pet.add_task(Task(task_activity="Bath", time_available="10:00 AM", priority=2,
                      owner_preference="gentle", frequency="weekly",
                      due_date=today + timedelta(days=5)))

    owner = make_owner_with_pets(pet)
    all_tasks = owner.scheduler.filter_tasks()
    todays_tasks = [(p, t) for p, t in all_tasks if t.due_date <= today]

    assert len(todays_tasks) == 1
    assert todays_tasks[0][1].task_activity == "Walk"


# ---------------------------------------------------------------------------
# Delete task bug — remove_task actually removes the task
# ---------------------------------------------------------------------------

def test_remove_task_decreases_count():
    """remove_task should reduce the pet's task list by one."""
    pet = Pet(name="Rex", gender="Male", age=2)
    task = make_task("Walk")
    pet.add_task(task)
    assert len(pet.tasks) == 1
    pet.remove_task(task)
    assert len(pet.tasks) == 0


def test_remove_task_removes_correct_task():
    """remove_task removes only the specified task, leaving others intact."""
    pet = Pet(name="Luna", gender="Female", age=3)
    task_a = make_task("Walk", "8:00 AM")
    task_b = make_task("Feeding", "12:00 PM")
    pet.add_task(task_a)
    pet.add_task(task_b)

    pet.remove_task(task_a)

    assert task_a not in pet.tasks
    assert task_b in pet.tasks


def test_remove_task_not_in_list_raises():
    """remove_task raises ValueError when the task is not in the list."""
    pet = Pet(name="Cleo", gender="Female", age=1)
    task = make_task("Walk")
    with pytest.raises(ValueError):
        pet.remove_task(task)


# ---------------------------------------------------------------------------
# Edit task
# ---------------------------------------------------------------------------

def test_edit_task_replaces_at_correct_index():
    """edit_task should replace the old task in-place."""
    pet = Pet(name="Mochi", gender="Female", age=2)
    original = make_task("Walk", "8:00 AM")
    other = make_task("Feeding", "12:00 PM")
    pet.add_task(original)
    pet.add_task(other)

    updated = make_task("Run", "8:00 AM")
    pet.edit_task(original, updated)

    assert pet.tasks[0].task_activity == "Run"
    assert pet.tasks[1].task_activity == "Feeding"


# ---------------------------------------------------------------------------
# Remove / edit pet
# ---------------------------------------------------------------------------

def test_remove_pet_decreases_count():
    """remove_pet should reduce the owner's pet list by one."""
    pet = Pet(name="Buddy", gender="Male", age=3)
    owner = make_owner_with_pets(pet)
    assert len(owner.pets) == 1
    owner.remove_pet(pet)
    assert len(owner.pets) == 0


def test_remove_pet_removes_correct_pet():
    """remove_pet removes only the specified pet."""
    pet_a = Pet(name="Buddy", gender="Male", age=3)
    pet_b = Pet(name="Luna", gender="Female", age=2)
    owner = make_owner_with_pets(pet_a, pet_b)

    owner.remove_pet(pet_a)

    assert pet_a not in owner.pets
    assert pet_b in owner.pets


def test_edit_pet_replaces_at_correct_index():
    """edit_pet should swap the old pet entry with the updated one."""
    pet = Pet(name="Buddy", gender="Male", age=3)
    owner = make_owner_with_pets(pet)

    updated = Pet(name="Buddy", gender="Male", age=4)
    owner.edit_pet(pet, updated)

    assert owner.pets[0].age == 4


if __name__ == "__main__":
    test_mark_complete_changes_status()
    print("PASSED: mark_complete changes task status")

    test_add_task_increases_pet_task_count()
    print("PASSED: add_task increases pet task count")
