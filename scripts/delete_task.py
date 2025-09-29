#!/usr/bin/env python3
"""
Delete a task by ID from tasks.json (or a custom JSON path).

Acceptance Criteria covered:
- Delete by ID
- Confirmation prompt (skippable with --yes)
- File updated after deletion
- Errors for invalid/missing IDs and missing/corrupt files
- Exit codes: 0 success, 1 not found/aborted, 2 invalid input/other errors
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Optional


def load_tasks(db_path: str) -> List[Dict]:
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}", file=sys.stderr)
        sys.exit(2)
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            print("Error: Database JSON must be a list of task objects.", file=sys.stderr)
            sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"Error: Could not read {db_path}: {e}", file=sys.stderr)
        sys.exit(2)


def save_tasks(db_path: str, tasks: List[Dict]) -> None:
    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Error: Could not write {db_path}: {e}", file=sys.stderr)
        sys.exit(2)


def get_task_by_id(tasks: List[Dict], task_id: int) -> Optional[Dict]:
    return next((t for t in tasks if t.get("id") == task_id), None)


def confirm(prompt: str) -> bool:
    try:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
    except EOFError:
        # Non-interactive context → default to "no"
        return False
    return ans in ("y", "yes")


def delete_by_id(db_path: str, task_id: int, assume_yes: bool) -> int:
    tasks = load_tasks(db_path)
    if not tasks:
        print("Error: No tasks to delete.", file=sys.stderr)
        return 1

    task = get_task_by_id(tasks, task_id)
    if not task:
        print(f"Error: No task found with ID {task_id}.", file=sys.stderr)
        return 1

    title = task.get("title", "(untitled)")
    if not assume_yes:
        if not confirm(f'Delete task #{task_id}: "{title}"?'):
            print("Aborted.")
            return 1

    # Remove task and save
    new_tasks = [t for t in tasks if t.get("id") != task_id]
    if len(new_tasks) == len(tasks):
        # Race condition or concurrent edit
        print(f"Error: Task #{task_id} could not be deleted (possibly already removed).", file=sys.stderr)
        return 1

    save_tasks(db_path, new_tasks)
    print(f"Deleted task #{task_id}.")
    return 0


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Delete a task by ID from the JSON task store.")
    p.add_argument("id", help="Task ID to delete (integer).")
    p.add_argument("-y", "--yes", action="store_true", help="Do not prompt for confirmation.")
    p.add_argument("--db", default="tasks.json", help="Path to tasks JSON file (default: tasks.json).")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        task_id = int(args.id)
    except ValueError:
        print("Error: Task ID must be an integer.", file=sys.stderr)
        return 2
    return delete_by_id(args.db, task_id, args.yes)


if __name__ == "__main__":
    raise SystemExit(main())
