import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet Setup")

col_owner, col_pet = st.columns(2)
with col_owner:
    owner_name = st.text_input("Owner name", value="Jordan")
    time_available = st.number_input(
        "Available time (minutes)", min_value=10, max_value=480, value=60
    )
with col_pet:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)

# Build Owner and Pet objects in session state
if "owner" not in st.session_state:
    st.session_state.owner = None
    st.session_state.pet = None

owner = Owner(owner_name, time_available)
pet = Pet(pet_name, species, pet_age)
owner.add_pet(pet)

# Restore previously added tasks onto the new pet
if "tasks" not in st.session_state:
    st.session_state.tasks = []

for t in st.session_state.tasks:
    pet.add_task(Task(t["title"], t["duration_minutes"], t["priority"]))

st.session_state.owner = owner
st.session_state.pet = pet

st.divider()
st.markdown("### Tasks")
st.caption("Add tasks for your pet. These feed directly into the scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    new_task = Task(task_title, int(duration), priority)
    pet.add_task(new_task)
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a priority-based schedule that fits within your available time.")

if st.button("Generate schedule"):
    if not pet.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        scheduler.generate_plan()

        if scheduler.plan:
            st.success(
                f"Schedule ready! {len(scheduler.plan)} task(s), "
                f"{scheduler.get_total_planned_time()}/{scheduler.available_time} min used."
            )
            st.text(scheduler.explain_plan())

            st.markdown("#### Pet Info")
            st.json(pet.get_info())
        else:
            st.warning("No tasks could fit within the available time.")
