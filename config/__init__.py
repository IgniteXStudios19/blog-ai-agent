# Config Package - Configuration and settings
# This file makes Python treat this directory as a package

from .settings import Settings
from .news_sources import RSS_FEEDS, NEWS_APIS, REDDIT_SUBREDDITS
from .prompts import PromptTemplates

__all__ = [
    'Settings',
    'RSS_FEEDS',
    'NEWS_APIS',
    'REDDIT_SUBREDDITS',
    'PromptTemplates'
]
