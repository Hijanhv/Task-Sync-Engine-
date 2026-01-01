"""
Health check endpoint
"""

from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns system status and configuration
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "bot + user-tool" if settings.AUTO_SYNC_ENABLED else "user-tool",
        "auto_sync_enabled": settings.AUTO_SYNC_ENABLED,
        "sync_interval_seconds": settings.SYNC_INTERVAL_SECONDS
    }
