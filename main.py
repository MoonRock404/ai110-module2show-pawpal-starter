from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---

owner = Owner(name="Alex", available_minutes_per_day=120)

# Pet 1: Milo the dog
milo = Pet(name="Milo", species="Dog", age_years=3, breed="Labrador")
milo.add_task(Task(description="Morning walk",        duration_minutes=30, priority=1, frequency="daily",       preferred_time="07:00"))
milo.add_task(Task(description="Breakfast feeding",   duration_minutes=10, priority=1, frequency="daily",       preferred_time="07:30"))
milo.add_task(Task(description="Flea medication",     duration_minutes=5,  priority=2, frequency="monthly",     preferred_time="08:00"))

# Pet 2: Luna the cat
luna = Pet(name="Luna", species="Cat", age_years=5, breed="Siamese")
luna.add_task(Task(description="Breakfast feeding",   duration_minutes=5,  priority=1, frequency="daily",       preferred_time="07:30"))
luna.add_task(Task(description="Brushing / grooming", duration_minutes=15, priority=3, frequency="twice weekly", preferred_time="09:00"))
luna.add_task(Task(description="Playtime enrichment", duration_minutes=20, priority=3, frequency="daily",       preferred_time="18:00"))

owner.add_pet(milo)
owner.add_pet(luna)

# --- Generate Schedule ---

scheduler = Scheduler(owner)
schedule = scheduler.generate_schedule()

# --- Print Today's Schedule ---

print("=" * 40)
print(f"  Today's Schedule — {owner.name}")
print(f"  Time budget: {owner.available_minutes_per_day} min/day")
print("=" * 40)

total = 0
for i, task in enumerate(schedule, start=1):
    pet_name = next(
        p.name for p in owner.pets if any(t.id == task.id for t in p.tasks)
    )
    time_label = task.preferred_time or "--:--"
    print(f"{i}. [{time_label}] {task.description} ({pet_name}) — {task.duration_minutes} min  |  priority {task.priority}")
    total += task.duration_minutes

print("-" * 40)
print(f"  Total scheduled: {total} min / {owner.available_minutes_per_day} min available")
print("=" * 40)
