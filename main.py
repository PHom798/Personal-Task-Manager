# main.py - Basic structure
if __name__ == "__main__":
    # Test the basic functionality
    storage = TaskStorage()
    
    # Create a sample task
    task = Task("Learn GitHub workflow")
    
    # Test save and load
    storage.save_tasks([task])
    loaded_tasks = storage.load_tasks()
    
    print(f"Task saved and loaded successfully!")
    print(f"Task: {loaded_tasks[0].description}")
    print(f"ID: {loaded_tasks[0].id}")
    print(f"Created: {loaded_tasks[0].created_date}")
