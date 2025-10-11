"""
Task Manager Core Module
Handles task data structure and file storage operations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class Task:
    """
    Task class to represent individual tasks
    
    Attributes:
        id (int): Unique identifier for the task
        description (str): Task description
        created_date (str): ISO format timestamp when task was created
        is_completed (bool): Task completion status
    """
    
    def __init__(self, description: str, task_id: int = None):
        """
        Initialize a new Task
        
        Args:
            description (str): The task description
            task_id (int, optional): Specific ID to assign. If None, generates unique ID
        """
        self.id = task_id if task_id else self._generate_id()
        self.description = description
        self.created_date = datetime.now().isoformat()
        self.is_completed = False
    
    def _generate_id(self) -> int:
        """
        Generate a unique ID based on current timestamp
        
        Returns:
            int: Unique task ID
        """
        return int(datetime.now().timestamp() * 1000000)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary for JSON serialization
        
        Returns:
            dict: Task data as dictionary
        """
        return {
            'id': self.id,
            'description': self.description,
            'created_date': self.created_date,
            'is_completed': self.is_completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a Task instance from dictionary data
        
        Args:
            data (dict): Dictionary containing task data
            
        Returns:
            Task: New Task instance
        """
        task = cls(data['description'], data['id'])
        task.created_date = data['created_date']
        task.is_completed = data['is_completed']
        return task
    
    def __repr__(self) -> str:
        """String representation of Task for debugging"""
        status = "✅" if self.is_completed else "⏳"
        return f"Task({status} {self.id}: {self.description})"


class TaskStorage:
    """
    Handle file storage operations for tasks using JSON format
    
    Attributes:
        filename (str): Path to the JSON storage file
    """
    
    def __init__(self, filename: str = 'tasks.json'):
        """
        Initialize TaskStorage
        
        Args:
            filename (str): Path to JSON file for storing tasks
        """
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create empty tasks file if it doesn't exist"""
        if not os.path.exists(self.filename):
            self.save_tasks([])
            print(f"✅ Created new task storage file: {self.filename}")
    
    def load_tasks(self) -> List[Task]:
        """
        Load all tasks from JSON file
        
        Returns:
            List[Task]: List of Task objects loaded from file
        """
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                tasks = [Task.from_dict(task_data) for task_data in data]
                print(f"📂 Loaded {len(tasks)} tasks from {self.filename}")
                return tasks
        except FileNotFoundError:
            print(f"⚠️  File not found: {self.filename}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding JSON: {e}")
            print("   Creating backup and starting fresh...")
            # Create backup of corrupted file
            if os.path.exists(self.filename):
                backup_name = f"{self.filename}.backup"
                os.rename(self.filename, backup_name)
                print(f"   Backup saved as: {backup_name}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error loading tasks: {e}")
            return []
    
    def save_tasks(self, tasks: List[Task]):
        """
        Save all tasks to JSON file
        
        Args:
            tasks (List[Task]): List of Task objects to save
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(
                    [task.to_dict() for task in tasks], 
                    file, 
                    indent=2,
                    ensure_ascii=False
                )
            print(f"💾 Saved {len(tasks)} tasks to {self.filename}")
        except IOError as e:
            print(f"❌ Error writing to file: {e}")
        except Exception as e:
            print(f"❌ Unexpected error saving tasks: {e}")


class TaskManager:
    """
    Main task manager class that handles all task operations
    
    Attributes:
        storage (TaskStorage): Storage handler for persisting tasks
        tasks (List[Task]): In-memory list of all tasks
    """
    
    def __init__(self, storage_file: str = 'tasks.json'):
        """
        Initialize TaskManager
        
        Args:
            storage_file (str): Path to JSON file for storing tasks
        """
        self.storage = TaskStorage(storage_file)
        self.tasks = self.storage.load_tasks()
        print(f"🎯 Task Manager initialized with {len(self.tasks)} existing tasks")
    
    def add_task(self, description: str) -> bool:
        """
        Add a new task to the task list
        
        Args:
            description (str): Task description text
            
        Returns:
            bool: True if task added successfully, False otherwise
        """
        # Validate input - check for None
        if description is None:
            print("❌ Error: Task description cannot be None!")
            return False
        
        # Validate input - check for empty string
        if not description or description.strip() == "":
            print("❌ Error: Task description cannot be empty!")
            print("💡 Tip: Please provide a meaningful task description")
            return False
        
        # Check for excessively long descriptions
        if len(description.strip()) > 500:
            print("❌ Error: Task description is too long (max 500 characters)")
            print(f"   Your description: {len(description.strip())} characters")
            return False
        
        # Create new task with trimmed description
        trimmed_description = description.strip()
        new_task = Task(trimmed_description)
        
        # Add to task list
        self.tasks.append(new_task)
        
        # Persist to file
        try:
            self.storage.save_tasks(self.tasks)
        except Exception as e:
            # Rollback if save fails
            self.tasks.pop()
            print(f"❌ Error: Failed to save task: {e}")
            return False
        
        # Provide user feedback
        print(f"\n✅ Task added successfully!")
        print(f"   ID: {new_task.id}")
        print(f"   Description: {new_task.description}")
        print(f"   Created: {datetime.fromisoformat(new_task.created_date).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Total tasks: {len(self.tasks)}")
        
        return True
    
    def _find_task_by_id(self, task_id: int):
        """
        Helper method to find a task by its ID
        
        Args:
            task_id (int): Task ID to search for
            
        Returns:
            Task or None: Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


# Test functionality when run directly
if __name__ == "__main__":
    print("=" * 70)
    print("Testing Task Manager - Add Task Feature")
    print("=" * 70)
    
    # Initialize TaskManager
    print("\n1. Initializing TaskManager...")
    manager = TaskManager('test_tasks.json')
    
    # Test adding valid tasks
    print("\n2. Testing valid task additions...")
    print("\n   Test 2a: Normal task")
    result1 = manager.add_task("Buy groceries for the week")
    
    print("\n   Test 2b: Task with special characters")
    result2 = manager.add_task("Schedule dentist appointment @ 3:00 PM")
    
    print("\n   Test 2c: Task with numbers")
    result3 = manager.add_task("Read chapters 1-5 of Python book")
    
    # Test edge cases
    print("\n3. Testing edge cases...")
    
    print("\n   Test 3a: Empty string")
    result4 = manager.add_task("")
    
    print("\n   Test 3b: Only whitespace")
    result5 = manager.add_task("   ")
    
    print("\n   Test 3c: Task with leading/trailing spaces (should be trimmed)")
    result6 = manager.add_task("   Complete Python project   ")
    
    print("\n   Test 3d: None value")
    result7 = manager.add_task(None)
    
    print("\n   Test 3e: Very long description")
    long_desc = "A" * 600
    result8 = manager.add_task(long_desc)
    
    print("\n   Test 3f: Single character task")
    result9 = manager.add_task("✓")
    
    # Test data persistence
    print("\n4. Testing data persistence...")
    print("   Creating new TaskManager instance to verify save/load...")
    manager2 = TaskManager('test_tasks.json')
    print(f"   Loaded {len(manager2.tasks)} tasks from storage")
    
    if len(manager2.tasks) == len([r for r in [result1, result2, result3, result6, result9] if r]):
        print("   ✅ Data persistence verified!")
    else:
        print("   ❌ Data persistence failed!")
    
    # Display all tasks
    print("\n5. Current tasks in system:")
    for i, task in enumerate(manager2.tasks, 1):
        print(f"   {i}. {task}")
    
    # Summary
    print("\n6. Test Summary:")
    tests_passed = sum([result1, result2, result3, result6, result9])
    tests_failed = sum([not result4, not result5, not result7, not result8])
    total_tests = tests_passed + tests_failed
    
    print(f"   Total tests: {total_tests}")
    print(f"   ✅ Passed: {tests_passed}")
    print(f"   ❌ Failed: {tests_failed}")
    print(f"   Success rate: {(tests_passed/total_tests)*100:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)
    
    # Cleanup test file
    if os.path.exists('test_tasks.json'):
        os.remove('test_tasks.json')
        print("\n🧹 Cleaned up test file")
