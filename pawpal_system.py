from dataclasses import dataclass, field


@dataclass
class Task:
    task_activity: str
    time_available: str
    priority: int
    owner_preference: str
    frequency: str
    is_complete: bool = False

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
