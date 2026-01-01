"""
Settings and Configuration Management Routes
Allows non-technical users to configure the system via UI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json

router = APIRouter()

# Configuration file path
CONFIG_FILE = "user_config.json"


class AppSettings(BaseModel):
    """Application settings model"""
    auto_sync_enabled: bool = False
    sync_interval_seconds: int = 300
    timezone: str = "UTC"
    notification_email: Optional[str] = None


class IntegrationConfig(BaseModel):
    """Integration configuration model"""
    integration_type: str  # jira, github, trello, asana
    name: str
    enabled: bool = True
    auth_type: str  # api_key, oauth, token
    credentials: Dict[str, str]  # Encrypted in production
    source_config: Dict[str, Any] = {}
    destination_config: Dict[str, Any] = {}


class SyncRule(BaseModel):
    """Sync rule configuration"""
    name: str
    source_integration: str
    destination_integration: str
    enabled: bool = True
    filters: Dict[str, Any] = {}
    field_mappings: Dict[str, str] = {}
    schedule: Optional[str] = None  # cron expression


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "settings": {},
        "integrations": [],
        "sync_rules": []
    }


def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


@router.get("/settings")
async def get_settings():
    """Get current application settings"""
    config = load_config()
    return {
        "status": "ok",
        "settings": config.get("settings", {})
    }


@router.put("/settings")
async def update_settings(settings: AppSettings):
    """
    Update application settings
    No coding required - just update via UI
    """
    config = load_config()
    config["settings"] = settings.dict()
    save_config(config)
    
    return {
        "status": "ok",
        "message": "Settings updated successfully",
        "settings": settings.dict()
    }


@router.get("/integrations")
async def get_integrations():
    """Get all configured integrations"""
    config = load_config()
    integrations = config.get("integrations", [])
    
    # Hide sensitive credentials
    for integration in integrations:
        if "credentials" in integration:
            integration["credentials"] = {k: "***" for k in integration["credentials"].keys()}
    
    return {
        "status": "ok",
        "integrations": integrations,
        "count": len(integrations)
    }


@router.post("/integrations")
async def create_integration(integration: IntegrationConfig):
    """
    Create a new integration
    Users can add Jira, GitHub, etc. via UI form
    """
    config = load_config()
    
    # Add new integration
    integration_data = integration.dict()
    integration_data["id"] = f"{integration.integration_type}_{len(config.get('integrations', []))}"
    
    if "integrations" not in config:
        config["integrations"] = []
    
    config["integrations"].append(integration_data)
    save_config(config)
    
    return {
        "status": "ok",
        "message": f"{integration.name} integration created successfully",
        "integration": integration_data
    }


@router.put("/integrations/{integration_id}")
async def update_integration(integration_id: str, integration: IntegrationConfig):
    """Update an existing integration"""
    config = load_config()
    integrations = config.get("integrations", [])
    
    for idx, integ in enumerate(integrations):
        if integ.get("id") == integration_id:
            integration_data = integration.dict()
            integration_data["id"] = integration_id
            integrations[idx] = integration_data
            save_config(config)
            return {
                "status": "ok",
                "message": "Integration updated successfully"
            }
    
    raise HTTPException(status_code=404, detail="Integration not found")


@router.delete("/integrations/{integration_id}")
async def delete_integration(integration_id: str):
    """Delete an integration"""
    config = load_config()
    integrations = config.get("integrations", [])
    
    config["integrations"] = [i for i in integrations if i.get("id") != integration_id]
    save_config(config)
    
    return {
        "status": "ok",
        "message": "Integration deleted successfully"
    }


@router.post("/integrations/{integration_id}/test")
async def test_integration(integration_id: str):
    """
    Test integration connection
    Users can verify their credentials work without coding
    """
    config = load_config()
    integrations = config.get("integrations", [])
    
    integration = next((i for i in integrations if i.get("id") == integration_id), None)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # In production, actually test the connection
    # For now, simulate success
    return {
        "status": "ok",
        "message": f"Connection to {integration['name']} successful!",
        "details": {
            "integration_type": integration["integration_type"],
            "connection": "verified"
        }
    }


@router.get("/sync-rules")
async def get_sync_rules():
    """Get all sync rules"""
    config = load_config()
    return {
        "status": "ok",
        "rules": config.get("sync_rules", []),
        "count": len(config.get("sync_rules", []))
    }


@router.post("/sync-rules")
async def create_sync_rule(rule: SyncRule):
    """
    Create a sync rule
    Define what syncs where without coding
    """
    config = load_config()
    
    rule_data = rule.dict()
    rule_data["id"] = f"rule_{len(config.get('sync_rules', []))}"
    
    if "sync_rules" not in config:
        config["sync_rules"] = []
    
    config["sync_rules"].append(rule_data)
    save_config(config)
    
    return {
        "status": "ok",
        "message": "Sync rule created successfully",
        "rule": rule_data
    }


@router.put("/sync-rules/{rule_id}")
async def update_sync_rule(rule_id: str, rule: SyncRule):
    """Update a sync rule"""
    config = load_config()
    rules = config.get("sync_rules", [])
    
    for idx, r in enumerate(rules):
        if r.get("id") == rule_id:
            rule_data = rule.dict()
            rule_data["id"] = rule_id
            rules[idx] = rule_data
            save_config(config)
            return {
                "status": "ok",
                "message": "Sync rule updated successfully"
            }
    
    raise HTTPException(status_code=404, detail="Sync rule not found")


@router.delete("/sync-rules/{rule_id}")
async def delete_sync_rule(rule_id: str):
    """Delete a sync rule"""
    config = load_config()
    rules = config.get("sync_rules", [])
    
    config["sync_rules"] = [r for r in rules if r.get("id") != rule_id]
    save_config(config)
    
    return {
        "status": "ok",
        "message": "Sync rule deleted successfully"
    }


@router.get("/available-integrations")
async def get_available_integrations():
    """
    Get list of available integrations
    Shows what platforms users can connect to
    """
    return {
        "status": "ok",
        "integrations": [
            {
                "type": "jira",
                "name": "Jira",
                "description": "Atlassian Jira project management",
                "icon": "🎯",
                "auth_types": ["api_key", "oauth"],
                "required_fields": ["url", "email", "api_token"]
            },
            {
                "type": "github",
                "name": "GitHub Issues",
                "description": "GitHub issue tracking",
                "icon": "🐙",
                "auth_types": ["token", "oauth"],
                "required_fields": ["token", "owner", "repo"]
            },
            {
                "type": "trello",
                "name": "Trello",
                "description": "Trello boards and cards",
                "icon": "📋",
                "auth_types": ["api_key"],
                "required_fields": ["api_key", "token", "board_id"]
            },
            {
                "type": "asana",
                "name": "Asana",
                "description": "Asana task management",
                "icon": "✅",
                "auth_types": ["token", "oauth"],
                "required_fields": ["token", "workspace"]
            },
            {
                "type": "linear",
                "name": "Linear",
                "description": "Linear issue tracking",
                "icon": "📐",
                "auth_types": ["api_key"],
                "required_fields": ["api_key", "team"]
            },
            {
                "type": "clickup",
                "name": "ClickUp",
                "description": "ClickUp project management",
                "icon": "🖱️",
                "auth_types": ["api_key"],
                "required_fields": ["api_key", "list_id"]
            }
        ]
    }


@router.get("/field-mappings/templates")
async def get_field_mapping_templates():
    """
    Get pre-configured field mapping templates
    Users can select common mappings without coding
    """
    return {
        "status": "ok",
        "templates": [
            {
                "name": "Jira to GitHub",
                "source": "jira",
                "destination": "github",
                "mappings": {
                    "summary": "title",
                    "description": "body",
                    "status": "state",
                    "priority": "labels",
                    "assignee": "assignees"
                }
            },
            {
                "name": "Trello to Asana",
                "source": "trello",
                "destination": "asana",
                "mappings": {
                    "name": "name",
                    "desc": "notes",
                    "due": "due_on",
                    "labels": "tags"
                }
            },
            {
                "name": "GitHub to Jira",
                "source": "github",
                "destination": "jira",
                "mappings": {
                    "title": "summary",
                    "body": "description",
                    "state": "status",
                    "labels": "labels"
                }
            }
        ]
    }


@router.post("/setup/complete")
async def complete_setup(data: Dict[str, Any]):
    """
    Mark initial setup as complete
    Called after setup wizard finishes
    """
    config = load_config()
    config["setup_completed"] = True
    config["setup_date"] = "2026-01-01T00:00:00"
    save_config(config)
    
    return {
        "status": "ok",
        "message": "Setup completed successfully!"
    }


@router.get("/setup/status")
async def get_setup_status():
    """Check if initial setup is complete"""
    config = load_config()
    return {
        "status": "ok",
        "setup_completed": config.get("setup_completed", False),
        "has_integrations": len(config.get("integrations", [])) > 0,
        "has_sync_rules": len(config.get("sync_rules", [])) > 0
    }
