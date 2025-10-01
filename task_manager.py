# task_manager.py — Issue #4 version (adds TaskManager.complete)

from __future__ import annotations

import datetime as _dt
import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class Task:
    id: str
    description: str
    created_date: str
    is_completed: bool = False


class TaskStorage:
    """
    JSON-backed storage with atomic writes and basic corruption recovery.
    """

    def __init__(self, path: Path | str):
        self.path = Path(path)

    def _ensure_file(self) -> None:
        try:
            if not self.path.exists():
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self._atomic_write([])
        except OSError as e:
            raise IOError(f"Failed to initialize storage: {e}") from e

    def _atomic_write(self, data) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(self.path)

    def load(self) -> List[Task]:
        self._ensure_file()
        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            return [Task(**item) for item in raw]
        except json.JSONDecodeError:
            # Backup the corrupted file and start fresh.
            backup = self.path.with_suffix(self.path.suffix + ".bak")
            try:
                self.path.replace(backup)
            finally:
                self._atomic_write([])
            return []
        except OSError as e:
            raise IOError(f"Failed to load tasks: {e}") from e

    def save(self, tasks: List[Task]) -> None:
        try:
            data = [asdict(t) for t in tasks]
            self._atomic_write(data)
        except OSError as e:
            raise IOError(f"Failed to save tasks: {e}") from e


class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks: List[Task] = self.storage.load()

    # Basic operations
    def add(self, description: str) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            description=description,
            created_date=_dt.datetime.now().isoformat(timespec="seconds"),
            is_completed=False,
        )
        self.tasks.append(task)
        self.storage.save(self.tasks)
        return task

    def list(self) -> List[Task]:
        return list(self.tasks)

    def get(self, task_id: str) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as completed. Returns the updated task, or None if not found.
        """
        t = self.get(task_id)
        if t is None:
            return None
        if not t.is_completed:
            t.is_completed = True
            self.storage.save(self.tasks)
        return t

