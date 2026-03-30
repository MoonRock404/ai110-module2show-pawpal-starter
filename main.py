from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---

owner = Owner(name="Alex", available_minutes_per_day=120)

milo = Pet(name="Milo", species="Dog", age_years=3, breed="Labrador")
milo.add_task(Task(description="Morning walk",      duration_minutes=30, priority=1, frequency="daily",   preferred_time="07:00"))
milo.add_task(Task(description="Breakfast feeding", duration_minutes=10, priority=1, frequency="daily",   preferred_time="07:30"))
milo.add_task(Task(description="Evening walk",      duration_minutes=30, priority=2, frequency="daily",   preferred_time="18:30"))

luna = Pet(name="Luna", species="Cat", age_years=5, breed="Siamese")
luna.add_task(Task(description="Breakfast feeding",   duration_minutes=5,  priority=1, frequency="daily",        preferred_time="07:30"))
luna.add_task(Task(description="Brushing / grooming", duration_minutes=15, priority=3, frequency="twice weekly", preferred_time="09:00"))
luna.add_task(Task(description="Playtime enrichment", duration_minutes=20, priority=3, frequency="daily",        preferred_time="18:00"))

# --- Deliberate same-time conflicts ---
# Both tasks start at 07:00 — one per pet, guaranteed overlap
milo.add_task(Task(description="Vet weigh-in",  duration_minutes=15, priority=1, frequency="weekly", preferred_time="07:00"))
luna.add_task(Task(description="Nail trim",     duration_minutes=10, priority=2, frequency="weekly", preferred_time="07:00"))

owner.add_pet(milo)
owner.add_pet(luna)

scheduler = Scheduler(owner)

# --- Isolated conflict warning test ---
print("=" * 40)
print("  CONFLICT WARNING TEST")
print("=" * 40)

all_tasks = owner.get_all_tasks()
warnings = scheduler.conflict_warnings(all_tasks)

if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

# --- Full schedule (warnings auto-printed by generate_schedule) ---
print()
print("=" * 40)
print(f"  TODAY'S SCHEDULE — {owner.name}")
print(f"  Time budget: {owner.available_minutes_per_day} min/day")
print("=" * 40)

schedule = scheduler.generate_schedule()
time_ordered = scheduler.sort_by_time(schedule)

total = 0
for i, task in enumerate(time_ordered, start=1):
    pet_name = next(p.name for p in owner.pets if any(t.id == task.id for t in p.tasks))
    time_label = task.preferred_time or "--:--"
    print(f"{i}. [{time_label}] {task.description} ({pet_name}) — {task.duration_minutes} min  |  priority {task.priority}")
    total += task.duration_minutes

print("-" * 40)
print(f"  Total scheduled: {total} min / {owner.available_minutes_per_day} min available")
print("=" * 40)
