"""
In-memory database for Task Sync Engine
Simple temporary storage - can be replaced with real database later
"""

from typing import Dict, List, Optional
from app.models.task import Task


class MemoryDB:
    """
    Simple in-memory database for storing tasks
    This is a temporary solution for MVP - replace with PostgreSQL/MongoDB later
    """
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def save_task(self, task: Task) -> Task:
        """
        Save a task to the database
        
        Args:
            task: Task to save
            
        Returns:
            Task: Saved task
        """
        self._tasks[task.id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            Task or None if not found
        """
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        return list(self._tasks.values())
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def clear(self):
        """Clear all tasks from the database"""
        self._tasks.clear()
    
    def count(self) -> int:
        """
        Count total tasks
        
        Returns:
            int: Number of tasks
        """
        return len(self._tasks)
