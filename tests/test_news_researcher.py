"""
Test cases for News Researcher Agent
Run with: pytest tests/test_news_researcher.py -v
"""

import pytest
from unittest.mock import Mock, patch
from agents.news_researcher import NewsResearcher
from config.settings import settings


class TestNewsResearcher:
    """Test suite for NewsResearcher agent"""
    
    @pytest.fixture
    def researcher(self):
        """Create a NewsResearcher instance for testing"""
        return NewsResearcher()
    
    def test_initialization(self, researcher):
        """Test that NewsResearcher initializes correctly"""
        assert researcher is not None
        assert hasattr(researcher, 'news_items')
        assert isinstance(researcher.news_items, list)
        assert len(researcher.news_items) == 0
    
    @patch('agents.news_researcher.feedparser.parse')
    def test_rss_feed_fetch(self, mock_parse, researcher):
        """Test RSS feed fetching with mocked response"""
        # Mock feedparser response
        mock_parse.return_value = {
            'feed': {'title': 'Test Feed'},
            'entries': [
                {
                    'title': 'Test News 1',
                    'link': 'https://example.com/news1',
                    'summary': 'Test summary',
                    'published': '2026-05-03T10:00:00Z'
                }
            ]
        }
        
        # Mock database
        researcher.db = Mock()
        researcher.db.is_url_processed.return_value = False
        
        # Test fetching
        researcher._fetch_rss_feeds('technology')
        
        assert len(researcher.news_items) > 0
        assert researcher.news_items[0]['title'] == 'Test News 1'
        assert researcher.news_items[0]['source_type'] == 'rss'
    
    def test_score_news_items(self, researcher):
        """Test news scoring algorithm"""
        researcher.news_items = [
            {
                'title': 'Test News',
                'source': 'The Guardian',
                'source_type': 'rss',
                'published': '2026-05-03T10:00:00Z'
            }
        ]
        
        researcher._score_news_items()
        
        assert 'trending_score' in researcher.news_items[0]
        assert researcher.news_items[0]['trending_score'] > 0
    
    def test_select_top_stories(self, researcher):
        """Test selection of top stories"""
        researcher.news_items = [
            {'title': 'News 1', 'trending_score': 10},
            {'title': 'News 2', 'trending_score': 8},
            {'title': 'News 3', 'trending_score': 6},
            {'title': 'News 4', 'trending_score': 4}
        ]
        
        top_stories = researcher._select_top_stories(2)
        
        assert len(top_stories) == 2
        assert top_stories[0]['title'] == 'News 1'
        assert top_stories[1]['title'] == 'News 2'
    
    @patch('agents.news_researcher.requests.get')
    def test_google_news_fetch(self, mock_get, researcher):
        """Test Google News fetching"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'''<?xml version="1.0"?>
        <rss>
            <channel>
                <item>
                    <title>Google News Test</title>
                    <link>https://example.com/google-news</link>
                    <pubDate>2026-05-03</pubDate>
                </item>
            </channel>
        </rss>'''
        mock_get.return_value = mock_response
        
        researcher._fetch_google_news('technology')
        
        # Check if any news was added
        google_news_items = [n for n in researcher.news_items if n['source_type'] == 'google_news']
        assert len(google_news_items) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
