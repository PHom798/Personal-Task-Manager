*** a/README.md
--- b/README.md
@@
+# Personal Task Manager
+
+## Storage & Data Model
+
+Tasks are stored as a JSON array at `data/tasks.json` by default. Each task has:
+
+```json
+{
+  "id": "uuid4-string",
+  "description": "string",
+  "created_date": "ISO-8601 string",
+  "is_completed": false
+}
+```
+
+Writes are **atomic** (temp file + replace). If the JSON becomes corrupted, the file is backed up to `tasks.json.bak` and a fresh empty file is created.
+
+## Quickstart
+
+```bash
+python3 -m venv .venv && source .venv/bin/activate
+pip install -r requirements-dev.txt
+
+python3 main.py --init      # create data/tasks.json
+python3 main.py             # prints number of tasks
+```
+
+## Running Tests
+
+```bash
+pytest -q
+```
