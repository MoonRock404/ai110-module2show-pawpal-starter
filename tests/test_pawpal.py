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
