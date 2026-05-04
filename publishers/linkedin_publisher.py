"""
LinkedIn Publisher - Posts to LinkedIn using free API
Requires OAuth 2.0 access token (manual setup once)
"""

import requests
import json
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LinkedInPublisher:
    """Publishes content to LinkedIn via API"""
    
    def __init__(self):
        self.access_token = settings.LINKEDIN_ACCESS_TOKEN
        self.base_url = 'https://api.linkedin.com/v2'
        
        if not self.access_token:
            logger.warning("LinkedIn access token not configured")
    
    def publish_text(self, text, visibility='PUBLIC'):
        """
        Post text to LinkedIn personal profile
        visibility: PUBLIC, CONNECTIONS, or LOGGED_IN
        Returns: Post ID if successful, None if failed
        """
        if not self.access_token:
            logger.error("LinkedIn not configured. Need LINKEDIN_ACCESS_TOKEN")
            return None
        
        logger.info("Posting to LinkedIn...")
        
        # Get user's ID first
        user_id = self._get_user_id()
        if not user_id:
            return None
        
        # Prepare post data
        post_data = {
            'author': f'urn:li:person:{user_id}',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': text[:1300]  # LinkedIn text limit
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': visibility
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/ugcPosts',
                headers=headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                post_id = result.get('id', '')
                logger.info(f"LinkedIn post successful (ID: {post_id})")
                return post_id
            else:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {str(e)}")
            return None
    
    def publish_with_link(self, text, url, title=None, description=None):
        """
        Post with a link preview to LinkedIn
        Returns: Post ID if successful, None if failed
        """
        if not self.access_token:
            logger.error("LinkedIn not configured")
            return None
        
        logger.info("Posting to LinkedIn with link...")
        
        user_id = self._get_user_id()
        if not user_id:
            return None
        
        # Prepare post with link
        post_data = {
            'author': f'urn:li:person:{user_id}',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': text[:1300]
                    },
                    'shareMediaCategory': 'ARTICLE',
                    'media': [{
                        'status': 'READY',
                        'originalUrl': url,
                        'title': title or '',
                        'description': description or ''
                    }]
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/ugcPosts',
                headers=headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                post_id = result.get('id', '')
                logger.info(f"LinkedIn post with link successful (ID: {post_id})")
                return post_id
            else:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {str(e)}")
            return None
    
    def publish_blog_post(self, blog_data, blog_url):
        """Publish blog post to LinkedIn"""
        if not self.access_token:
            return None
        
        logger.info(f"Publishing blog to LinkedIn: {blog_data['title']}")
        
        # Create LinkedIn post text
        text = f"{blog_data['title']}\n\n"
        text += f"{blog_data.get('summary', '')[:500]}\n\n"
        text += "Read the full article for more insights!"
        
        return self.publish_with_link(
            text=text,
            url=blog_url,
            title=blog_data['title'],
            description=blog_data.get('meta_description', '')
        )
    
    def _get_user_id(self):
        """Get the LinkedIn user ID from access token"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/userinfo',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('sub', '')  # 'sub' is the user ID
            else:
                logger.error(f"Failed to get LinkedIn user ID: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting LinkedIn user ID: {str(e)}")
            return None
