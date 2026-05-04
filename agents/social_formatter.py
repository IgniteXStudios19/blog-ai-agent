"""
Social Formatter Agent - Formats content for different social media platforms
Handles platform-specific requirements, character limits, and formatting
"""

import re
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SocialFormatter:
    """Formats blog content for various social media platforms"""
    
    def __init__(self):
        self.platform_limits = {
            'twitter': 280,
            'linkedin': 3000,
            'reddit_title': 300,
            'reddit_body': 40000,
            'telegram': 4096,
            'discord': 2000,
            'mastodon': 500
        }
    
    def format_for_twitter(self, blog_data, blog_url):
        """Format content for Twitter/X"""
        title = blog_data['title']
        summary = blog_data.get('summary', '')
        
        # Create tweet with hook
        hook = self._create_hook(title)
        
        # Add hashtags from tags
        hashtags = self._generate_hashtags(blog_data.get('tags', []), max_tags=3)
        
        # Build tweet
        tweet = f"{hook}\n\n{blog_url}"
        
        # Add hashtags if space allows
        if len(tweet) + len(hashtags) + 1 <= self.platform_limits['twitter']:
            tweet = f"{hook}\n\n{hashtags}\n\n{blog_url}"
        
        # Truncate if still too long
        if len(tweet) > self.platform_limits['twitter']:
            tweet = tweet[:self.platform_limits['twitter'] - 3] + "..."
        
        return tweet
    
    def format_for_linkedin(self, blog_data, blog_url):
        """Format content for LinkedIn"""
        title = blog_data['title']
        summary = blog_data.get('summary', '')
        key_points = blog_data.get('analysis', {}).get('key_points', [])
        
        # Build LinkedIn post
        post = f"🚀 {title}\n\n"
        post += f"{summary}\n\n"
        
        if key_points:
            post += "Key insights:\n"
            for i, point in enumerate(key_points[:3], 1):
                post += f"{i}. {point}\n"
            post += "\n"
        
        post += f"Read the full article: {blog_url}\n\n"
        post += "#" + " #".join(blog_data.get('tags', [])[:5])
        
        # Truncate if needed
        if len(post) > self.platform_limits['linkedin']:
            post = post[:self.platform_limits['linkedin'] - 3] + "..."
        
        return post
    
    def format_for_reddit(self, blog_data, subreddit):
        """Format content for Reddit"""
        title = blog_data['title']
        
        # Reddit titles should be catchy but not clickbaity
        if len(title) > self.platform_limits['reddit_title']:
            title = title[:self.platform_limits['reddit_title'] - 3] + "..."
        
        # Body text
        body = f"**{blog_data.get('summary', '')}**\n\n"
        body += f"Full article: {blog_url}\n\n"
        body += "What are your thoughts on this? I'd love to hear your perspective!"
        
        return {
            'title': title,
            'body': body,
            'subreddit': subreddit
        }
    
    def format_for_telegram(self, blog_data, blog_url):
        """Format content for Telegram (using HTML formatting)"""
        title = blog_data['title']
        summary = blog_data.get('summary', '')
        
        # Telegram supports HTML formatting
        message = f"<b>{self._escape_html(title)}</b>\n\n"
        message += f"{self._escape_html(summary)}\n\n"
        message += f"📖 <a href='{blog_url}'>Read full article</a>"
        
        # Truncate if needed
        if len(message) > self.platform_limits['telegram']:
            message = message[:self.platform_limits['telegram'] - 3] + "..."
        
        return message
    
    def format_for_discord(self, blog_data, blog_url, image_url=None):
        """Format content for Discord webhook (embed format)"""
        embed = {
            "title": blog_data['title'][:256],  # Discord embed title limit
            "description": blog_data.get('summary', '')[:2048],  # Discord description limit
            "url": blog_url,
            "color": 0x5865F2,  # Discord blurple
            "footer": {
                "text": f"Blog AI Agent | {settings.NICHE.title()} News"
            }
        }
        
        if image_url:
            embed["thumbnail"] = {"url": image_url}
        
        return {
            "embeds": [embed]
        }
    
    def format_for_mastodon(self, blog_data, blog_url):
        """Format content for Mastodon"""
        title = blog_data['title']
        summary = blog_data.get('summary', '')
        
        # Mastodon uses hashtags differently
        hashtags = self._generate_hashtags(blog_data.get('tags', []), max_tags=4)
        
        post = f"{title}\n\n{summary}\n\n{hashtags}\n\n{blog_url}"
        
        # Truncate if needed
        if len(post) > self.platform_limits['mastodon']:
            post = post[:self.platform_limits['mastodon'] - 3] + "..."
        
        return post
    
    def _create_hook(self, title):
        """Create an engaging hook for social posts"""
        hooks = [
            "📰 Latest update:",
            "🚨 Breaking:",
            "💡 Interesting development:",
            "🔥 Hot topic:",
            "Just published:"
        ]
        
        # Simple logic: pick hook based on title keywords
        title_lower = title.lower()
        if any(word in title_lower for word in ['new', 'launch', 'release']):
            return "🚀 Just launched:"
        elif any(word in title_lower for word in ['study', 'research', 'discover']):
            return "🔬 New research:"
        elif any(word in title_lower for word in ['update', 'change', 'announce']):
            return "📢 Important update:"
        else:
            return "📰 Latest news:"
    
    def _generate_hashtags(self, tags, max_tags=3):
        """Generate hashtags from tags"""
        if not tags:
            return ""
        
        hashtags = []
        for tag in tags[:max_tags]:
            # Clean tag for hashtag (remove spaces, special chars)
            clean_tag = re.sub(r'[^a-zA-Z0-9]', '', tag)
            if clean_tag:
                hashtags.append(f"#{clean_tag}")
        
        return " ".join(hashtags)
    
    def _escape_html(self, text):
        """Escape HTML special characters for Telegram"""
        text = text.replace('&', '&')
        text = text.replace('<', '<')
        text = text.replace('>', '>')
        return text
