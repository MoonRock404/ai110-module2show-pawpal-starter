from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_task_status():
    """mark_complete() should flip the task's completed flag to True."""
    pet = Pet(name="Milo", species="Dog", age_years=3)
    task = Task(description="Morning walk", duration_minutes=30, priority=1, frequency="daily")
    pet.add_task(task)

    owner = Owner(name="Alex", available_minutes_per_day=120)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    assert task.completed is False
    scheduler.mark_complete(task.id)
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """add_task() should increase the pet's task list length by one."""
    pet = Pet(name="Luna", species="Cat", age_years=5)
    assert len(pet.tasks) == 0

    task = Task(description="Breakfast feeding", duration_minutes=5, priority=1, frequency="daily")
    pet.add_task(task)
    assert len(pet.tasks) == 1

    task2 = Task(description="Brushing", duration_minutes=15, priority=3, frequency="weekly")
    pet.add_task(task2)
    assert len(pet.tasks) == 2


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order tasks by preferred_time ascending,
    with tasks missing a preferred_time placed at the end."""
    pet = Pet(name="Milo", species="Dog", age_years=3)
    pet.add_task(Task(description="Evening walk",    duration_minutes=30, priority=2, frequency="daily", preferred_time="18:00"))
    pet.add_task(Task(description="Lunch treat",     duration_minutes=5,  priority=2, frequency="daily", preferred_time="12:00"))
    pet.add_task(Task(description="Morning walk",    duration_minutes=30, priority=1, frequency="daily", preferred_time="07:00"))
    pet.add_task(Task(description="No-time task",    duration_minutes=10, priority=1, frequency="daily", preferred_time=None))

    owner = Owner(name="Alex", available_minutes_per_day=120)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    times = [t.preferred_time or "99:99" for t in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got: {times}"
    assert sorted_tasks[-1].description == "No-time task"


def test_mark_complete_daily_task_creates_next_occurrence():
    """Marking a daily task complete should add a new task for the following day."""
    pet = Pet(name="Milo", species="Dog", age_years=3)
    task = Task(description="Morning walk", duration_minutes=30, priority=1, frequency="daily", preferred_time="07:00")
    pet.add_task(task)

    owner = Owner(name="Alex", available_minutes_per_day=120)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    assert len(pet.tasks) == 1
    scheduler.mark_complete(task.id)

    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert new_task.description == "Morning walk"
    assert new_task.completed is False
    assert tomorrow in new_task.preferred_time


def test_conflict_warnings_flags_same_time_tasks():
    """detect_conflicts() should flag two tasks scheduled at the exact same time."""
    pet = Pet(name="Milo", species="Dog", age_years=3)
    pet.add_task(Task(description="Morning walk", duration_minutes=30, priority=1, frequency="daily", preferred_time="07:00"))
    pet.add_task(Task(description="Vet check-in", duration_minutes=20, priority=1, frequency="weekly", preferred_time="07:00"))

    owner = Owner(name="Alex", available_minutes_per_day=120)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    warnings = scheduler.conflict_warnings(pet.tasks)
    assert len(warnings) >= 1
    assert any("Morning walk" in w and "Vet check-in" in w for w in warnings)
