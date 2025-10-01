import json
from pathlib import Path
import pytest

from task_manager import TaskManager, TaskStorage


@pytest.fixture()
def tmpdb(tmp_path: Path) -> Path:
    """Provide a temporary JSON database path for testing."""
    return tmp_path / "tasks.json"


def test_round_trip_add_and_load(tmpdb: Path):
    tm = TaskManager(TaskStorage(tmpdb))
    assert len(tm.list()) == 0

    t = tm.add("write tests")
    assert t.description == "write tests"

    # New manager loads previously saved task
    tm2 = TaskManager(TaskStorage(tmpdb))
    tasks = tm2.list()
    assert len(tasks) == 1
    assert tasks[0].id == t.id
    assert tasks[0].description == "write tests"
    assert tasks[0].is_completed is False


def test_corrupted_json_is_backed_up_and_reset(tmpdb: Path):
    storage = TaskStorage(tmpdb)

    # Manually write corrupted content
    tmpdb.parent.mkdir(parents=True, exist_ok=True)
    tmpdb.write_text("{not-json", encoding="utf-8")

    # Loading should back up and reset to empty
    tasks = storage.load()
    assert tasks == []

    # A .bak should exist
    backup = tmpdb.with_suffix(tmpdb.suffix + ".bak")
    assert backup.exists()

    # After saving, the main file is valid JSON list
    storage.save([])
    data = json.loads(tmpdb.read_text(encoding="utf-8"))
    assert isinstance(data, list)
