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


# Test functionality when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Task Manager - Basic Structure & Storage")
    print("=" * 60)
    
    # Initialize storage
    print("\n1. Initializing TaskStorage...")
    storage = TaskStorage('test_tasks.json')
    
    # Create sample tasks
    print("\n2. Creating sample tasks...")
    task1 = Task("Learn GitHub workflow")
    task2 = Task("Practice opening issues")
    task3 = Task("Master pull requests")
    
    print(f"   Created: {task1}")
    print(f"   Created: {task2}")
    print(f"   Created: {task3}")
    
    # Test save functionality
    print("\n3. Testing save functionality...")
    tasks = [task1, task2, task3]
    storage.save_tasks(tasks)
    
    # Test load functionality
    print("\n4. Testing load functionality...")
    loaded_tasks = storage.load_tasks()
    
    # Verify data integrity
    print("\n5. Verifying data integrity...")
    print(f"   Original tasks: {len(tasks)}")
    print(f"   Loaded tasks: {len(loaded_tasks)}")
    
    if len(tasks) == len(loaded_tasks):
        print("   ✅ Task count matches!")
    else:
        print("   ❌ Task count mismatch!")
    
    # Display loaded tasks
    print("\n6. Loaded tasks:")
    for i, task in enumerate(loaded_tasks, 1):
        print(f"   {i}. {task}")
        print(f"      ID: {task.id}")
        print(f"      Description: {task.description}")
        print(f"      Created: {task.created_date}")
        print(f"      Completed: {task.is_completed}")
    
    # Test task modification
    print("\n7. Testing task modification...")
    if loaded_tasks:
        loaded_tasks[0].is_completed = True
        storage.save_tasks(loaded_tasks)
        print(f"   Modified task: {loaded_tasks[0]}")
        
        # Reload to verify persistence
        reloaded_tasks = storage.load_tasks()
        print(f"   Reloaded task: {reloaded_tasks[0]}")
        
        if reloaded_tasks[0].is_completed:
            print("   ✅ Modification persisted successfully!")
        else:
            print("   ❌ Modification not persisted!")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    
    # Cleanup test file
    if os.path.exists('test_tasks.json'):
        os.remove('test_tasks.json')
        print("\n🧹 Cleaned up test file")
