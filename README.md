# Personal Task Manager

A simple command-line task manager written in Python. You can add, list, complete, and delete tasks right from your terminal.

---

## ✨ Features
- Add tasks with descriptions
- List all tasks, filter by completed/pending
- Mark tasks as complete
- Delete tasks
- Saves to a local JSON file (no database required)

---

## 🧰 Requirements
- Python **3.9+**
- Works on Linux, macOS, Windows
- No external packages required

---

## 🔧 Installation
```bash
# Clone your fork
git clone https://github.com/<your-username>/Personal-Task-Manager.git
cd Personal-Task-Manager

# (Optional) create virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

---

## 🚀 Usage

Add a task:
```bash
python main.py add "Buy groceries"
```

List tasks:
```bash
python main.py list
python main.py list --status completed
python main.py list --status pending
```

Complete a task:
```bash
python main.py complete 1
```

Delete a task:
```bash
python main.py delete 2
```

Tasks are stored in `tasks.json` automatically.

---

## 🗂 Project structure
```
.
├── main.py            # CLI entry point
├── task_manager.py    # Task logic + storage
├── tasks.json         # Created automatically
└── README.md
```

---

## 🤝 Contributing
1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Commit: `git commit -m "feat: add feature"`
4. Push: `git push origin feature-name`
5. Open a Pull Request

---

## 📄 License
MIT
