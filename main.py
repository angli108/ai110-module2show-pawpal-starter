from pawpal_system import Task, Pet, Owner

owner = Owner("Alex")

pet1 = Pet(name="Buddy", gender="Male", age=3)
pet2 = Pet(name="Luna", gender="Female", age=5)

owner.add_pet(pet1)
owner.add_pet(pet2)

#Add tasks
pet1.add_task(Task(task_activity="Morning Walk", time_available="7:00 AM", priority=1, owner_preference="leash only", frequency="daily"))
pet1.add_task(Task(task_activity="Feeding", time_available="8:00 AM", priority=2, owner_preference="dry food", frequency="twice daily"))
pet2.add_task(Task(task_activity="Grooming", time_available="3:00 PM", priority=3, owner_preference="brush only", frequency="weekly"))

#Today's Schedule
print(f"=== Today's Schedule for {owner.name} ===\n")

for pet, task in owner.scheduler.get_tasks_by_priority():
    status = "✓" if task.is_complete else "○"
    print(f"  {status} [{task.time_available}] {pet.name} — {task.task_activity}")
    print(f"       Priority: {task.priority} | Frequency: {task.frequency} | Preference: {task.owner_preference}")
    print()
