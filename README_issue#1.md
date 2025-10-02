# Personal Task Manager

A lightweight CLI-based task manager. Tasks are persisted as JSON files and managed via Python classes.

## Storage & Data Model

Tasks are stored as a JSON array at `data/tasks.json` by default. Each task has this structure:

```json
{
  "id": "uuid4-string",
  "description": "string",
  "created_date": "ISO-8601 string",
  "is_completed": false
}
