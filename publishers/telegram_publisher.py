"""
Telegram Publisher - Sends messages, images, audio, video to Telegram channel
Telegram is the BEST platform to start with: NO rate limits, completely free API
"""

import os
import requests
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramPublisher:
    """Publishes content to Telegram channel via Bot API"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.channel_id = settings.TELEGRAM_CHANNEL_ID
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}'
        
        if not self.bot_token:
            logger.warning("Telegram bot token not configured")
        if not self.channel_id:
            logger.warning("Telegram channel ID not configured")
    
    def publish_text(self, text, parse_mode='HTML'):
        """
        Send text message to Telegram channel
        parse_mode: 'HTML' or 'MarkdownV2'
        Returns: Message ID if successful, None if failed
        """
        if not self._is_configured():
            return None
        
        logger.info("Sending text message to Telegram...")
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.channel_id,
            'text': text[:4096],  # Telegram limit: 4096 chars
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get('ok'):
                message_id = result['result']['message_id']
                logger.info(f"Text message sent successfully (ID: {message_id})")
                return message_id
            else:
                logger.error(f"Telegram API error: {result.get('description')}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {str(e)}")
            return None
    
    def publish_photo(self, photo_path, caption=None, parse_mode='HTML'):
        """Send photo with optional caption to Telegram channel"""
        if not self._is_configured():
            return None
        
        logger.info(f"Sending photo to Telegram: {photo_path}")
        
        url = f"{self.base_url}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as photo:
                payload = {
                    'chat_id': self.channel_id,
                    'caption': caption[:1024] if caption else '',  # Caption limit
                    'parse_mode': parse_mode
                }
                
                files = {'photo': photo}
                response = requests.post(url, data=payload, files=files, timeout=30)
                
            result = response.json()
            
            if result.get('ok'):
                message_id = result['result']['message_id']
                logger.info(f"Photo sent successfully (ID: {message_id})")
                return message_id
            else:
                logger.error(f"Telegram API error: {result.get('description')}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send photo: {str(e)}")
            return None
    
    def publish_audio(self, audio_path, caption=None, title=None):
        """Send audio file (MP3) to Telegram channel"""
        if not self._is_configured():
            return None
        
        logger.info(f"Sending audio to Telegram: {audio_path}")
        
        url = f"{self.base_url}/sendAudio"
        
        try:
            with open(audio_path, 'rb') as audio:
                payload = {
                    'chat_id': self.channel_id,
                    'caption': caption[:1024] if caption else '',
                    'title': title or 'Audio',
                    'performer': 'Blog AI Agent'
                }
                
                files = {'audio': audio}
                response = requests.post(url, data=payload, files=files, timeout=60)
                
            result = response.json()
            
            if result.get('ok'):
                message_id = result['result']['message_id']
                logger.info(f"Audio sent successfully (ID: {message_id})")
                return message_id
            else:
                logger.error(f"Telegram API error: {result.get('description')}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send audio: {str(e)}")
            return None
    
    def publish_video(self, video_path, caption=None):
        """Send video file to Telegram channel"""
        if not self._is_configured():
            return None
        
        logger.info(f"Sending video to Telegram: {video_path}")
        
        url = f"{self.base_url}/sendVideo"
        
        try:
            with open(video_path, 'rb') as video:
                payload = {
                    'chat_id': self.channel_id,
                    'caption': caption[:1024] if caption else '',
                    'supports_streaming': True
                }
                
                files = {'video': video}
                response = requests.post(url, data=payload, files=files, timeout=120)
                
            result = response.json()
            
            if result.get('ok'):
                message_id = result['result']['message_id']
                logger.info(f"Video sent successfully (ID: {message_id})")
                return message_id
            else:
                logger.error(f"Telegram API error: {result.get('description')}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send video: {str(e)}")
            return None
    
    def publish_blog_post(self, blog_data, blog_url):
        """
        Publish a complete blog post to Telegram
        Sends: Text message + Image (if available) + Audio (if available) + Video (if available)
        """
        if not self._is_configured():
            return None
        
        logger.info(f"Publishing blog post to Telegram: {blog_data['title']}")
        
        message_ids = []
        
        # 1. Send text message with blog link
        text = f"<b>{blog_data['title']}</b>\n\n"
        text += f"{blog_data.get('summary', '')[:200]}...\n\n"
        text += f"📖 <a href='{blog_url}'>Read full article</a>"
        
        msg_id = self.publish_text(text)
        if msg_id:
            message_ids.append(msg_id)
        
        # 2. Send audio if available
        audio_path = blog_data.get('audio_path')
        if audio_path and os.path.exists(audio_path):
            audio_caption = f"🎧 Audio version: {blog_data['title']}"
            msg_id = self.publish_audio(audio_path, caption=audio_caption, title=blog_data['title'])
            if msg_id:
                message_ids.append(msg_id)
        
        # 3. Send video if available
        video_path = blog_data.get('video_path')
        if video_path and os.path.exists(video_path):
            video_caption = f"🎥 Video version: {blog_data['title']}"
            msg_id = self.publish_video(video_path, caption=video_caption)
            if msg_id:
                message_ids.append(msg_id)
        
        logger.info(f"Published to Telegram: {len(message_ids)} messages sent")
        return message_ids
    
    def _is_configured(self):
        """Check if Telegram is properly configured"""
        if not self.bot_token or not self.channel_id:
            logger.error("Telegram not configured. Need TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID")
            return False
        return True
