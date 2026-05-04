"""
Mastodon Publisher - Posts to Mastodon (free, open-source social media)
No approval needed, unlimited posts, growing platform
"""

import requests
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MastodonPublisher:
    """Publishes content to Mastodon via API"""
    
    def __init__(self):
        self.access_token = settings.MASTODON_ACCESS_TOKEN
        self.api_base_url = settings.MASTODON_API_BASE_URL
        self.api_url = f'{self.api_base_url}/api/v1'
        
        if not self.access_token:
            logger.warning("Mastodon access token not configured")
        if not self.api_base_url:
            logger.warning("Mastodon API base URL not configured")
    
    def publish_text(self, text):
        """
        Post text to Mastodon
        Returns: Post ID if successful, None if failed
        """
        if not self._is_configured():
            return None
        
        logger.info("Posting to Mastodon...")
        
        # Truncate if too long (Mastodon limit: 500 chars)
        if len(text) > 500:
            text = text[:497] + "..."
        
        url = f'{self.api_url}/statuses'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'status': text,
            'visibility': 'public'  # public, unlisted, private, direct
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                post_id = data.get('id', '')
                logger.info(f"Mastodon post successful (ID: {post_id})")
                return post_id
            else:
                logger.error(f"Mastodon API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post to Mastodon: {str(e)}")
            return None
    
    def publish_with_media(self, text, media_path):
        """
        Post with media attachment to Mastodon
        Returns: Post ID if successful, None if failed
        """
        if not self._is_configured():
            return None
        
        logger.info(f"Posting to Mastodon with media: {media_path}")
        
        # First upload media
        media_id = self._upload_media(media_path)
        if not media_id:
            return None
        
        # Then post with media
        url = f'{self.api_url}/statuses'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'status': text[:500],
            'media_ids': [media_id],
            'visibility': 'public'
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                post_id = data.get('id', '')
                logger.info(f"Mastodon post with media successful (ID: {post_id})")
                return post_id
            else:
                logger.error(f"Mastodon API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post to Mastodon with media: {str(e)}")
            return None
    
    def _upload_media(self, media_path):
        """Upload media file to Mastodon"""
        url = f'{self.api_url}/media'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        try:
            with open(media_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, headers=headers, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('id')
            else:
                logger.error(f"Media upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to upload media: {str(e)}")
            return None
    
    def publish_blog_post(self, blog_data, blog_url):
        """
        Publish blog post to Mastodon
        Sends: Text with link + optional image
        """
        if not self._is_configured():
            return None
        
        logger.info(f"Publishing blog to Mastodon: {blog_data['title']}")
        
        # Create Mastodon post text
        title = blog_data['title']
        hashtags = self._generate_hashtags(blog_data.get('tags', []))
        
        # Format: Title + URL + hashtags (within 500 chars)
        text = f"{title}\n\n{blog_url}\n\n{hashtags}"
        
        if len(text) > 500:
            # Truncate title
            max_title = 500 - len(blog_url) - len(hashtags) - 10
            text = f"{title[:max_title]}...\n\n{blog_url}\n\n{hashtags}"
        
        # Try to include image if available
        image_path = blog_data.get('cover_image', '')
        if image_path and os.path.exists(image_path):
            return self.publish_with_media(text, image_path)
        else:
            return self.publish_text(text)
    
    def _generate_hashtags(self, tags, max_tags=3):
        """Generate hashtags for Mastodon (different style than Twitter)"""
        if not tags:
            return '#news #technology'
        
        hashtags = []
        for tag in tags[:max_tags]:
            # Clean tag for hashtag
            clean_tag = ''.join(c for c in tag if c.isalnum() or c.isspace())
            clean_tag = clean_tag.replace(' ', '')
            if clean_tag:
                hashtags.append(f"#{clean_tag}")
        
        return ' '.join(hashtags) if hashtags else '#news'
    
    def get_account_info(self):
        """Get information about the authenticated account"""
        if not self._is_configured():
            return None
        
        url = f'{self.api_url}/accounts/verify_credentials'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get account info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return None
    
    def _is_configured(self):
        """Check if Mastodon is properly configured"""
        if not self.access_token or not self.api_base_url:
            logger.error("Mastodon not configured. Need MASTODON_ACCESS_TOKEN and MASTODON_API_BASE_URL")
            return False
        return True
