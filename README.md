# Personal Task Manager

A simple **command-line** task management application built with Python. You can add, list, complete, and delete tasks from your terminal.

---

## ✨ Features

- Add new tasks
- List all tasks (with optional status filters)
- Mark tasks as complete
- Delete tasks
- Simple JSON file storage (no external DB)
- Zero external runtime dependencies

---

## 🧰 Requirements

- **Python**: 3.9+ (tested with 3.10/3.11)
- **OS**: Linux, macOS, or Windows

> No third-party packages are required to run the app. (A `requirements-dev.txt` may exist for development tasks like testing/formatting.)

---

## 🔧 Installation (2 minutes)

```bash
# 1) Clone your fork
git clone https://github.com/<your-username>/Personal-Task-Manager.git
cd Personal-Task-Manager

# 2) (Optional but recommended) Create a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Run the CLI help
python main.py --help
