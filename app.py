import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Initialize Owner in session state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

# ----------------------------------------
# SECTION 1: Add a Pet
# ----------------------------------------
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    pet_gender = st.selectbox("Gender", ["Male", "Female"])
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=2)
    submitted = st.form_submit_button("Add Pet")

if submitted:
    new_pet = Pet(name=pet_name, gender=pet_gender, age=int(pet_age))
    owner.add_pet(new_pet)
    st.success(f"{pet_name} added!")

if owner.pets:
    st.write("Your pets:")
    for pet in owner.pets:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{pet.name} ({pet.gender}, age {pet.age})")
        with col2:
            if st.button("Edit", key=f"edit_pet_{pet.name}"):
                st.session_state.editing_pet = pet.name
        with col3:
            if st.button("Delete", key=f"delete_pet_{pet.name}"):
                owner.remove_pet(pet)
                st.rerun()

    # Edit pet form
    if "editing_pet" in st.session_state:
        pet_to_edit = next((p for p in owner.pets if p.name == st.session_state.editing_pet), None)
        if pet_to_edit:
            st.write(f"Editing: {pet_to_edit.name}")
            with st.form("edit_pet_form"):
                new_name = st.text_input("Name", value=pet_to_edit.name)
                new_gender = st.selectbox("Gender", ["Male", "Female"], index=0 if pet_to_edit.gender == "Male" else 1)
                new_age = st.number_input("Age", min_value=0, max_value=30, value=pet_to_edit.age)
                save_pet = st.form_submit_button("Save changes")
                cancel_pet = st.form_submit_button("Cancel")
            if save_pet:
                updated_pet = Pet(name=new_name, gender=new_gender, age=int(new_age))
                updated_pet.tasks = pet_to_edit.tasks
                owner.edit_pet(pet_to_edit, updated_pet)
                del st.session_state.editing_pet
                st.rerun()
            if cancel_pet:
                del st.session_state.editing_pet
                st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ----------------------------------------
# SECTION 2: Schedule a Task
# ----------------------------------------
st.subheader("Schedule a Task")

if not owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.name for p in owner.pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Select pet", pet_names)
        task_activity = st.text_input("Task activity", value="Morning walk")
        time_available = st.text_input("Time available", value="8:00 AM")
        task_date = st.date_input("Date", value=date.today())
        priority = st.number_input("Priority (1 = highest)", min_value=1, max_value=5, value=1)
        owner_preference = st.text_input("Owner preference", value="leash only")
        frequency = st.text_input("Frequency", value="daily")
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        new_task = Task(
            task_activity=task_activity,
            time_available=time_available,
            priority=int(priority),
            owner_preference=owner_preference,
            frequency=frequency,
            due_date=task_date,
        )
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_activity}' added to {selected_pet_name}!")

st.divider()

# ----------------------------------------
# SECTION 3: Today's Schedule
# ----------------------------------------
st.subheader("Today's Schedule")

# Edit task form — shown at the top of this section when active
if "editing_task" in st.session_state:
    epet_name, etask_activity, etime = st.session_state.editing_task
    epet = next((p for p in owner.pets if p.name == epet_name), None)
    etask = next((t for t in epet.tasks if t.task_activity == etask_activity and t.time_available == etime), None) if epet else None
    if epet and etask:
        st.info(f"Editing: {etask.task_activity} for {epet.name}")
        with st.form("edit_task_form"):
            new_activity = st.text_input("Task activity", value=etask.task_activity)
            new_time = st.text_input("Time available", value=etask.time_available)
            new_priority = st.number_input("Priority", min_value=1, max_value=5, value=etask.priority)
            new_preference = st.text_input("Owner preference", value=etask.owner_preference)
            new_frequency = st.text_input("Frequency", value=etask.frequency)
            col1, col2 = st.columns([1, 1])
            with col1:
                save_task = st.form_submit_button("Save changes")
            with col2:
                cancel_task = st.form_submit_button("Cancel")
        if save_task:
            updated_task = Task(
                task_activity=new_activity,
                time_available=new_time,
                priority=int(new_priority),
                owner_preference=new_preference,
                frequency=new_frequency,
                due_date=etask.due_date,
            )
            epet.edit_task(etask, updated_task)
            del st.session_state.editing_task
            st.session_state.task_saved = new_activity
            st.rerun()
        if cancel_task:
            del st.session_state.editing_task
            st.rerun()
    st.divider()

if "task_saved" in st.session_state:
    st.success(f"'{st.session_state.task_saved}' updated successfully.")
    del st.session_state.task_saved

show_completed = st.checkbox("Show completed tasks")

if st.button("Generate Schedule"):
    st.session_state.show_schedule = True

if st.session_state.get("show_schedule"):
    tasks = owner.scheduler.filter_tasks(is_complete=None if show_completed else False)
    tasks = [(pet, task) for pet, task in tasks if task.due_date <= date.today()]
    sorted_tasks = owner.scheduler.sort_by_time(tasks)

    conflicts = owner.scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)

    if sorted_tasks:
        for i, (pet, task) in enumerate(sorted_tasks):
            status = "✓" if task.is_complete else "○"
            st.markdown(f"**{status} [{task.time_available}] {pet.name} — {task.task_activity}**")
            st.caption(f"Priority: {task.priority} | Frequency: {task.frequency} | Preference: {task.owner_preference}")

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if not task.is_complete:
                    if st.button("Mark complete", key=f"complete_{i}_{pet.name}_{task.task_activity}"):
                        next_task = owner.scheduler.mark_task_complete(pet, task)
                        if next_task:
                            st.success(f"Done! Next '{task.task_activity}' scheduled for {next_task.due_date}.")
                        else:
                            st.success(f"'{task.task_activity}' marked complete.")
                        st.rerun()
            with col2:
                if st.button("Edit", key=f"edit_task_{i}_{pet.name}_{task.task_activity}"):
                    st.session_state.editing_task = (pet.name, task.task_activity, task.time_available)
                    st.rerun()
            with col3:
                if st.button("Delete", key=f"delete_{i}_{pet.name}_{task.task_activity}"):
                    pet.remove_task(task)
                    st.rerun()

    else:
        st.info("No tasks scheduled yet.")
