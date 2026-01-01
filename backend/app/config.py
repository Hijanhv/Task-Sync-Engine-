"""
Configuration management for Task Sync Engine
Loads environment variables and provides app settings
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # App configuration
    APP_NAME: str = "Task Sync Engine"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Sync configuration
    SYNC_INTERVAL_SECONDS: int = int(os.getenv("SYNC_INTERVAL_SECONDS", "300"))  # 5 minutes
    AUTO_SYNC_ENABLED: bool = os.getenv("AUTO_SYNC_ENABLED", "False").lower() == "true"
    
    # Source and destination configuration (can be extended)
    SOURCE_API_URL: Optional[str] = os.getenv("SOURCE_API_URL")
    DESTINATION_API_URL: Optional[str] = os.getenv("DESTINATION_API_URL")

    # GitHub Integration
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_SOURCE_REPO: Optional[str] = os.getenv("GITHUB_SOURCE_REPO")  # Format: "owner/repo"
    GITHUB_DEST_REPO: Optional[str] = os.getenv("GITHUB_DEST_REPO")  # Format: "owner/repo"

    # Integration mode
    SOURCE_TYPE: str = os.getenv("SOURCE_TYPE", "mock")  # "mock" or "github"
    DEST_TYPE: str = os.getenv("DEST_TYPE", "mock")  # "mock" or "github"

    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]


settings = Settings()
