"""
Main Orchestrator - Master controller for the Blog AI Agent
Runs the complete pipeline: Research → Write → Generate Audio/Video → Publish
"""

import os
import sys
import time
from datetime import datetime
from config.settings import settings
from config.news_sources import NEWS_APIS
from agents.news_researcher import NewsResearcher
from agents.content_writer import ContentWriter
from agents.audio_generator import AudioGenerator
from agents.video_creator import VideoCreator
from agents.social_formatter import SocialFormatter
from publishers.hashnode_publisher import HashnodePublisher
from publishers.telegram_publisher import TelegramPublisher
from publishers.twitter_publisher import TwitterPublisher
from publishers.linkedin_publisher import LinkedInPublisher
from publishers.reddit_publisher import RedditPublisher
from publishers.discord_publisher import DiscordPublisher
from publishers.mastodon_publisher import MastodonPublisher
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BlogAIAgent:
    """Main orchestrator class that runs the complete automation pipeline"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("=" * 60)
        logger.info("Blog AI Agent - Starting up...")
        logger.info("=" * 60)
        
        # Validate configuration
        errors = settings.validate_required_keys()
        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            sys.exit(1)
        
        # Print configuration status
        settings.print_status()
        
        # Initialize database
        self.db = DatabaseManager()
        logger.info("Database initialized")
        
        # Initialize agents
        self.news_researcher = NewsResearcher()
        self.news_researcher.db = self.db
        
        self.content_writer = ContentWriter()
        self.audio_generator = AudioGenerator()
        self.video_creator = VideoCreator()
        self.social_formatter = SocialFormatter()
        
        # Initialize publishers
        self.publishers = {
            'hashnode': HashnodePublisher(),
            'telegram': TelegramPublisher(),
            'twitter': TwitterPublisher(),
            'linkedin': LinkedInPublisher(),
            'reddit': RedditPublisher(),
            'discord': DiscordPublisher(),
            'mastodon': MastodonPublisher()
        }
        
        logger.info("All components initialized successfully")
    
    def run_pipeline(self):
        """Run the complete automation pipeline"""
        start_time = time.time()
        logger.info("\n" + "=" * 60)
        logger.info(f"Starting pipeline run at {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Statistics
        stats = {
            'news_fetched': 0,
            'posts_created': 0,
            'posts_published': 0,
            'errors': 0
        }
        
        try:
            # Stage 1: Fetch news
            logger.info("\n--- STAGE 1: FETCHING NEWS ---")
            news_items = self.news_researcher.fetch_all_news()
            stats['news_fetched'] = len(news_items)
            logger.info(f"Fetched {len(news_items)} top stories")
            
            if not news_items:
                logger.warning("No news items found. Exiting.")
                return
            
            # Process each news item
            for i, news_item in enumerate(news_items, 1):
                logger.info(f"\n{'=' * 60}")
                logger.info(f"PROCESSING STORY {i}/{len(news_items)}: {news_item['title'][:50]}...")
                logger.info("=" * 60)
                
                try:
                    # Stage 2: Extract full article
                    logger.info("\n--- STAGE 2: EXTRACTING FULL ARTICLE ---")
                    full_article = self.news_researcher.extract_full_article(news_item['url'])
                    
                    # Add to processed news
                    news_id = self.db.add_processed_news(
                        url=news_item['url'],
                        title=news_item['title'],
                        source=news_item['source'],
                        status='processing'
                    )
                    
                    # Stage 3: Generate blog post
                    logger.info("\n--- STAGE 3: GENERATING BLOG POST ---")
                    blog_data = self.content_writer.generate_blog_post(news_item, full_article)
                    
                    if not blog_data:
                        logger.error("Blog post generation failed")
                        self.db.update_news_status(news_item['url'], 'failed')
                        stats['errors'] += 1
                        continue
                    
                    # Save generated content to database
                    audio_path = None
                    video_path = None
                    
                    # Stage 4: Generate audio
                    logger.info("\n--- STAGE 4: GENERATING AUDIO ---")
                    audio_path = self.audio_generator.generate_audio_for_blog(blog_data)
                    if audio_path:
                        blog_data['audio_path'] = audio_path
                        logger.info(f"Audio generated: {audio_path}")
                    
                    # Stage 5: Generate video
                    logger.info("\n--- STAGE 5: GENERATING VIDEO ---")
                    video_path = self.video_creator.create_video(blog_data, audio_path)
                    if video_path:
                        blog_data['video_path'] = video_path
                        logger.info(f"Video generated: {video_path}")
                    
                    # Save to database
                    self.db.save_generated_content(
                        news_id=news_id,
                        blog_text=blog_data['content'],
                        social_text='',  # Will be filled when publishing
                        audio_path=audio_path,
                        video_path=video_path,
                        word_count=blog_data.get('word_count', 0),
                        quality_score=blog_data.get('quality_score', 0)
                    )
                    
                    # Stage 6: Publish to blog platform
                    logger.info("\n--- STAGE 6: PUBLISHING TO BLOG ---")
                    blog_url = None
                    
                    if self.publishers['hashnode'].api_key:
                        blog_url = self.publishers['hashnode'].publish(blog_data)
                        if blog_url:
                            self.db.add_published_content(
                                news_id=news_id,
                                blog_title=blog_data['title'],
                                blog_slug=blog_data.get('slug', ''),
                                platform='hashnode',
                                post_url=blog_url
                            )
                            stats['posts_published'] += 1
                            logger.info(f"Published to Hashnode: {blog_url}")
                    
                    # Stage 7: Publish to social media
                    logger.info("\n--- STAGE 7: PUBLISHING TO SOCIAL MEDIA ---")
                    
                    # Generate social posts
                    social_posts = self.content_writer.generate_social_posts(blog_data)
                    
                    # Publish to each platform
                    for platform, publisher in self.publishers.items():
                        if platform == 'hashnode':
                            continue  # Already published
                        
                        try:
                            if platform == 'telegram' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            elif platform == 'twitter' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            elif platform == 'linkedin' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            elif platform == 'reddit' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            elif platform == 'discord' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            elif platform == 'mastodon' and blog_url:
                                result = publisher.publish_blog_post(blog_data, blog_url)
                            else:
                                continue
                            
                            if result:
                                self.db.add_published_content(
                                    news_id=news_id,
                                    blog_title=blog_data['title'],
                                    blog_slug='',
                                    platform=platform,
                                    post_url=str(result) if result else ''
                                )
                                stats['posts_published'] += 1
                                
                        except Exception as e:
                            logger.error(f"Failed to publish to {platform}: {str(e)}")
                            stats['errors'] += 1
                    
                    # Update status
                    self.db.update_news_status(news_item['url'], 'published')
                    stats['posts_created'] += 1
                    
                    logger.info(f"\n✓ Completed processing story {i}")
                    
                except Exception as e:
                    logger.error(f"Error processing story: {str(e)}")
                    self.db.log_error(
                        phase='pipeline',
                        error_message=str(e),
                        news_url=news_item.get('url', '')
                    )
                    stats['errors'] += 1
                    continue
            
            # Update statistics
            today = datetime.now().strftime('%Y-%m-%d')
            self.db.update_statistics(
                date=today,
                posts_created=stats['posts_created'],
                posts_published=stats['posts_published'],
                errors_count=stats['errors']
            )
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            self.db.log_error(phase='main', error_message=str(e))
            stats['errors'] += 1
        
        # Print summary
        elapsed_time = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info("PIPELINE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"News fetched: {stats['news_fetched']}")
        logger.info(f"Posts created: {stats['posts_created']}")
        logger.info(f"Posts published: {stats['posts_published']}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info(f"Total time: {elapsed_time:.1f} seconds")
        logger.info("=" * 60)
        
        # Send Telegram notification if configured
        if self.publishers['telegram'].bot_token:
            try:
                summary_msg = f"✅ Blog AI Agent Run Complete!\n\n"
                summary_msg += f"News fetched: {stats['news_fetched']}\n"
                summary_msg += f"Posts created: {stats['posts_created']}\n"
                summary_msg += f"Posts published: {stats['posts_published']}\n"
                summary_msg += f"Errors: {stats['errors']}\n"
                summary_msg += f"Time: {elapsed_time:.1f}s"
                
                self.publishers['telegram'].publish_text(summary_msg)
            except:
                pass


def main():
    """Main entry point"""
    try:
        agent = BlogAIAgent()
        agent.run_pipeline()
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
