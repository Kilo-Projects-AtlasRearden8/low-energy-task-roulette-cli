"""Completion history tracking and export."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class DoneRecord:
    task_id: str
    title: str
    completed_at: str
    energy: str = ""
    estimated_minutes: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


class HistoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[DoneRecord]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return [DoneRecord(**item) for item in data]

    def save(self, records: Iterable[DoneRecord]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump([record.to_dict() for record in records], handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    def add(self, task_id: str, title: str, energy: str, estimated_minutes: int) -> DoneRecord:
        records = self.load()
        record = DoneRecord(
            task_id=task_id,
            title=title,
            completed_at=datetime.now(timezone.utc).isoformat(),
            energy=energy,
            estimated_minutes=int(estimated_minutes),
        )
        records.append(record)
        self.save(records)
        return record

    def done_today_ids(self) -> set[str]:
        today = datetime.now(timezone.utc).date().isoformat()
        return {
            record.task_id
            for record in self.load()
            if record.completed_at.startswith(today)
        }

    def export_json(self, path: Path, records: list[DoneRecord]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump([record.to_dict() for record in records], handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    def export_csv(self, path: Path, records: list[DoneRecord]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["task_id", "title", "completed_at", "energy", "estimated_minutes"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for record in records:
                writer.writerow(record.to_dict())
