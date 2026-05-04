"""
News Researcher Agent - Fetches and analyzes news from multiple free sources
This agent handles: RSS feeds, News APIs, Reddit trends, Google News
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime, timedelta
import time
from config.settings import settings
from config.news_sources import (
    get_feeds_for_niche, 
    get_subreddits_for_niche, 
    GOOGLE_NEWS_TOPICS,
    NEWS_APIS,
    SOURCE_CREDIBILITY
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


class NewsResearcher:
    """Fetches news from multiple free sources and selects top stories"""
    
    def __init__(self):
        self.news_items = []
        self.db = None  # Will be set by main orchestrator
        
    def fetch_all_news(self, niche=None):
        """Fetch news from all configured sources"""
        if niche is None:
            niche = settings.NICHE
            
        logger.info(f"Starting news research for niche: {niche}")
        
        # Fetch from all sources
        self._fetch_rss_feeds(niche)
        self._fetch_google_news(niche)
        self._fetch_news_api(niche)
        self._fetch_reddit_trends(niche)
        
        # Score and select top stories
        self._score_news_items()
        top_stories = self._select_top_stories(settings.POSTS_PER_RUN)
        
        logger.info(f"Found {len(top_stories)} top stories to process")
        return top_stories
    
    def _fetch_rss_feeds(self, niche):
        """Fetch news from RSS feeds (completely free, no API key needed)"""
        logger.info("Fetching RSS feeds...")
        feeds = get_feeds_for_niche(niche)
        
        for feed_url in feeds:
            try:
                logger.debug(f"Parsing feed: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:  # Limit per feed
                    # Skip if already processed
                    if self.db and self.db.is_url_processed(entry.link):
                        continue
                        
                    news_item = {
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'summary': entry.get('summary', ''),
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', 'Unknown RSS Source'),
                        'source_type': 'rss',
                        'credibility_score': SOURCE_CREDIBILITY.get(
                            feed.feed.get('title', ''), 5
                        ),
                        'fetched_at': datetime.now().isoformat()
                    }
                    self.news_items.append(news_item)
                    
                time.sleep(0.5)  # Be nice to servers
                
            except Exception as e:
                logger.error(f"Error fetching RSS feed {feed_url}: {str(e)}")
                
        logger.info(f"RSS feeds: Got {len([n for n in self.news_items if n['source_type']=='rss'])} items")
    
    def _fetch_google_news(self, niche):
        """Fetch from Google News RSS (completely free, no API key)"""
        logger.info("Fetching Google News...")
        try:
            topic = GOOGLE_NEWS_TOPICS.get(niche, 'news')
            url = f"https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
            
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:15]:
                if self.db and self.db.is_url_processed(entry.link):
                    continue
                    
                news_item = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': 'Google News',
                    'source_type': 'google_news',
                    'credibility_score': 8,  # Google aggregates credible sources
                    'fetched_at': datetime.now().isoformat()
                }
                self.news_items.append(news_item)
                
            logger.info(f"Google News: Got {len([n for n in self.news_items if n['source_type']=='google_news'])} items")
            
        except Exception as e:
            logger.error(f"Error fetching Google News: {str(e)}")
    
    def _fetch_news_api(self, niche):
        """Fetch from free News APIs (Guardian, GNews, NewsAPI)"""
        logger.info("Fetching from News APIs...")
        
        # The Guardian API (completely free, unlimited)
        if settings.GUARDIAN_API_KEY:
            self._fetch_guardian(niche)
            
        # GNews API (100 requests/day free)
        if settings.GNEWS_API_KEY:
            self._fetch_gnews(niche)
            
        # NewsAPI.org (100 requests/day free)
        if settings.NEWSAPI_KEY:
            self._fetch_newsapi(niche)
    
    def _fetch_guardian(self, niche):
        """Fetch from The Guardian API (free, unlimited)"""
        try:
            section = NEWS_APIS['guardian']['sections'].get(niche, 'world')
            url = f"{NEWS_APIS['guardian']['base_url']}"
            params = {
                'section': section,
                'api-key': settings.GUARDIAN_API_KEY,
                'page-size': 10,
                'show-fields': 'headline,shortUrl,trailText'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get('response', {}).get('results', [])
                
                for item in results:
                    url = item.get('webUrl', '')
                    if self.db and self.db.is_url_processed(url):
                        continue
                        
                    news_item = {
                        'title': item.get('fields', {}).get('headline', item.get('webTitle', '')),
                        'url': url,
                        'summary': item.get('fields', {}).get('trailText', ''),
                        'published': item.get('webPublicationDate', ''),
                        'source': 'The Guardian',
                        'source_type': 'guardian_api',
                        'credibility_score': SOURCE_CREDIBILITY['The Guardian'],
                        'fetched_at': datetime.now().isoformat()
                    }
                    self.news_items.append(news_item)
                    
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            logger.error(f"Error fetching The Guardian: {str(e)}")
    
    def _fetch_gnews(self, niche):
        """Fetch from GNews API (100 requests/day free)"""
        try:
            category = NEWS_APIS['gnews']['categories'].get(niche, 'general')
            url = f"{NEWS_APIS['gnews']['base_url']}"
            params = {
                'category': category,
                'apikey': settings.GNEWS_API_KEY,
                'max': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                for article in articles:
                    url = article.get('url', '')
                    if self.db and self.db.is_url_processed(url):
                        continue
                        
                    news_item = {
                        'title': article.get('title', ''),
                        'url': url,
                        'summary': article.get('description', ''),
                        'published': article.get('published_date', ''),
                        'source': article.get('source', {}).get('name', 'GNews'),
                        'source_type': 'gnews_api',
                        'credibility_score': 6,
                        'fetched_at': datetime.now().isoformat()
                    }
                    self.news_items.append(news_item)
                    
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error fetching GNews: {str(e)}")
    
    def _fetch_newsapi(self, niche):
        """Fetch from NewsAPI.org (100 requests/day free)"""
        try:
            category = NEWS_APIS['newsapi']['categories'].get(niche, 'general')
            url = f"{NEWS_APIS['newsapi']['base_url']}"
            params = {
                'category': category,
                'apiKey': settings.NEWSAPI_KEY,
                'pageSize': 10,
                'language': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                for article in articles:
                    url = article.get('url', '')
                    if self.db and self.db.is_url_processed(url):
                        continue
                        
                    news_item = {
                        'title': article.get('title', ''),
                        'url': url,
                        'summary': article.get('description', ''),
                        'published': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'NewsAPI'),
                        'source_type': 'newsapi_org',
                        'credibility_score': 7,
                        'fetched_at': datetime.now().isoformat()
                    }
                    self.news_items.append(news_item)
                    
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error fetching NewsAPI.org: {str(e)}")
    
    def _fetch_reddit_trends(self, niche):
        """Fetch trending posts from Reddit (free API)"""
        logger.info("Fetching Reddit trends...")
        
        if not all([settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET, 
                   settings.REDDIT_USERNAME, settings.REDDIT_PASSWORD]):
            logger.warning("Reddit API credentials not configured, skipping")
            return
            
        try:
            reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                username=settings.REDDIT_USERNAME,
                password=settings.REDDIT_PASSWORD,
                user_agent='BlogAIAgent/1.0'
            )
            
            subreddits = get_subreddits_for_niche(niche)
            
            for subreddit_name in subreddits:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    hot_posts = subreddit.hot(limit=5)
                    
                    for post in hot_posts:
                        # Only consider posts with good engagement
                        if post.score < 50:  # Skip low-scoring posts
                            continue
                            
                        url = f"https://reddit.com{post.permalink}"
                        if self.db and self.db.is_url_processed(url):
                            continue
                            
                        news_item = {
                            'title': post.title,
                            'url': url,
                            'summary': post.selftext[:500] if post.selftext else '',
                            'published': datetime.fromtimestamp(post.created_utc).isoformat(),
                            'source': f'Reddit r/{subreddit_name}',
                            'source_type': 'reddit',
                            'credibility_score': SOURCE_CREDIBILITY['Reddit'],
                            'reddit_score': post.score,
                            'reddit_comments': post.num_comments,
                            'fetched_at': datetime.now().isoformat()
                        }
                        self.news_items.append(news_item)
                        
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error fetching subreddit {subreddit_name}: {str(e)}")
                    
            logger.info(f"Reddit: Got {len([n for n in self.news_items if n['source_type']=='reddit'])} items")
            
        except Exception as e:
            logger.error(f"Error initializing Reddit API: {str(e)}")
    
    def _score_news_items(self):
        """Score news items by relevance, recency, and credibility"""
        logger.info("Scoring news items...")
        
        now = datetime.now()
        
        for item in self.news_items:
            score = 0
            
            # Credibility score (0-10)
            score += item.get('credibility_score', 5) * 2  # Weight: 0-20
            
            # Recency score (newer = higher)
            try:
                if 'published' in item and item['published']:
                    # Try to parse date (handles multiple formats)
                    pub_date = None
                    for fmt in ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ', 
                                 '%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%d']:
                        try:
                            pub_date = datetime.strptime(item['published'][:19], fmt)
                            break
                        except:
                            continue
                            
                    if pub_date:
                        hours_ago = (now - pub_date).total_seconds() / 3600
                        if hours_ago < 6:
                            score += 20
                        elif hours_ago < 24:
                            score += 15
                        elif hours_ago < 48:
                            score += 10
                        else:
                            score += 5
            except:
                score += 5  # Default if date parsing fails
                
            # Reddit engagement (if from Reddit)
            if item.get('source_type') == 'reddit':
                score += min(item.get('reddit_score', 0) / 100, 10)  # Up to 10 points
                score += min(item.get('reddit_comments', 0) / 20, 5)  # Up to 5 points
                
            # Multiple sources reporting (sign of trending)
            title_keywords = set(item['title'].lower().split()[:5])  # First 5 words
            same_story_count = 0
            for other in self.news_items:
                if other['url'] != item['url']:
                    other_keywords = set(other['title'].lower().split()[:5])
                    if len(title_keywords.intersection(other_keywords)) >= 3:
                        same_story_count += 1
                        
            score += same_story_count * 5  # 5 points per additional source
            
            item['trending_score'] = score
            
        # Sort by score (highest first)
        self.news_items.sort(key=lambda x: x.get('trending_score', 0), reverse=True)
    
    def _select_top_stories(self, count):
        """Select top N unique stories"""
        selected = []
        seen_titles = set()
        
        for item in self.news_items:
            # Skip if title is too similar to already selected
            title_words = set(item['title'].lower().split()[:5])
            is_duplicate = False
            
            for selected_item in selected:
                selected_words = set(selected_item['title'].lower().split()[:5])
                if len(title_words.intersection(selected_words)) >= 4:
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                selected.append(item)
                if len(selected) >= count:
                    break
                    
        return selected
    
    def extract_full_article(self, url):
        """Extract full article text using newspaper3k (free, no API needed)"""
        logger.info(f"Extracting full article: {url}")
        
        try:
            from newspaper import Article
            
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'summary': article.summary if hasattr(article, 'summary') else ''
            }
            
        except Exception as e:
            logger.error(f"Error extracting article with newspaper3k: {str(e)}")
            
            # Fallback to BeautifulSoup
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                    
                # Get text
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return {
                    'title': soup.title.string if soup.title else '',
                    'text': text[:5000],  # Limit to 5000 chars
                    'authors': [],
                    'publish_date': None,
                    'top_image': '',
                    'summary': ''
                }
                
            except Exception as e2:
                logger.error(f"BeautifulSoup fallback also failed: {str(e2)}")
                return None
