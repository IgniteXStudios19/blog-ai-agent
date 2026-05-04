"""
Twitter/X Publisher - Posts to Twitter/X using free basic API
Free tier: 1500 tweets/month, read/write access
"""

import tweepy
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TwitterPublisher:
    """Publishes content to Twitter/X via Tweepy"""
    
    def __init__(self):
        self.api_key = settings.TWITTER_API_KEY
        self.api_secret = settings.TWITTER_API_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize Tweepy client with OAuth 1.0a"""
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            logger.warning("Twitter API credentials not fully configured")
            return
        
        try:
            # For API v2 (newer, required for free tier)
            self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            
            # For media upload (API v1.1 needed)
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api_v1 = tweepy.API(auth)
            
            logger.info("Twitter client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            self.client = None
    
    def publish_text(self, text):
        """
        Post a text-only tweet
        Returns: Tweet ID if successful, None if failed
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return None
        
        logger.info("Posting tweet...")
        
        # Truncate if too long
        if len(text) > 280:
            text = text[:277] + "..."
        
        try:
            response = self.client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"Tweet posted successfully (ID: {tweet_id})")
                return tweet_id
            else:
                logger.error("No data in Twitter response")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            return None
    
    def publish_with_image(self, text, image_path):
        """
        Post a tweet with an image
        Returns: Tweet ID if successful, None if failed
        """
        if not self.client or not hasattr(self, 'api_v1'):
            logger.error("Twitter client not properly initialized")
            return None
        
        logger.info(f"Posting tweet with image: {image_path}")
        
        try:
            # Upload image using API v1.1
            media = self.api_v1.media_upload(image_path)
            media_id = media.media_id_string
            
            # Post tweet with media using API v2
            response = self.client.create_tweet(
                text=text[:280],
                media_ids=[media_id]
            )
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"Tweet with image posted (ID: {tweet_id})")
                return tweet_id
            else:
                logger.error("No data in Twitter response")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post tweet with image: {str(e)}")
            return None
    
    def publish_blog_post(self, blog_data, blog_url):
        """
        Publish blog post to Twitter
        Sends: Tweet with link + optional image
        """
        if not self.client:
            return None
        
        logger.info(f"Publishing blog to Twitter: {blog_data['title']}")
        
        # Create tweet text
        title = blog_data['title']
        hashtags = self._generate_hashtags(blog_data.get('tags', []))
        
        # Format: Title + URL + hashtags
        text = f"{title[:100]}...\n\n{blog_url}\n\n{hashtags}"
        
        # Truncate if needed
        if len(text) > 280:
            title_max = 280 - len(blog_url) - len(hashtags) - 10
            text = f"{title[:title_max]}...\n\n{blog_url}\n\n{hashtags}"
        
        # Try to include image if available
        image_path = blog_data.get('cover_image', '')
        if image_path and os.path.exists(image_path):
            return self.publish_with_image(text, image_path)
        else:
            return self.publish_text(text)
    
    def _generate_hashtags(self, tags, max_tags=3):
        """Generate hashtags from tags"""
        if not tags:
            return "#news #technology"
        
        hashtags = []
        for tag in tags[:max_tags]:
            # Clean tag for hashtag
            clean_tag = ''.join(c for c in tag if c.isalnum() or c.isspace())
            clean_tag = clean_tag.replace(' ', '')
            if clean_tag:
                hashtags.append(f"#{clean_tag}")
        
        return ' '.join(hashtags) if hashtags else "#news"
    
    def get_remaining_tweets(self):
        """Check how many tweets remaining this month (free tier: 1500/month)"""
        # Note: This requires additional API calls that may count toward rate limits
        # For simplicity, we'll skip this in the free implementation
        return 1500  # Assume full quota
