from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TimePreference
import streamlit as st

if "owner" not in st.session_state:
    st.session_state["owner"] = None
if "pet" not in st.session_state:
    st.session_state["pet"] = None
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = None

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.scheduler is None:
        st.session_state.owner = Owner(name=owner_name, available_minutes=120)
        st.session_state.pet = Pet(name=pet_name, species=species)
        st.session_state.scheduler = Scheduler(
            owner=st.session_state.owner,
            pet=st.session_state.pet,
            tasks=[],
        )

    new_task = Task(
        name=task_title,
        category="general",
        duration_minutes=int(duration),
        priority=Priority[priority.upper()],
        time_preference=TimePreference.ANY,
    )
    st.session_state.scheduler.tasks.append(new_task)

current_tasks = st.session_state.scheduler.tasks if st.session_state.scheduler else []
priority_filter = st.selectbox(
    "Filter tasks by priority",
    ["all", "high", "medium", "low"],
    index=0,
)
filter_priority = None if priority_filter == "all" else Priority[priority_filter.upper()]
filtered_tasks = (
    st.session_state.scheduler.filter_tasks(priority=filter_priority)
    if st.session_state.scheduler
    else []
)

if current_tasks:
    st.write("Current tasks:")
    st.table([task.to_dict() for task in current_tasks])

    st.write("Filtered tasks:")
    if filtered_tasks:
        st.table([task.to_dict() for task in filtered_tasks])
    else:
        st.info("No tasks match the selected priority filter.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click the button to build a schedule from the current tasks.")

if st.button("Generate schedule"):
    if st.session_state.scheduler is None:
        st.session_state.owner = Owner(name=owner_name, available_minutes=120)
        st.session_state.pet = Pet(name=pet_name, species=species)
        st.session_state.scheduler = Scheduler(
            owner=st.session_state.owner,
            pet=st.session_state.pet,
            tasks=[],
        )

    plan = st.session_state.scheduler.generate_plan()
    warnings = st.session_state.scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            st.warning(
                f"⚠️ Scheduling conflict detected — {warning} "
                "Please move one task to another time of day or lower its priority."
            )
    else:
        st.success(f"No conflicts detected. Total scheduled duration: {plan.total_duration()} minutes.")

    sorted_scheduled = [
        task
        for task in st.session_state.scheduler.sort_by_time()
        if task in plan.scheduled
    ]
    if sorted_scheduled:
        st.subheader("Scheduled tasks")
        st.table([task.to_dict() for task in sorted_scheduled])

    if plan.skipped:
        st.warning("Skipped tasks:")
        st.table([task.to_dict() for task in plan.skipped])

    st.write(plan.summary())
