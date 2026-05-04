"""
Settings Configuration - Central configuration for the Blog AI Agent
Loads all settings from environment variables with sensible defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Central settings class that loads all configuration from environment variables"""
    
    # AI API Keys (Required: At least one)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
    
    # News API Keys (Required: At least one)
    GUARDIAN_API_KEY = os.getenv('GUARDIAN_API_KEY', '')
    GNEWS_API_KEY = os.getenv('GNEWS_API_KEY', '')
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
    
    # Image API Keys (Required for video generation)
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '')
    
    # Blog Platforms
    HASHNODE_API_KEY = os.getenv('HASHNODE_API_KEY', '')
    HASHNODE_PUBLICATION_ID = os.getenv('HASHNODE_PUBLICATION_ID', '')
    
    # Social Media Platforms
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '').strip()  # Remove whitespace/newlines
    
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
    
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USERNAME = os.getenv('REDDIT_USERNAME', '')
    REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD', '')
    
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
    
    MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN', '')
    MASTODON_API_BASE_URL = os.getenv('MASTODON_API_BASE_URL', 'https://mastodon.social')
    
    # System Settings (handle empty strings properly)
    NICHE = os.getenv('NICHE', 'technology')  # Blog topic
    POSTS_PER_RUN = int(os.getenv('POSTS_PER_RUN') or '3')  # Posts per 6-hour run
    BLOG_LANGUAGE = os.getenv('BLOG_LANGUAGE', 'english')
    MIN_ARTICLE_WORDS = int(os.getenv('MIN_ARTICLE_WORDS') or '800')
    MAX_ARTICLE_WORDS = int(os.getenv('MAX_ARTICLE_WORDS') or '1500')
    
    # AI Model Settings (CURRENT WORKING MODELS - Updated 2026)
    PRIMARY_AI = 'groq' if GROQ_API_KEY else 'gemini'
    GROQ_MODEL = 'llama-3.1-8b-instant'  # Current fast Groq model
    GEMINI_MODEL = 'gemini-1.5-flash'  # Current fast Gemini model
    
    # TTS Settings
    TTS_VOICE = 'en-US-AriaNeural'  # Microsoft Edge TTS voice
    TTS_RATE = '+0%'  # Speech rate adjustment
    
    # Video Settings
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    VIDEO_FPS = 24
    IMAGE_DURATION = 5  # Seconds per image in video
    BG_MUSIC_VOLUME = 0.2  # 20% volume for background music
    
    # Database Settings
    DATABASE_PATH = 'database/blog_agent.db'
    
    # Output Directories
    OUTPUT_DIR = 'output'
    BLOGS_DIR = f'{OUTPUT_DIR}/blogs'
    AUDIO_DIR = f'{OUTPUT_DIR}/audio'
    VIDEOS_DIR = f'{OUTPUT_DIR}/videos'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'blog_agent.log'
    
    @classmethod
    def validate_required_keys(cls):
        """Validate that at least minimum required API keys are present"""
        errors = []
        
        # Check AI keys
        if not cls.GROQ_API_KEY and not cls.GEMINI_API_KEY:
            errors.append("At least one AI API key required: GROQ_API_KEY or GEMINI_API_KEY")
        
        # Check news sources
        if not any([cls.GUARDIAN_API_KEY, cls.GNEWS_API_KEY, cls.NEWSAPI_KEY]):
            errors.append("At least one news API key recommended")
        
        # Check blog platform
        if not cls.HASHNODE_API_KEY:
            errors.append("HASHNODE_API_KEY required for blog publishing")
        
        return errors
    
    @classmethod
    def print_status(cls):
        """Print current configuration status"""
        print("=== Blog AI Agent Configuration ===")
        print(f"Niche: {cls.NICHE}")
        print(f"Posts per run: {cls.POSTS_PER_RUN}")
        print(f"Language: {cls.BLOG_LANGUAGE}")
        print(f"AI Model: {cls.PRIMARY_AI}")
        print(f"Groq Model: {cls.GROQ_MODEL}")
        print(f"Gemini Model: {cls.GEMINI_MODEL}")
        print(f"Groq API: {'✓' if cls.GROQ_API_KEY else '✗'}")
        print(f"Gemini API: {'✓' if cls.GEMINI_API_KEY else '✗'}")
        print(f"Hashnode: {'✓' if cls.HASHNODE_API_KEY else '✗'}")
        print(f"Telegram: {'✓' if cls.TELEGRAM_BOT_TOKEN else '✗'}")
        print(f"Twitter: {'✓' if cls.TWITTER_API_KEY else '✗'}")
        print(f"Discord: {'✓' if cls.DISCORD_WEBHOOK_URL else '✗'}")
        print(f"Mastodon: {'✓' if cls.MASTODON_ACCESS_TOKEN else '✗'}")

# Create a global settings instance
settings = Settings()
