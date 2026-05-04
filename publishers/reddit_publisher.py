"""
Reddit Publisher - Posts to Reddit using PRAW (free API)
Can post to relevant subreddits based on niche
"""

import praw
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RedditPublisher:
    """Publishes content to Reddit via PRAW"""
    
    def __init__(self):
        self.client_id = settings.REDDIT_CLIENT_ID
        self.client_secret = settings.REDDIT_CLIENT_SECRET
        self.username = settings.REDDIT_USERNAME
        self.password = settings.REDDIT_PASSWORD
        
        self.reddit = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize Reddit client with OAuth"""
        if not all([self.client_id, self.client_secret, self.username, self.password]):
            logger.warning("Reddit API credentials not fully configured")
            return
        
        try:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                username=self.username,
                password=self.password,
                user_agent='BlogAIAgent/1.0 (by /u/{})'.format(self.username)
            )
            
            # Test connection
            _ = self.reddit.user.me()
            logger.info("Reddit client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {str(e)}")
            self.reddit = None
    
    def publish_link_post(self, subreddit, title, url, comment=None):
        """
        Submit a link post to a subreddit
        Returns: Post URL if successful, None if failed
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return None
        
        logger.info(f"Posting to r/{subreddit}: {title[:50]}...")
        
        try:
            sub = self.reddit.subreddit(subreddit)
            
            # Submit link post
            submission = sub.submit(title=title[:300], url=url)  # Title limit: 300 chars
            
            # Add a comment if provided
            if comment:
                submission.reply(comment[:10000])  # Comment limit: 10000 chars
            
            post_url = f"https://reddit.com{submission.permalink}"
            logger.info(f"Reddit post successful: {post_url}")
            return post_url
            
        except Exception as e:
            logger.error(f"Failed to post to Reddit: {str(e)}")
            return None
    
    def publish_text_post(self, subreddit, title, text):
        """
        Submit a text (self) post to a subreddit
        Returns: Post URL if successful, None if failed
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return None
        
        logger.info(f"Posting text to r/{subreddit}: {title[:50]}...")
        
        try:
            sub = self.reddit.subreddit(subreddit)
            
            # Submit text post
            submission = sub.submit(title=title[:300], selftext=text[:40000])  # Text limit: 40000 chars
            
            post_url = f"https://reddit.com{submission.permalink}"
            logger.info(f"Reddit text post successful: {post_url}")
            return post_url
            
        except Exception as e:
            logger.error(f"Failed to post text to Reddit: {str(e)}")
            return None
    
    def publish_blog_post(self, blog_data, blog_url):
        """
        Publish blog post to relevant subreddits
        Automatically selects subreddits based on niche
        Returns: List of post URLs
        """
        if not self.reddit:
            return []
        
        logger.info(f"Publishing blog to Reddit: {blog_data['title']}")
        
        # Get relevant subreddits for niche
        from config.news_sources import get_subreddits_for_niche
        subreddits = get_subreddits_for_niche(settings.NICHE)
        
        post_urls = []
        
        # Post to first 2 subreddits (avoid spamming)
        for subreddit in subreddits[:2]:
            try:
                title = blog_data['title'][:300]
                
                # Create a Reddit-appropriate comment
                comment = f"**{blog_data.get('summary', '')}**\n\n"
                comment += f"Full article: {blog_url}\n\n"
                comment += "What are your thoughts on this? I'd love to hear your perspective!"
                
                url = self.publish_link_post(subreddit, title, blog_url, comment)
                
                if url:
                    post_urls.append(url)
                    
            except Exception as e:
                logger.error(f"Failed to post to r/{subreddit}: {str(e)}")
        
        logger.info(f"Posted to {len(post_urls)} subreddits")
        return post_urls
    
    def get_subreddit_info(self, subreddit):
        """Get information about a subreddit"""
        if not self.reddit:
            return None
        
        try:
            sub = self.reddit.subreddit(subreddit)
            return {
                'name': sub.display_name,
                'title': sub.title,
                'subscribers': sub.subscribers,
                'description': sub.public_description[:500]
            }
        except Exception as e:
            logger.error(f"Failed to get subreddit info: {str(e)}")
            return None
