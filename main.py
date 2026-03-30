from pawpal_system import Task, Pet, Owner

owner = Owner("Alex")

pet1 = Pet(name="Buddy", gender="Male", age=3)
pet2 = Pet(name="Luna", gender="Female", age=5)

owner.add_pet(pet1)
owner.add_pet(pet2)

pet1.add_task(Task(task_activity="Evening Walk",  time_available="6:00 PM", priority=2, owner_preference="leash only",  frequency="daily"))
pet1.add_task(Task(task_activity="Feeding",       time_available="8:00 AM", priority=2, owner_preference="dry food",    frequency="twice daily"))
pet1.add_task(Task(task_activity="Morning Walk",  time_available="7:00 AM", priority=1, owner_preference="leash only",  frequency="daily"))
pet2.add_task(Task(task_activity="Grooming",      time_available="3:00 PM", priority=3, owner_preference="brush only",  frequency="weekly"))
pet2.add_task(Task(task_activity="Vet Check-in",  time_available="10:00 AM", priority=1, owner_preference="calm only", frequency="monthly"))

# Intentional conflicts: two tasks at the same time
pet1.add_task(Task(task_activity="Bath Time",     time_available="7:00 AM", priority=2, owner_preference="indoors",    frequency="weekly"))
pet2.add_task(Task(task_activity="Nail Trim",     time_available="3:00 PM", priority=2, owner_preference="calm only",  frequency="weekly"))

# Mark one task complete so filtering has something to show
pet1.tasks[0].mark_complete()


print("=== Recurring Task Demo ===\n")
morning_walk = pet1.tasks[2]  # Morning Walk (daily)
print(f"  Completing: {morning_walk.task_activity} | due {morning_walk.due_date}")
next_task = owner.scheduler.mark_task_complete(pet1, morning_walk)
if next_task:
    print(f"  Auto-scheduled next: {next_task.task_activity} | due {next_task.due_date}")
print()


print("=== Conflict Detection ===\n")
conflicts = owner.scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("  No conflicts found.")
print()


print(f"=== Sorted by Time for {owner.name} ===\n")
for pet, task in owner.scheduler.sort_by_time():
    status = "✓" if task.is_complete else "○"
    print(f"  {status} [{task.time_available}] {pet.name} — {task.task_activity}")
    print(f"       Priority: {task.priority} | Frequency: {task.frequency} | Preference: {task.owner_preference}")
    print()


print("=== Pending Tasks Only ===\n")
for pet, task in owner.scheduler.sort_by_time(owner.scheduler.filter_tasks(is_complete=False)):
    print(f"  ○ [{task.time_available}] {pet.name} — {task.task_activity}")
print()


print("=== Buddy's Tasks ===\n")
for pet, task in owner.scheduler.sort_by_time(owner.scheduler.filter_tasks(pet_name="Buddy")):
    status = "✓" if task.is_complete else "○"
    print(f"  {status} [{task.time_available}] {pet.name} — {task.task_activity}")
