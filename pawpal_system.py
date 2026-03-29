from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    gender: str
    age: int


@dataclass
class Task:
    pet: Pet
    task_activity: str
    time_available: str
    priority: int
    owner_preference: str


class Scheduler:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def edit_task(self, task: Task, updated_task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.scheduler = Scheduler()

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def edit_pet(self, pet: Pet, updated_pet: Pet) -> None:
        pass
