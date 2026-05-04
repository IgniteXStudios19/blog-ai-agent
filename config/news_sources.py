"""
News Sources Configuration - RSS feeds and API configurations
Organized by niche/topic for easy customization
"""

# RSS Feeds by Niche
RSS_FEEDS = {
    'technology': [
        'https://techcrunch.com/feed/',
        'https://www.wired.com/feed/rss',
        'https://feeds.arstechnica.com/arstechnica/index',
        'https://www.theverge.com/rss/index.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
        'https://www.reddit.com/r/technology/.rss',
    ],
    'business': [
        'https://www.forbes.com/innovation/feed/',
        'https://feeds.bloomberg.com/markets/news/',
        'https://www.businessinsider.com/rss',
        'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
        'https://www.reddit.com/r/business/.rss',
    ],
    'science': [
        'https://www.sciencedaily.com/rss/all.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
        'https://www.newscientist.com/feed/home/?cmpid=RSS|NSNS|2012-GLOBAL|HOME',
        'https://www.reddit.com/r/science/.rss',
        'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    ],
    'health': [
        'https://www.who.int/rss-feeds/news-english.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Health.xml',
        'https://www.webmd.com/rss/webmd/news.xml',
        'https://www.medicalnewstoday.com/rss',
        'https://www.reddit.com/r/health/.rss',
    ],
    'general': [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://www.reuters.com/rssfeed/',
        'https://www.theguardian.com/uk/rss',
        'https://www.reddit.com/r/news/.rss',
    ],
}

# Google News RSS (no API key needed, completely free)
# Format: https://news.google.com/rss/search?q={TOPIC}&hl=en-US&gl=US&ceid=US:en
GOOGLE_NEWS_TOPICS = {
    'technology': 'technology',
    'business': 'business',
    'science': 'science',
    'health': 'health',
    'general': 'news',
}

# News API Configurations
NEWS_APIS = {
    'guardian': {
        'name': 'The Guardian',
        'base_url': 'https://content.guardianapis.com/search',
        'requires_key': True,
        'free_tier': 'Unlimited for developers',
        'sections': {
            'technology': 'technology',
            'business': 'business',
            'science': 'science',
            'general': 'world',
        }
    },
    'gnews': {
        'name': 'GNews',
        'base_url': 'https://gnews.io/api/v4/top-headlines',
        'requires_key': True,
        'free_tier': '100 requests/day',
        'categories': {
            'technology': 'technology',
            'business': 'business',
            'science': 'science',
            'health': 'health',
            'general': 'general',
        }
    },
    'newsapi': {
        'name': 'NewsAPI.org',
        'base_url': 'https://newsapi.org/v2/top-headlines',
        'requires_key': True,
        'free_tier': '100 requests/day',
        'categories': {
            'technology': 'technology',
            'business': 'business',
            'science': 'science',
            'health': 'health',
            'general': 'general',
        }
    },
}

# Reddit Subreddits to monitor by niche
REDDIT_SUBREDDITS = {
    'technology': ['technology', 'technews', 'gadgets', 'programming'],
    'business': ['business', 'investing', 'economics', 'entrepreneur'],
    'science': ['science', 'physics', 'biology', 'space'],
    'health': ['health', 'medicine', 'fitness', 'nutrition'],
    'general': ['news', 'worldnews', 'politics', 'upliftingnews'],
}

# News source credibility scores (higher = more credible)
SOURCE_CREDIBILITY = {
    'BBC': 10,
    'Reuters': 10,
    'The New York Times': 9,
    'The Guardian': 9,
    'TechCrunch': 8,
    'Wired': 8,
    'Ars Technica': 8,
    'The Verge': 7,
    'Forbes': 7,
    'Bloomberg': 9,
    'NASA': 10,
    'WHO': 10,
    'Science Daily': 8,
    'New Scientist': 8,
    'WebMD': 7,
    'Medical News Today': 6,
    'Reddit': 5,  # Lower credibility, but good for trends
}


def get_feeds_for_niche(niche):
    """Get all RSS feeds for a specific niche"""
    return RSS_FEEDS.get(niche, RSS_FEEDS['general'])


def get_subreddits_for_niche(niche):
    """Get Reddit subreddits for a specific niche"""
    return REDDIT_SUBREDDITS.get(niche, REDDIT_SUBREDDITS['general'])


def get_google_news_url(niche, limit=10):
    """Generate Google News RSS URL for a niche"""
    topic = GOOGLE_NEWS_TOPICS.get(niche, 'news')
    return f'https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en&num={limit}'
