"""
Logger Utility - Configures logging for the entire application
Uses loguru for simple, colorful, and powerful logging
"""

import sys
from pathlib import Path
from loguru import logger
from config.settings import settings

def setup_logger(name=__name__, log_file=None):
    """
    Configure and return a logger instance
    Logs to both console (colored) and file
    """
    # Remove default handler
    logger.remove()
    
    # Console handler (colored output)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # File handler (no color codes in file)
    if log_file is None:
        log_file = settings.LOG_FILE
    
    log_path = Path(log_file)
    logger.add(
        log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",  # Rotate when file reaches 10MB
        retention="30 days",  # Keep logs for 30 days
        compression="zip"  # Compress rotated logs
    )
    
    return logger

# Create a default logger instance
default_logger = setup_logger()

# Export the logger
__all__ = ['setup_logger', 'default_logger', 'logger']
