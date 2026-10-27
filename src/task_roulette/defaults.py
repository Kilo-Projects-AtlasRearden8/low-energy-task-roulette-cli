"""Default data directory and sample tasks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

DEFAULT_TASKS: list[dict] = [
    {
        "id": "drink-water",
        "title": "Drink a glass of water",
        "description": "A small glass counts. Hydration is a win.",
        "category": "body",
        "energy": "low",
        "estimated_minutes": 2,
        "tags": ["hydration"],
    },
    {
        "id": "open-curtains",
        "title": "Open the curtains or blinds",
        "description": "Let some natural light into the room.",
        "category": "body",
        "energy": "low",
        "estimated_minutes": 1,
        "tags": ["light", "environment"],
    },
    {
        "id": "deep-breaths",
        "title": "Take five deep breaths",
        "description": "Inhale slowly, exhale slowly. That is all.",
        "category": "mind",
        "energy": "low",
        "estimated_minutes": 1,
        "tags": ["calm", "breathing"],
    },
    {
        "id": "stretch",
        "title": "Stretch for two minutes",
        "description": "Reach up, touch your toes, roll your shoulders.",
        "category": "body",
        "energy": "low",
        "estimated_minutes": 2,
        "tags": ["movement"],
    },
    {
        "id": "write-sentence",
        "title": "Write one sentence",
        "description": "Anything at all. A journal line, a note, a text.",
        "category": "mind",
        "energy": "low",
        "estimated_minutes": 3,
        "tags": ["writing"],
    },
    {
        "id": "read-page",
        "title": "Read one page",
        "description": "One page of anything. You do not have to finish the book.",
        "category": "mind",
        "energy": "low",
        "estimated_minutes": 5,
        "tags": ["reading"],
    },
    {
        "id": "step-outside",
        "title": "Step outside for fresh air",
        "description": "Open a door or window and breathe for a minute.",
        "category": "body",
        "energy": "low",
        "estimated_minutes": 3,
        "tags": ["outdoors"],
    },
    {
        "id": "tidy-one-surface",
        "title": "Tidy one small surface",
        "description": "One shelf, one corner of a desk, one nightstand.",
        "category": "home",
        "energy": "medium",
        "estimated_minutes": 10,
        "tags": ["cleaning"],
    },
    {
        "id": "delete-emails",
        "title": "Delete five old emails",
        "description": "Just five. Inbox zero is not the goal.",
        "category": "work",
        "energy": "medium",
        "estimated_minutes": 5,
        "tags": ["digital"],
    },
    {
        "id": "water-plant",
        "title": "Water one plant",
        "description": "One plant only. Or check the soil and skip it.",
        "category": "home",
        "energy": "low",
        "estimated_minutes": 3,
        "tags": ["plants"],
    },
    {
        "id": "text-someone",
        "title": "Send one 'thinking of you' text",
        "description": "One person, a few words. Connection in small doses.",
        "category": "connection",
        "energy": "medium",
        "estimated_minutes": 3,
        "tags": ["relationships"],
    },
    {
        "id": "set-timer",
        "title": "Set a ten-minute timer and tidy anything",
        "description": "Stop when the timer rings. Anything you did is enough.",
        "category": "home",
        "energy": "medium",
        "estimated_minutes": 10,
        "tags": ["cleaning", "timer"],
    },
]


def default_data_dir() -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "task-roulette"
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", home)) / "task-roulette"
    return home / ".local" / "share" / "task-roulette"
