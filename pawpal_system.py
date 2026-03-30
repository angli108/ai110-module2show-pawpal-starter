from dataclasses import dataclass, field
from datetime import datetime, date, timedelta


@dataclass
class Task:
    task_activity: str
    time_available: str
    priority: int
    owner_preference: str
    frequency: str
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Marks the task as complete."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    gender: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Removes a task from the pet's task list."""
        self.tasks.remove(task)

    def edit_task(self, task: Task, updated_task: Task) -> None:
        """Replaces an existing task with an updated version."""
        index = self.tasks.index(task)
        self.tasks[index] = updated_task


class Scheduler:
    def __init__(self, owner: "Owner"):
        self.owner = owner

    def get_all_tasks(self) -> list[tuple["Pet", Task]]:
        """Returns all tasks across every pet the owner has."""
        return [(pet, task) for pet in self.owner.pets for task in pet.tasks]

    def get_pending_tasks(self) -> list[tuple["Pet", Task]]:
        """Returns only tasks that have not been marked complete."""
        return [(pet, task) for pet, task in self.get_all_tasks() if not task.is_complete]

    def get_tasks_for_pet(self, pet: "Pet") -> list[Task]:
        """Returns all tasks assigned to a specific pet."""
        return pet.tasks

    def get_tasks_by_priority(self) -> list[tuple["Pet", Task]]:
        """Returns all tasks sorted from highest to lowest priority."""
        return sorted(self.get_all_tasks(), key=lambda x: x[1].priority)

    def sort_by_time(self, tasks: list[tuple["Pet", Task]] | None = None) -> list[tuple["Pet", Task]]:
        """Returns tasks sorted chronologically by time_available.

        Parses time strings (e.g. '8:00 AM', '14:30') so '9:00 AM' correctly
        comes before '10:00 AM' instead of doing a raw string comparison.
        Tasks with unparseable times are placed at the end.

        Args:
            tasks: Optional subset to sort. If None, sorts all tasks.
        """
        source = tasks if tasks is not None else self.get_all_tasks()
        return sorted(source, key=lambda x: self._parse_time(x[1].time_available))

    def mark_task_complete(self, pet: "Pet", task: Task) -> Task | None:
        """Marks a task complete and auto-schedules the next occurrence if recurring.

        Uses timedelta to calculate the next due date:
          - 'daily'  → due_date + 1 day
          - 'weekly' → due_date + 7 days

        Args:
            pet: The pet the task belongs to.
            task: The task to mark complete.

        Returns:
            The newly created next-occurrence Task, or None if not recurring.
        """
        task.mark_complete()

        intervals = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        delta = intervals.get(task.frequency.lower())

        if delta is None:
            return None  # non-recurring frequency (e.g. "monthly", "once")

        next_task = Task(
            task_activity=task.task_activity,
            time_available=task.time_available,
            priority=task.priority,
            owner_preference=task.owner_preference,
            frequency=task.frequency,
            due_date=task.due_date + delta,
        )
        pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> list[str]:
        """Checks for tasks scheduled at the same time and returns warning messages.

        Compares every pair of pending tasks. If two tasks share the same
        parsed time, a warning string is appended to the results list rather
        than raising an exception, so the program keeps running.

        Returns:
            A list of warning strings, one per conflict found. Empty if none.
        """
        warnings = []
        pending = self.get_pending_tasks()

        for i in range(len(pending)):
            for j in range(i + 1, len(pending)):
                pet_a, task_a = pending[i]
                pet_b, task_b = pending[j]

                time_a = self._parse_time(task_a.time_available)
                time_b = self._parse_time(task_b.time_available)

                if time_a == time_b and time_a != datetime.max:
                    warnings.append(
                        f"  WARNING: '{task_a.task_activity}' ({pet_a.name}) and "
                        f"'{task_b.task_activity}' ({pet_b.name}) are both scheduled at {task_a.time_available}"
                    )

        return warnings

    @staticmethod
    def _parse_time(time_str: str) -> datetime:
        """Parses a time string ('8:00 AM' or '14:30') into a datetime for comparison."""
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                return datetime.strptime(time_str.strip(), fmt)
            except ValueError:
                continue
        return datetime.max

    def filter_tasks(
        self,
        pet_name: str | None = None,
        is_complete: bool | None = None,
    ) -> list[tuple["Pet", Task]]:
        """Returns tasks filtered by pet name and/or completion status.

        Args:
            pet_name: If provided, only return tasks belonging to this pet.
            is_complete: If True return only completed tasks; if False return
                only pending tasks; if None return both.
        """
        results = self.get_all_tasks()
        if pet_name is not None:
            results = [(pet, task) for pet, task in results if pet.name == pet_name]
        if is_complete is not None:
            results = [(pet, task) for pet, task in results if task.is_complete == is_complete]
        return results


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.scheduler = Scheduler(self)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Removes a pet from the owner's pet list."""
        self.pets.remove(pet)

    def edit_pet(self, pet: Pet, updated_pet: Pet) -> None:
        """Replaces an existing pet entry with an updated version."""
        index = self.pets.index(pet)
        self.pets[index] = updated_pet
