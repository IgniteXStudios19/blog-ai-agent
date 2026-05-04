"""
Discord Publisher - Sends messages to Discord via webhooks
Easiest platform to set up: just need a webhook URL (no API keys!)
"""

import requests
import json
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DiscordPublisher:
    """Publishes content to Discord via webhooks"""
    
    def __init__(self):
        self.webhook_url = settings.DISCORD_WEBHOOK_URL
        
        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured")
    
    def publish_text(self, text):
        """
        Send a simple text message to Discord
        Returns: True if successful, False if failed
        """
        if not self._is_configured():
            return False
        
        logger.info("Sending text message to Discord...")
        
        payload = {
            'content': text[:2000]  # Discord limit: 2000 chars
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204 or response.status_code == 200:
                logger.info("Discord message sent successfully")
                return True
            else:
                logger.error(f"Discord API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Discord message: {str(e)}")
            return False
    
    def publish_embed(self, embed_data):
        """
        Send a rich embed message to Discord
        embed_data should be a dict with: title, description, url, color, thumbnail, footer
        Returns: True if successful, False if failed
        """
        if not self._is_configured():
            return False
        
        logger.info("Sending embed message to Discord...")
        
        payload = {
            'embeds': [embed_data]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204 or response.status_code == 200:
                logger.info("Discord embed sent successfully")
                return True
            else:
                logger.error(f"Discord API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Discord embed: {str(e)}")
            return False
    
    def publish_with_file(self, text, file_path, filename=None):
        """
        Send a message with a file attachment to Discord
        Returns: True if successful, False if failed
        """
        if not self._is_configured():
            return False
        
        logger.info(f"Sending message with file to Discord: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (filename or 'file', f)}
                payload = {
                    'content': text[:2000]
                }
                
                response = requests.post(
                    self.webhook_url,
                    data=payload,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 204 or response.status_code == 200:
                logger.info("Discord message with file sent successfully")
                return True
            else:
                logger.error(f"Discord API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Discord message with file: {str(e)}")
            return False
    
    def publish_blog_post(self, blog_data, blog_url, image_url=None):
        """
        Publish blog post to Discord with rich embed
        Returns: True if successful, False if failed
        """
        if not self._is_configured():
            return False
        
        logger.info(f"Publishing blog to Discord: {blog_data['title']}")
        
        # Create embed
        embed = {
            'title': blog_data['title'][:256],  # Discord embed title limit
            'description': blog_data.get('summary', '')[:2048],  # Description limit
            'url': blog_url,
            'color': 0x5865F2,  # Discord blurple
            'footer': {
                'text': f"Blog AI Agent | {settings.NICHE.title()} News"
            }
        }
        
        if image_url:
            embed['thumbnail'] = {'url': image_url}
        
        # Send embed
        success = self.publish_embed(embed)
        
        # Optionally send audio/video files
        audio_path = blog_data.get('audio_path')
        if audio_path and os.path.exists(audio_path):
            self.publish_with_file("🎧 Audio version:", audio_path)
        
        video_path = blog_data.get('video_path')
        if video_path and os.path.exists(video_path):
            self.publish_with_file("🎥 Video version:", video_path)
        
        return success
    
    def _is_configured(self):
        """Check if Discord is properly configured"""
        if not self.webhook_url:
            logger.error("Discord not configured. Need DISCORD_WEBHOOK_URL")
            return False
        return True
