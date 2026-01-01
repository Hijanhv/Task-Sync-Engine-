"""
Logging helper for Task Sync Engine
"""

import logging
import sys
from datetime import datetime

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("TaskSyncEngine")


def log_sync_event(event_type: str, details: dict):
    """
    Log a synchronization event with structured data
    
    Args:
        event_type: Type of event (start, complete, error, etc.)
        details: Event details dictionary
    """
    timestamp = datetime.utcnow().isoformat()
    logger.info(f"[SYNC_EVENT] {event_type} | {timestamp} | {details}")


def log_api_call(endpoint: str, method: str, status: int):
    """
    Log an API call
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        status: Response status code
    """
    logger.info(f"[API] {method} {endpoint} - Status: {status}")
