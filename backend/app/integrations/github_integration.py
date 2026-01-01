"""
GitHub Issues Integration
Connects to GitHub API to fetch and sync issues
"""

import requests
from typing import List, Optional
from datetime import datetime

from app.models.task import Task
from app.services.logger import logger


class GitHubIntegration:
    """
    GitHub Issues integration
    Fetches issues from a GitHub repository and converts them to Tasks
    """

    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        Initialize GitHub integration

        Args:
            token: GitHub personal access token
            repo_owner: Repository owner (username or organization)
            repo_name: Repository name
        """
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def fetch_issues(self, state: str = "all") -> List[Task]:
        """
        Fetch issues from GitHub repository

        Args:
            state: Issue state - "open", "closed", or "all" (default: "all")

        Returns:
            List[Task]: List of tasks converted from GitHub issues
        """
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {
            "state": state,
            "per_page": 100  # Max 100 issues per page
        }

        try:
            logger.info(f"📥 Fetching issues from {self.repo_owner}/{self.repo_name}...")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            issues = response.json()

            # Filter out pull requests (GitHub API returns PRs as issues)
            issues = [issue for issue in issues if "pull_request" not in issue]

            logger.info(f"✅ Fetched {len(issues)} issues from GitHub")

            # Convert GitHub issues to Tasks
            tasks = []
            for issue in issues:
                task = self._convert_issue_to_task(issue)
                tasks.append(task)

            return tasks

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to fetch GitHub issues: {str(e)}")
            raise Exception(f"GitHub API error: {str(e)}")

    def _convert_issue_to_task(self, issue: dict) -> Task:
        """
        Convert a GitHub issue to a Task object

        Args:
            issue: GitHub issue data

        Returns:
            Task: Converted task
        """
        # Map GitHub state to our status
        status_map = {
            "open": "todo",
            "closed": "done"
        }

        # Determine priority from labels
        priority = "medium"  # default
        labels = [label["name"].lower() for label in issue.get("labels", [])]

        if "priority: high" in labels or "urgent" in labels:
            priority = "high"
        elif "priority: low" in labels:
            priority = "low"

        # Parse dates
        created_at = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00"))

        return Task(
            id=f"github-{issue['number']}",
            title=issue["title"],
            description=issue.get("body") or "",
            status=status_map.get(issue["state"], "todo"),
            priority=priority,
            created_at=created_at,
            updated_at=updated_at,
            metadata={
                "source": "github",
                "github_number": issue["number"],
                "github_url": issue["html_url"],
                "github_state": issue["state"],
                "labels": [label["name"] for label in issue.get("labels", [])]
            }
        )

    def create_issue(self, task: Task) -> dict:
        """
        Create a new issue in GitHub from a Task

        Args:
            task: Task to create as GitHub issue

        Returns:
            dict: Created issue data
        """
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"

        data = {
            "title": task.title,
            "body": task.description,
            "labels": []
        }

        # Add priority label
        if task.priority == "high":
            data["labels"].append("priority: high")
        elif task.priority == "low":
            data["labels"].append("priority: low")

        try:
            logger.info(f"📤 Creating GitHub issue: {task.title}")
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()

            issue = response.json()
            logger.info(f"✅ Created GitHub issue #{issue['number']}")

            return issue

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to create GitHub issue: {str(e)}")
            raise Exception(f"GitHub API error: {str(e)}")

    def update_issue(self, issue_number: int, task: Task) -> dict:
        """
        Update an existing GitHub issue

        Args:
            issue_number: GitHub issue number
            task: Task with updated data

        Returns:
            dict: Updated issue data
        """
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"

        data = {
            "title": task.title,
            "body": task.description,
            "state": "open" if task.status != "done" else "closed"
        }

        try:
            logger.info(f"📤 Updating GitHub issue #{issue_number}")
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()

            issue = response.json()
            logger.info(f"✅ Updated GitHub issue #{issue_number}")

            return issue

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to update GitHub issue: {str(e)}")
            raise Exception(f"GitHub API error: {str(e)}")
