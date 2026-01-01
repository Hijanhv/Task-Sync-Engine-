"""
Core Sync Engine
Implements the synchronization logic for tasks
Works in both USER TOOL mode (manual trigger) and BOT mode (automatic)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque

from app.models.task import Task
from app.services.data_loader import DataLoader
from app.db.memory_db import MemoryDB
from app.services.logger import logger, log_sync_event


class SyncEngine:
    """
    Core synchronization engine
    
    This engine supports dual execution modes:
    1. USER TOOL MODE: Triggered manually via API/UI
    2. BOT MODE: Triggered automatically by scheduler
    
    The same sync logic is used in both cases
    """
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.db = MemoryDB()
        self.sync_history = deque(maxlen=100)  # Store last 100 sync operations
        self.total_syncs = 0
        self.last_sync_time: Optional[datetime] = None
    
    async def sync(self) -> Dict[str, Any]:
        """
        Main synchronization method
        Can be called by:
        - User clicking a button (USER TOOL MODE)
        - Scheduled task (BOT MODE)
        - API call (USER TOOL MODE)
        
        Returns:
            dict: Sync result with statistics
        """
        start_time = datetime.utcnow()
        
        try:
            log_sync_event("sync_start", {"timestamp": start_time.isoformat()})
            
            # Step 1: Load data from source and destination
            source_tasks = await self.data_loader.load_source_tasks()
            destination_tasks = await self.data_loader.load_destination_tasks()
            
            # Step 2: Compare and identify differences
            changes = self._identify_changes(source_tasks, destination_tasks)
            
            # Step 3: Apply changes to destination
            if changes["to_add"] or changes["to_update"]:
                tasks_to_push = changes["to_add"] + changes["to_update"]
                push_result = await self.data_loader.push_to_destination(tasks_to_push)
            else:
                push_result = {"success": True, "pushed_count": 0, "failed_count": 0}
            
            # Step 4: Update local database
            self._update_local_db(source_tasks)
            
            # Step 5: Record sync operation
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            sync_record = {
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration,
                "source_count": len(source_tasks),
                "destination_count": len(destination_tasks),
                "added": len(changes["to_add"]),
                "updated": len(changes["to_update"]),
                "unchanged": len(changes["unchanged"]),
                "success": push_result["success"]
            }
            
            self.sync_history.append(sync_record)
            self.total_syncs += 1
            self.last_sync_time = end_time
            
            log_sync_event("sync_complete", sync_record)
            
            return {
                "success": True,
                "message": f"Sync completed successfully",
                "stats": sync_record
            }
            
        except Exception as e:
            error_time = datetime.utcnow()
            error_record = {
                "timestamp": error_time.isoformat(),
                "error": str(e),
                "success": False
            }
            self.sync_history.append(error_record)
            
            log_sync_event("sync_error", error_record)
            raise
    
    async def dry_run(self) -> Dict[str, Any]:
        """
        Perform a dry-run (preview changes without applying)
        
        Returns:
            dict: Preview of what would be synced
        """
        logger.info("🔍 Starting dry-run sync...")
        
        source_tasks = await self.data_loader.load_source_tasks()
        destination_tasks = await self.data_loader.load_destination_tasks()
        
        changes = self._identify_changes(source_tasks, destination_tasks)
        
        return {
            "dry_run": True,
            "preview": {
                "tasks_to_add": [task.dict() for task in changes["to_add"]],
                "tasks_to_update": [task.dict() for task in changes["to_update"]],
                "tasks_unchanged": len(changes["unchanged"])
            },
            "source_count": len(source_tasks),
            "destination_count": len(destination_tasks)
        }
    
    def _identify_changes(self, source_tasks: List[Task], destination_tasks: List[Task]) -> Dict[str, List[Task]]:
        """
        Identify differences between source and destination
        
        Args:
            source_tasks: Tasks from source system
            destination_tasks: Tasks from destination system
            
        Returns:
            dict: Categorized changes (to_add, to_update, unchanged)
        """
        logger.info("🔍 Identifying changes...")
        
        dest_task_map = {task.id: task for task in destination_tasks}
        
        to_add = []
        to_update = []
        unchanged = []
        
        for source_task in source_tasks:
            if source_task.id not in dest_task_map:
                to_add.append(source_task)
            else:
                dest_task = dest_task_map[source_task.id]
                if self._task_has_changed(source_task, dest_task):
                    to_update.append(source_task)
                else:
                    unchanged.append(source_task)
        
        logger.info(f"📊 Changes: {len(to_add)} to add, {len(to_update)} to update, {len(unchanged)} unchanged")
        
        return {
            "to_add": to_add,
            "to_update": to_update,
            "unchanged": unchanged
        }
    
    def _task_has_changed(self, source_task: Task, dest_task: Task) -> bool:
        """
        Check if a task has changed using timestamp-based comparison

        Args:
            source_task: Task from source
            dest_task: Task from destination

        Returns:
            bool: True if task has changed
        """
        # First check if updated_at timestamp is newer
        if source_task.updated_at > dest_task.updated_at:
            return True

        # Fallback to field comparison if timestamps are equal
        return (
            source_task.title != dest_task.title or
            source_task.description != dest_task.description or
            source_task.status != dest_task.status or
            source_task.priority != dest_task.priority
        )
    
    def _update_local_db(self, tasks: List[Task]):
        """
        Update local database with current tasks
        
        Args:
            tasks: Tasks to store
        """
        for task in tasks:
            self.db.save_task(task)
        logger.info(f"💾 Updated local database with {len(tasks)} tasks")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get synchronization statistics
        
        Returns:
            dict: Current statistics
        """
        return {
            "total_syncs": self.total_syncs,
            "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None,
            "tasks_in_db": len(self.db.get_all_tasks())
        }
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get sync history
        
        Args:
            limit: Number of records to return
            
        Returns:
            list: Recent sync records
        """
        return list(self.sync_history)[-limit:]
