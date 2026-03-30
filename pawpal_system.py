from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from typing import Optional
import uuid


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    duration_minutes: int
    priority: int           # 1 = highest, 4 = lowest
    frequency: str          # e.g. "daily", "twice daily", "weekly"
    preferred_time: Optional[str] = None  # e.g. "08:00"
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Pet:
    """Stores pet details and owns a list of tasks."""
    name: str
    species: str
    age_years: int
    breed: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_by_priority(self) -> list[Task]:
        return sorted(self.tasks, key=lambda t: t.priority)


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, available_minutes_per_day: int):
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list[Task]:
        """Returns every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain — retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[Task]:
        """Returns an ordered list of tasks that fit within the owner's time budget.
        Prints any scheduling conflicts as warnings without interrupting the schedule."""
        sorted_tasks = self._sort_by_priority(self.owner.get_all_tasks())
        scheduled, skipped = [], []
        used = 0
        for task in sorted_tasks:
            if self._fits_in_budget(task, used):
                scheduled.append(task)
                used += task.duration_minutes
            else:
                skipped.append(task)
        self._build_explanation(scheduled, skipped)
        for warning in self.conflict_warnings(scheduled):
            print(warning)
        return scheduled

    def conflict_warnings(self, tasks: list[Task]) -> list[str]:
        """Returns human-readable warning strings for any overlapping tasks.
        Never raises — returns an empty list if detection fails or finds nothing."""
        try:
            conflicts = self.detect_conflicts(tasks)
        except Exception:
            return ["WARNING: conflict detection encountered an unexpected error."]
        warnings = []
        for a, b, pet_a, pet_b in conflicts:
            who_a = f"{a.description} ({pet_a}, {a.preferred_time})"
            who_b = f"{b.description} ({pet_b}, {b.preferred_time})"
            warnings.append(f"WARNING: '{who_a}' overlaps with '{who_b}'")
        return warnings

    def mark_complete(self, task_id: str) -> None:
        """Marks a task as completed by id.
        For 'daily' and 'weekly' tasks, schedules a new instance for the next occurrence."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    task.completed = True
                    next_time = self._next_occurrence_time(task)
                    if next_time is not None:
                        pet.add_task(Task(
                            description=task.description,
                            duration_minutes=task.duration_minutes,
                            priority=task.priority,
                            frequency=task.frequency,
                            preferred_time=next_time,
                        ))
                    return

    def _next_occurrence_time(self, task: Task) -> Optional[str]:
        """Returns the preferred_time string for the next occurrence, or None for one-off tasks."""
        if task.frequency == "daily":
            next_date = date.today() + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = date.today() + timedelta(weeks=1)
        elif task.frequency == "twice daily":
            next_date = date.today()
        else:
            return None  # monthly, one-off, etc. — no auto-recurrence
        prefix = next_date.strftime("%Y-%m-%d")
        time_part = task.preferred_time or "08:00"
        return f"{prefix} {time_part}"

    def get_pending_tasks(self) -> list[Task]:
        """Returns all incomplete tasks across all pets, sorted by priority."""
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        return self._sort_by_priority(pending)

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: (t.priority, t.preferred_time or "99:99"))

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sorts tasks chronologically by preferred_time.
        Tasks without a preferred_time are placed at the end."""
        return sorted(tasks, key=lambda t: t.preferred_time or "99:99")

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task, str, str]]:
        """Returns a list of (task_a, task_b, pet_a, pet_b) tuples where the two tasks
        have overlapping time windows. Tasks without a preferred_time are skipped."""
        pet_of = {
            task.id: pet.name
            for pet in self.owner.pets
            for task in pet.tasks
        }
        timed = [t for t in tasks if t.preferred_time and self._task_start_minutes(t) is not None]
        starts = {t.id: self._task_start_minutes(t) for t in timed}
        conflicts = []
        for a, b in combinations(timed, 2):
            start_a, start_b = starts[a.id], starts[b.id]
            if start_a < start_b + b.duration_minutes and start_b < start_a + a.duration_minutes:
                conflicts.append((a, b, pet_of.get(a.id, "?"), pet_of.get(b.id, "?")))
        return conflicts

    def _task_start_minutes(self, task: Task) -> Optional[int]:
        """Parses preferred_time ('HH:MM' or 'YYYY-MM-DD HH:MM') into minutes since midnight."""
        if not task.preferred_time:
            return None
        time_part = task.preferred_time.split(" ")[-1]  # handles both formats
        try:
            h, m = time_part.split(":")
            return int(h) * 60 + int(m)
        except ValueError:
            return None

    def _fits_in_budget(self, task: Task, used_minutes: int) -> bool:
        return used_minutes + task.duration_minutes <= self.owner.available_minutes_per_day

    def _build_explanation(self, scheduled: list[Task], skipped: list[Task]) -> str:
        lines = [f"  - {t.description} ({t.duration_minutes} min)" for t in scheduled]
        skip_lines = [f"  - {t.description} (skipped: not enough time)" for t in skipped]
        return "\n".join(lines + skip_lines)
