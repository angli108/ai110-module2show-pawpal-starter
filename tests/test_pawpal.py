from pawpal_system import Task, Pet


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


if __name__ == "__main__":
    test_mark_complete_changes_status()
    print("PASSED: mark_complete changes task status")

    test_add_task_increases_pet_task_count()
    print("PASSED: add_task increases pet task count")
