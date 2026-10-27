"""Tests for selection logic."""

from __future__ import annotations

import random

from task_roulette.tasks import ENERGY_ORDER, Task, select_task


def make_task(task_id: str, energy: str = "low") -> Task:
    return Task(id=task_id, title=f"Task {task_id}", energy=energy)


def test_select_task_returns_none_for_empty_list() -> None:
    assert select_task([], energy="low") is None


def test_select_task_low_energy_only_returns_low_tasks() -> None:
    tasks = [make_task("a", "low"), make_task("b", "medium"), make_task("c", "high")]
    chosen = select_task(tasks, energy="low", rng=random.Random(1))
    assert chosen is not None
    assert chosen.energy == "low"


def test_select_task_medium_energy_includes_low_and_medium() -> None:
    tasks = [make_task("a", "low"), make_task("b", "medium"), make_task("c", "high")]
    seen = set()
    for seed in range(50):
        chosen = select_task(tasks, energy="medium", rng=random.Random(seed))
        assert chosen is not None
        seen.add(chosen.id)
    assert "c" not in seen
    assert "a" in seen
    assert "b" in seen


def test_select_task_high_energy_returns_any_task() -> None:
    tasks = [make_task("a", "low"), make_task("b", "medium"), make_task("c", "high")]
    seen = set()
    for seed in range(50):
        chosen = select_task(tasks, energy="high", rng=random.Random(seed))
        assert chosen is not None
        seen.add(chosen.id)
    assert seen == {"a", "b", "c"}


def test_select_task_excludes_ids() -> None:
    tasks = [make_task("a", "low"), make_task("b", "low")]
    chosen = select_task(tasks, energy="low", rng=random.Random(1), exclude_ids={"a", "b"})
    assert chosen is None
    chosen = select_task(tasks, energy="low", rng=random.Random(1), exclude_ids={"a"})
    assert chosen is not None
    assert chosen.id == "b"


def test_select_task_deterministic_with_seed() -> None:
    tasks = [make_task("a", "low"), make_task("b", "low"), make_task("c", "low")]
    first = [select_task(tasks, energy="low", rng=random.Random(42)) for _ in range(10)]
    second = [select_task(tasks, energy="low", rng=random.Random(42)) for _ in range(10)]
    assert first == second
