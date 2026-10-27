"""Command-line interface for task-roulette."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from .defaults import DEFAULT_TASKS, default_data_dir
from .tasks import Task, load_tasks, select_task
from .tracking import DoneRecord, HistoryStore

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"


def data_dir_from_args(args: argparse.Namespace) -> Path:
    if getattr(args, "data_dir", None):
        return Path(args.data_dir)
    return default_data_dir()


def ensure_tasks(data_dir: Path) -> None:
    tasks_path = data_dir / TASKS_FILE
    if not tasks_path.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        tasks_path.write_text(
            json.dumps(DEFAULT_TASKS, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-roulette",
        description="Pick one small task for low-energy or ADHD days from a local JSON list.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pick = sub.add_parser("pick", help="Pick one task")
    pick.add_argument("--energy", choices=["low", "medium", "high"], default="low")
    pick.add_argument("--seed", type=int, default=None)
    pick.add_argument("--exclude-done", action="store_true")
    pick.add_argument("--mark-done", action="store_true")
    pick.add_argument("--data-dir", default=None)

    list_cmd = sub.add_parser("list", help="List tasks")
    list_cmd.add_argument("--energy", choices=["low", "medium", "high"], default=None)
    list_cmd.add_argument("--data-dir", default=None)

    done_cmd = sub.add_parser("done", help="Mark a task as done")
    done_cmd.add_argument("task_id")
    done_cmd.add_argument("--data-dir", default=None)

    history_cmd = sub.add_parser("history", help="Show completion history")
    history_cmd.add_argument("--limit", type=int, default=20)
    history_cmd.add_argument("--data-dir", default=None)

    export_cmd = sub.add_parser("export", help="Export history to JSON or CSV")
    export_cmd.add_argument("path")
    export_cmd.add_argument("--data-dir", default=None)

    init_cmd = sub.add_parser("init", help="Create data folder with a sample tasks.json")
    init_cmd.add_argument("--data-dir", default=None)

    return parser


def cmd_pick(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    tasks_path = data_dir / TASKS_FILE
    if not tasks_path.exists():
        print(f"No tasks file at {tasks_path}. Run: task-roulette init")
        return 1
    tasks = load_tasks(tasks_path)

    history = HistoryStore(data_dir / HISTORY_FILE)
    exclude_ids: set[str] | None = None
    if args.exclude_done:
        exclude_ids = history.done_today_ids()

    rng = random.Random(args.seed) if args.seed is not None else None
    chosen = select_task(tasks, energy=args.energy, rng=rng, exclude_ids=exclude_ids)
    if chosen is None:
        print("No eligible tasks for that energy level. Rest is a valid choice too.")
        return 0

    print(f"{chosen.title}")
    print(f"  id: {chosen.id}")
    print(f"  energy: {chosen.energy}  ~{chosen.estimated_minutes} min")
    if chosen.description:
        print(f"  {chosen.description}")
    if chosen.tags:
        print(f"  tags: {', '.join(chosen.tags)}")

    if args.mark_done:
        history.add(chosen.id, chosen.title, chosen.energy, chosen.estimated_minutes)
        print("Marked done.")

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    tasks_path = data_dir / TASKS_FILE
    if not tasks_path.exists():
        print(f"No tasks file at {tasks_path}. Run: task-roulette init")
        return 1
    tasks = load_tasks(tasks_path)
    if args.energy is not None:
        order = {"low": 0, "medium": 1, "high": 2}
        level = order[args.energy]
        tasks = [t for t in tasks if order.get(t.energy, 0) <= level]
    if not tasks:
        print("No tasks.")
        return 0
    for task in tasks:
        print(f"{task.id}  [{task.energy}, ~{task.estimated_minutes}min]  {task.title}")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    tasks_path = data_dir / TASKS_FILE
    if not tasks_path.exists():
        print(f"No tasks file at {tasks_path}. Run: task-roulette init")
        return 1
    tasks = load_tasks(tasks_path)
    task = next((t for t in tasks if t.id == args.task_id), None)
    if task is None:
        print(f"No task with id: {args.task_id}")
        return 1
    history = HistoryStore(data_dir / HISTORY_FILE)
    history.add(task.id, task.title, task.energy, task.estimated_minutes)
    print(f"Marked done: {task.title}")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    history = HistoryStore(data_dir / HISTORY_FILE)
    records = history.load()
    if not records:
        print("No history yet.")
        return 0
    for record in records[-args.limit :][::-1]:
        print(f"{record.completed_at}  {record.task_id}  {record.title}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    history = HistoryStore(data_dir / HISTORY_FILE)
    records = history.load()
    out_path = Path(args.path)
    if out_path.suffix.lower() == ".csv":
        history.export_csv(out_path, records)
    else:
        history.export_json(out_path, records)
    print(f"Exported {len(records)} record(s) to {out_path}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    data_dir = data_dir_from_args(args)
    data_dir.mkdir(parents=True, exist_ok=True)
    tasks_path = data_dir / TASKS_FILE
    if not tasks_path.exists():
        tasks_path.write_text(
            json.dumps(DEFAULT_TASKS, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(f"Data directory: {data_dir}")
    print(f"Tasks file: {tasks_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    commands = {
        "pick": cmd_pick,
        "list": cmd_list,
        "done": cmd_done,
        "history": cmd_history,
        "export": cmd_export,
        "init": cmd_init,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
