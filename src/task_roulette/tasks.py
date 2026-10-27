"""Task loading and selection logic."""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

ENERGY_ORDER = {"low": 0, "medium": 1, "high": 2}


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    category: str = "general"
    energy: str = "low"
    estimated_minutes: int = 15
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=str(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            category=str(data.get("category", "general")),
            energy=str(data.get("energy", "low")),
            estimated_minutes=int(data.get("estimated_minutes", 15)),
            tags=list(data.get("tags", [])),
        )


def load_tasks(path: Path) -> list[Task]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        data = data.get("tasks", [])
    tasks: list[Task] = []
    for item in data:
        tasks.append(Task.from_dict(item))
    return tasks


def save_tasks(path: Path, tasks: Iterable[Task]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump([task.to_dict() for task in tasks], handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def select_task(
    tasks: list[Task],
    energy: str = "low",
    rng: random.Random | None = None,
    exclude_ids: set[str] | None = None,
) -> Task | None:
    """Return one task eligible for the given energy level, or None."""
    if rng is None:
        rng = random
    level = ENERGY_ORDER.get(energy, 0)
    eligible = [
        task
        for task in tasks
        if ENERGY_ORDER.get(task.energy, 0) <= level
        and (exclude_ids is None or task.id not in exclude_ids)
    ]
    if not eligible:
        return None
    return rng.choice(eligible)
