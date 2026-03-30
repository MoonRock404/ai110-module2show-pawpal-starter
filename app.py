import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session State Initialization ---

if "owner" not in st.session_state:
    st.session_state.owner = None

if "pet" not in st.session_state:
    st.session_state.pet = None

# --- Owner + Pet Setup ---

st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes per day", min_value=10, max_value=480, value=120)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=2)

if st.button("Save Owner & Pet"):
    owner = Owner(name=owner_name, available_minutes_per_day=int(available_minutes))
    pet = Pet(name=pet_name, species=species, age_years=int(age))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.success(f"Saved! {owner_name} with pet {pet_name}.")

st.divider()

# --- Add Tasks ---

st.subheader("Add Tasks")

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["high", "medium", "low"])
with col4:
    preferred_time = st.text_input("Preferred time", value="08:00")

if st.button("Add Task"):
    if st.session_state.pet is None:
        st.warning("Save an owner and pet first.")
    else:
        task = Task(
            description=task_title,
            duration_minutes=int(duration),
            priority=PRIORITY_MAP[priority_label],
            frequency="daily",
            preferred_time=preferred_time or None,
        )
        st.session_state.pet.add_task(task)
        st.success(f"Added: {task_title}")

# Display current tasks
if st.session_state.pet and st.session_state.pet.tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Description": t.description,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Preferred Time": t.preferred_time or "--",
            "Done": t.completed,
        }
        for t in st.session_state.pet.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---

st.subheader("Generate Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.warning("Save an owner and pet first.")
    elif not st.session_state.pet.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.generate_schedule()

        st.success(f"Scheduled {len(schedule)} task(s) for {st.session_state.pet.name}:")
        total = 0
        for i, task in enumerate(schedule, start=1):
            time_label = task.preferred_time or "--:--"
            st.markdown(f"**{i}. [{time_label}] {task.description}** — {task.duration_minutes} min | priority {task.priority}")
            total += task.duration_minutes

        skipped = [t for t in st.session_state.pet.tasks if t not in schedule]
        if skipped:
            st.warning("Skipped (not enough time):")
            for t in skipped:
                st.markdown(f"- {t.description} ({t.duration_minutes} min)")

        st.info(f"Total: {total} / {st.session_state.owner.available_minutes_per_day} min used")
