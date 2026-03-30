from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


# --- Enumerations ---

class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    VET_VISIT = "vet_visit"
    OTHER = "other"


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


# --- Data Classes ---

@dataclass
class Task:
    title: str
    task_type: TaskType
    duration_minutes: int
    priority: Priority
    preferred_time: Optional[str] = None  # e.g. "08:00"
    is_recurring: bool = True
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Pet:
    name: str
    species: str
    age_years: int
    breed: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks_by_priority(self) -> list[Task]:
        pass


# --- Owner ---

class Owner:
    def __init__(self, name: str, email: str, available_minutes_per_day: int):
        self.name = name
        self.email = email
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass


# --- Schedule Output ---

@dataclass
class ScheduledTask:
    task: Task
    start_time: str   # e.g. "08:00"
    end_time: str     # e.g. "08:30"
    reason: str = ""


@dataclass
class DailySchedule:
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    unscheduled_tasks: list[Task] = field(default_factory=list)
    total_minutes_used: int = 0
    total_minutes_available: int = 0
    summary: str = ""

    def get_schedule_by_time(self) -> list[ScheduledTask]:
        pass

    def get_unscheduled_summary(self) -> str:
        pass


# --- Scheduler ---

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_schedule(self) -> DailySchedule:
        pass

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def _fits_in_schedule(self, task: Task, used_minutes: int) -> bool:
        pass

    def _assign_time_slot(self, task: Task, current_time: str) -> ScheduledTask:
        pass

    def _build_explanation(self, scheduled: list[ScheduledTask], unscheduled: list[Task]) -> str:
        pass
