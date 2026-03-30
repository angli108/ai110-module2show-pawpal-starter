import streamlit as st
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
    owner.add_pet(new_pet)  # calls Owner.add_pet()
    st.success(f"{pet_name} added!")

if owner.pets:
    st.write("Your pets:")
    st.table([{"name": p.name, "gender": p.gender, "age": p.age, "tasks": len(p.tasks)} for p in owner.pets])
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
        )
        selected_pet.add_task(new_task)  # calls Pet.add_task()
        st.success(f"Task '{task_activity}' added to {selected_pet_name}!")

st.divider()

# ----------------------------------------
# SECTION 3: Today's Schedule
# ----------------------------------------
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    all_tasks = owner.scheduler.get_tasks_by_priority()  # calls Scheduler.get_tasks_by_priority()
    if all_tasks:
        for pet, task in all_tasks:
            status = "✓" if task.is_complete else "○"
            st.markdown(f"**{status} [{task.time_available}] {pet.name} — {task.task_activity}**")
            st.caption(f"Priority: {task.priority} | Frequency: {task.frequency} | Preference: {task.owner_preference}")
    else:
        st.info("No tasks scheduled yet.")
