"""
Sync endpoints - USER TOOL MODE
These endpoints allow manual/user-triggered synchronization
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from app.services.sync_engine import SyncEngine
from app.services.logger import logger

router = APIRouter()
sync_engine = SyncEngine()


@router.post("/sync")
async def trigger_sync():
    """
    USER TOOL MODE: Manually trigger synchronization
    
    This endpoint allows users to trigger sync on-demand by:
    - Clicking a button in the UI
    - Making an API call
    - Running a script
    
    Returns:
        dict: Sync result with statistics
    """
    try:
        logger.info("🔄 Manual sync triggered by user (USER TOOL MODE)")
        result = await sync_engine.sync()
        logger.info(f"✅ Manual sync completed: {result['message']}")
        return result
    except Exception as e:
        logger.error(f"❌ Manual sync failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sync/status")
async def get_sync_status():
    """
    Get current synchronization status
    
    Returns:
        dict: Current sync statistics and last sync time
    """
    try:
        stats = sync_engine.get_stats()
        return {
            "status": "ok",
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sync/history")
async def get_sync_history(limit: Optional[int] = 10):
    """
    Get synchronization history
    
    Args:
        limit: Number of recent sync records to return
        
    Returns:
        dict: List of recent sync operations
    """
    try:
        history = sync_engine.get_history(limit)
        return {
            "status": "ok",
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/dry-run")
async def dry_run_sync():
    """
    Perform a dry-run sync (preview changes without applying)
    
    Returns:
        dict: Preview of what would be synced
    """
    try:
        logger.info("🔍 Dry-run sync initiated")
        result = await sync_engine.dry_run()
        return result
    except Exception as e:
        logger.error(f"❌ Dry-run failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
