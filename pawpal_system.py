from dataclasses import dataclass, field
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
        """Returns an ordered list of tasks that fit within the owner's time budget."""
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
        return scheduled

    def mark_complete(self, task_id: str) -> None:
        """Marks a task as completed by id."""
        for task in self.owner.get_all_tasks():
            if task.id == task_id:
                task.completed = True
                return

    def get_pending_tasks(self) -> list[Task]:
        """Returns all incomplete tasks across all pets, sorted by priority."""
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        return self._sort_by_priority(pending)

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: (t.priority, t.preferred_time or "99:99"))

    def _fits_in_budget(self, task: Task, used_minutes: int) -> bool:
        return used_minutes + task.duration_minutes <= self.owner.available_minutes_per_day

    def _build_explanation(self, scheduled: list[Task], skipped: list[Task]) -> str:
        lines = [f"  - {t.description} ({t.duration_minutes} min)" for t in scheduled]
        skip_lines = [f"  - {t.description} (skipped: not enough time)" for t in skipped]
        return "\n".join(lines + skip_lines)
