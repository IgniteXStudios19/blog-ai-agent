"""
Database Manager - Handles all SQLite database operations
Uses SQLAlchemy ORM for easy database interactions
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

Base = declarative_base()


class ProcessedNews(Base):
    """Table to track already processed news URLs"""
    __tablename__ = 'processed_news'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(500), unique=True, nullable=False)
    title = Column(String(500))
    source = Column(String(100))
    fetched_at = Column(DateTime)
    status = Column(String(50), default='pending')  # pending, processed, failed
    created_at = Column(DateTime, default=datetime.now)


class PublishedContent(Base):
    """Table to track all published content"""
    __tablename__ = 'published_content'
    
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer)
    blog_title = Column(String(500))
    blog_slug = Column(String(200))
    platform = Column(String(50))  # hashnode, telegram, twitter, etc.
    published_at = Column(DateTime)
    post_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)


class GeneratedContent(Base):
    """Table to store generated content (blog, social, audio, video)"""
    __tablename__ = 'generated_content'
    
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer)
    blog_text = Column(Text)
    social_text = Column(Text)
    audio_path = Column(String(500))
    video_path = Column(String(500))
    word_count = Column(Integer)
    quality_score = Column(Float)
    created_at = Column(DateTime, default=datetime.now)


class ErrorLog(Base):
    """Table to log all errors for debugging"""
    __tablename__ = 'error_logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    phase = Column(String(100))  # news_research, content_writing, etc.
    error_message = Column(Text)
    news_url = Column(String(500))
    stack_trace = Column(Text)


class Statistics(Base):
    """Table to track daily statistics"""
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(10))  # YYYY-MM-DD
    posts_created = Column(Integer, default=0)
    posts_published = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    api_calls = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class DatabaseManager:
    """Main database manager class"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = settings.DATABASE_PATH
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create engine and session
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        logger.info(f"Database initialized at: {db_path}")
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    # ========== PROCESSED NEWS METHODS ==========
    
    def is_url_processed(self, url):
        """Check if a URL has already been processed"""
        session = self.get_session()
        try:
            result = session.query(ProcessedNews).filter_by(url=url).first()
            return result is not None
        finally:
            session.close()
    
    def add_processed_news(self, url, title, source, status='pending'):
        """Add a news URL to processed list"""
        session = self.get_session()
        try:
            news = ProcessedNews(
                url=url,
                title=title,
                source=source,
                fetched_at=datetime.now(),
                status=status
            )
            session.add(news)
            session.commit()
            return news.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding processed news: {str(e)}")
            return None
        finally:
            session.close()
    
    def update_news_status(self, url, status):
        """Update the status of a processed news item"""
        session = self.get_session()
        try:
            news = session.query(ProcessedNews).filter_by(url=url).first()
            if news:
                news.status = status
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating news status: {str(e)}")
        finally:
            session.close()
    
    # ========== PUBLISHED CONTENT METHODS ==========
    
    def add_published_content(self, news_id, blog_title, blog_slug, platform, post_url):
        """Record a published content item"""
        session = self.get_session()
        try:
            content = PublishedContent(
                news_id=news_id,
                blog_title=blog_title,
                blog_slug=blog_slug,
                platform=platform,
                published_at=datetime.now(),
                post_url=post_url
            )
            session.add(content)
            session.commit()
            return content.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding published content: {str(e)}")
            return None
        finally:
            session.close()
    
    def is_already_published(self, news_id, platform):
        """Check if content was already published to a platform"""
        session = self.get_session()
        try:
            result = session.query(PublishedContent).filter_by(
                news_id=news_id,
                platform=platform
            ).first()
            return result is not None
        finally:
            session.close()
    
    # ========== GENERATED CONTENT METHODS ==========
    
    def save_generated_content(self, news_id, blog_text, social_text=None, 
                               audio_path=None, video_path=None, 
                               word_count=0, quality_score=0):
        """Save generated content to database"""
        session = self.get_session()
        try:
            content = GeneratedContent(
                news_id=news_id,
                blog_text=blog_text,
                social_text=social_text,
                audio_path=audio_path,
                video_path=video_path,
                word_count=word_count,
                quality_score=quality_score
            )
            session.add(content)
            session.commit()
            return content.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving generated content: {str(e)}")
            return None
        finally:
            session.close()
    
    # ========== ERROR LOGGING METHODS ==========
    
    def log_error(self, phase, error_message, news_url=None, stack_trace=None):
        """Log an error to database"""
        session = self.get_session()
        try:
            error = ErrorLog(
                phase=phase,
                error_message=error_message,
                news_url=news_url,
                stack_trace=stack_trace
            )
            session.add(error)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error logging error: {str(e)}")
        finally:
            session.close()
    
    # ========== STATISTICS METHODS ==========
    
    def update_statistics(self, date=None, **kwargs):
        """Update daily statistics"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        session = self.get_session()
        try:
            stats = session.query(Statistics).filter_by(date=date).first()
            if not stats:
                stats = Statistics(date=date)
                session.add(stats)
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(stats, key):
                    setattr(stats, key, value)
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating statistics: {str(e)}")
        finally:
            session.close()
    
    def get_statistics(self, date=None):
        """Get statistics for a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        session = self.get_session()
        try:
            stats = session.query(Statistics).filter_by(date=date).first()
            if stats:
                return {
                    'date': stats.date,
                    'posts_created': stats.posts_created,
                    'posts_published': stats.posts_published,
                    'errors_count': stats.errors_count,
                    'api_calls': stats.api_calls
                }
            return None
        finally:
            session.close()
    
    # ========== CLEANUP METHODS ==========
    
    def cleanup_old_data(self, days=30):
        """Clean up data older than specified days"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Delete old error logs
            session.query(ErrorLog).filter(ErrorLog.timestamp < cutoff_date).delete()
            
            # Delete old processed news
            session.query(ProcessedNews).filter(ProcessedNews.fetched_at < cutoff_date).delete()
            
            session.commit()
            logger.info(f"Cleaned up data older than {days} days")
        except Exception as e:
            session.rollback()
            logger.error(f"Error during cleanup: {str(e)}")
        finally:
            session.close()
