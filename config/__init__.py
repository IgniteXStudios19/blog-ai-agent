# Config Package - Configuration and settings
# This file makes Python treat this directory as a package

from .settings import Settings
from .news_sources import NEWS_SOURCES, RSS_FEEDS
from .prompts import PromptTemplates

__all__ = [
    'Settings',
    'NEWS_SOURCES',
    'RSS_FEEDS',
    'PromptTemplates'
]
