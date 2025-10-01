from __future__ import annotations

import argparse

from pathlib import Path

from task_manager import TaskManager, TaskStorage

DEFAULT_DB = Path("data/tasks.json")

def build_manager(db_path: Path) -> TaskManager:

    storage = TaskStorage(db_path)

    return TaskManager(storage)

def main(argv=None) -> int:

    parser = argparse.ArgumentParser(description="Personal Task Manager")

    parser.add_argument(

        "--db",

        type=Path,

        default=DEFAULT_DB,

        help="Path to the tasks JSON file",

    )

    parser.add_argument(

        "--init",

        action="store_true",

        help="Initialize storage and exit",

    )

    # Subcommands

    subparsers = parser.add_subparsers(dest="command")

    # Issue #2: add task

    p_add = subparsers.add_parser("add", help="Add a new task")

    p_add.add_argument("description", nargs="+", help="Task description")

    # Issue #3: list all tasks

    p_list = subparsers.add_parser("list", help="List all tasks")

    p_list.add_argument(

        "--show-ids", action="store_true", help="Include task IDs in output"

    )

    p_list.add_argument(

        "--only-open", action="store_true", help="Show only incomplete tasks"

    )

    args = parser.parse_args(argv)

    tm = build_manager(args.db)

    if args.init:

        tm.storage.save(tm.list())

        print(f"Initialized storage at: {tm.storage.path}")

        return 0

    if args.command == "add":

        desc = " ".join(args.description).strip()

        t = tm.add(desc)

        print(f"Added task {t.id}: {t.description}")

        return 0

    elif args.command == "list":

        tasks = tm.list()

        if args.only_open:

            tasks = [t for t in tasks if not t.is_completed]

        if not tasks:

            print("No tasks found.")

            return 0

        for t in tasks:

            status = "✓" if t.is_completed else "•"

            if args.show_ids:

                print(f"{status} {t.created_date}  {t.id}  {t.description}")

            else:

                print(f"{status} {t.created_date}  {t.description}")

        return 0

    # default when no subcommand provided

    print(f"{len(tm.list())} tasks in {tm.storage.path}")

    return 0

if __name__ == "__main__":

    raise SystemExit(main())