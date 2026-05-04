# Database Package - Handles all database operations
# This file makes Python treat this directory as a package

from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
