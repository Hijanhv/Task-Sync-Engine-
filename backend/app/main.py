"""
FastAPI entry point for Task Sync Engine
Supports both user-triggered (API calls) and autonomous (scheduled) execution
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import os

from app.config import settings
from app.routes import sync, health, config
from app.services.logger import logger

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A dual-mode task synchronization engine (User Tool + Autonomous Bot)"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(sync.router, prefix="/api", tags=["Sync"])
app.include_router(config.router, prefix="/api", tags=["Configuration"])

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve the frontend UI"""
        return FileResponse(os.path.join(frontend_path, "index.html"))


@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION} starting...")
    logger.info(f"📍 Server running at http://{settings.HOST}:{settings.PORT}")
    logger.info(f"🤖 Auto-sync mode: {'ENABLED' if settings.AUTO_SYNC_ENABLED else 'DISABLED'}")
    
    # Start background sync if auto-sync is enabled (BOT MODE)
    if settings.AUTO_SYNC_ENABLED:
        asyncio.create_task(background_sync_task())
        logger.info(f"⏱️  Auto-sync interval: {settings.SYNC_INTERVAL_SECONDS} seconds")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"👋 {settings.APP_NAME} shutting down...")


async def background_sync_task():
    """
    BOT MODE: Autonomous background sync task
    Runs continuously at specified intervals
    """
    from app.services.sync_engine import SyncEngine
    
    sync_engine = SyncEngine()
    logger.info("🤖 Background sync task started (BOT MODE)")
    
    while True:
        try:
            await asyncio.sleep(settings.SYNC_INTERVAL_SECONDS)
            logger.info("🔄 Auto-sync triggered by scheduler...")
            result = await sync_engine.sync()
            logger.info(f"✅ Auto-sync completed: {result['message']}")
        except Exception as e:
            logger.error(f"❌ Auto-sync failed: {str(e)}")
