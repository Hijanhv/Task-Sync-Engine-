"""
Data loader for Task Sync Engine
Responsible for loading data from source and destination systems
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import random

from app.models.task import Task
from app.services.logger import logger
from app.config import settings


class DataLoader:
    """
    Loads data from various sources and destinations
    Can be extended to support different integrations (APIs, databases, files, etc.)
    """

    def __init__(self):
        self.source_type = settings.SOURCE_TYPE
        self.destination_type = settings.DEST_TYPE

        # Initialize GitHub integrations if configured
        self.github_source = None
        self.github_dest = None

        if self.source_type == "github" and settings.GITHUB_TOKEN and settings.GITHUB_SOURCE_REPO:
            from app.integrations.github_integration import GitHubIntegration
            owner, repo = settings.GITHUB_SOURCE_REPO.split("/")
            self.github_source = GitHubIntegration(settings.GITHUB_TOKEN, owner, repo)
            logger.info(f"✅ GitHub source integration initialized: {settings.GITHUB_SOURCE_REPO}")

        if self.destination_type == "github" and settings.GITHUB_TOKEN and settings.GITHUB_DEST_REPO:
            from app.integrations.github_integration import GitHubIntegration
            owner, repo = settings.GITHUB_DEST_REPO.split("/")
            self.github_dest = GitHubIntegration(settings.GITHUB_TOKEN, owner, repo)
            logger.info(f"✅ GitHub destination integration initialized: {settings.GITHUB_DEST_REPO}")
    
    async def load_source_tasks(self) -> List[Task]:
        """
        Load tasks from the source system

        Returns:
            List[Task]: Tasks from the source
        """
        logger.info(f"📥 Loading tasks from source ({self.source_type})...")

        if self.source_type == "github" and self.github_source:
            tasks = self.github_source.fetch_issues(state="all")
        else:
            # Fallback to mock data
            tasks = self._generate_mock_source_tasks()

        logger.info(f"✅ Loaded {len(tasks)} tasks from source")
        return tasks
    
    async def load_destination_tasks(self) -> List[Task]:
        """
        Load tasks from the destination system

        Returns:
            List[Task]: Tasks from the destination
        """
        logger.info(f"📥 Loading tasks from destination ({self.destination_type})...")

        if self.destination_type == "github" and self.github_dest:
            tasks = self.github_dest.fetch_issues(state="all")
        else:
            # Fallback to mock data
            tasks = self._generate_mock_destination_tasks()

        logger.info(f"✅ Loaded {len(tasks)} tasks from destination")
        return tasks
    
    async def push_to_destination(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Push tasks to the destination system

        Args:
            tasks: List of tasks to push

        Returns:
            dict: Result of the push operation
        """
        logger.info(f"📤 Pushing {len(tasks)} tasks to destination ({self.destination_type})...")

        success_count = 0
        failed_count = 0

        if self.destination_type == "github" and self.github_dest:
            for task in tasks:
                try:
                    # Check if task already exists in GitHub (has github-XX id)
                    if task.id.startswith("github-"):
                        # Update existing issue
                        issue_number = int(task.id.replace("github-", ""))
                        self.github_dest.update_issue(issue_number, task)
                    else:
                        # Create new issue
                        self.github_dest.create_issue(task)
                    success_count += 1
                except Exception as e:
                    logger.error(f"Failed to push task {task.id}: {str(e)}")
                    failed_count += 1
        else:
            # Mock implementation
            success_count = len(tasks)

        logger.info(f"✅ Successfully pushed {success_count} tasks, {failed_count} failed")
        return {
            "success": True,
            "pushed_count": success_count,
            "failed_count": failed_count
        }
    
    def _generate_mock_source_tasks(self) -> List[Task]:
        """Generate mock source tasks for testing"""
        return [
            Task(
                id="src-1",
                title="Implement authentication",
                description="Add OAuth2 authentication to the API",
                status="in_progress",
                priority="high",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Task(
                id="src-2",
                title="Write documentation",
                description="Document all API endpoints",
                status="todo",
                priority="medium",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Task(
                id="src-3",
                title="Fix bug in sync engine",
                description="Resolve memory leak issue",
                status="in_progress",
                priority="high",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
        ]
    
    def _generate_mock_destination_tasks(self) -> List[Task]:
        """Generate mock destination tasks for testing"""
        return [
            Task(
                id="dest-1",
                title="Setup CI/CD pipeline",
                description="Configure GitHub Actions",
                status="done",
                priority="medium",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Task(
                id="dest-2",
                title="Write unit tests",
                description="Add tests for sync engine",
                status="todo",
                priority="high",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
        ]
