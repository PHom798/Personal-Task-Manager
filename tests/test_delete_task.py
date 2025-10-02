import json
import os
import sys
from pathlib import Path

# Import functions directly for unit tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.delete_task import delete_by_id, load_tasks, save_tasks  # noqa: E402


def write_tasks(path, tasks):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def test_delete_success(tmp_path):
    db = tmp_path / "tasks.json"
    write_tasks(db, [{"id": 1, "title": "keep"}, {"id": 2, "title": "remove"}])

    code = delete_by_id(str(db), 2, assume_yes=True)
    assert code == 0
    remaining = json.loads(db.read_text())
    assert remaining == [{"id": 1, "title": "keep"}]


def test_delete_not_found(tmp_path):
    db = tmp_path / "tasks.json"
    write_tasks(db, [{"id": 1, "title": "one"}])
    code = delete_by_id(str(db), 999, assume_yes=True)
    assert code == 1


def test_delete_empty_list(tmp_path):
    db = tmp_path / "tasks.json"
    write_tasks(db, [])
    code = delete_by_id(str(db), 1, assume_yes=True)
    assert code == 1


def test_missing_db(tmp_path, capsys):
    db = tmp_path / "missing.json"
    # load_tasks is exercised through delete_by_id (which should exit with 2),
    # but since delete_by_id calls sys.exit only in load/save helpers,
    # we assert via a subprocess-like behavior by catching SystemExit.
    try:
        delete_by_id(str(db), 1, assume_yes=True)
    except SystemExit as e:
        assert e.code == 2
    else:
        # If no SystemExit was raised, capture stderr for debugging
        out = capsys.readouterr()
        assert False, f"Expected SystemExit(2); got stdout={out.out!r}, stderr={out.err!r}"
