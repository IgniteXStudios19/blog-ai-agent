"""
Test cases for Publishers
Run with: pytest tests/test_publishers.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from publishers.hashnode_publisher import HashnodePublisher
from publishers.telegram_publisher import TelegramPublisher
from publishers.twitter_publisher import TwitterPublisher
from publishers.linkedin_publisher import LinkedInPublisher
from publishers.reddit_publisher import RedditPublisher
from publishers.discord_publisher import DiscordPublisher
from publishers.mastodon_publisher import MastodonPublisher


class TestHashnodePublisher:
    """Test suite for HashnodePublisher"""
    
    @pytest.fixture
    def publisher(self):
        """Create a HashnodePublisher instance for testing"""
        with patch('publishers.hashnode_publisher.settings') as mock_settings:
            mock_settings.HASHNODE_API_KEY = 'test_key'
            mock_settings.HASHNODE_PUBLICATION_ID = 'test_pub_id'
            return HashnodePublisher()
    
    @patch('publishers.hashnode_publisher.requests.post')
    def test_publish_success(self, mock_post, publisher):
        """Test successful blog post publishing"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'publishPost': {
                    'post': {
                        'id': '123',
                        'title': 'Test',
                        'url': 'https://test.hashnode.dev/test'
                    }
                }
            }
        }
        mock_post.return_value = mock_response
        
        blog_data = {
            'title': 'Test Post',
            'content': '# Test\n\nContent here',
            'tags': ['test'],
            'meta_description': 'Test desc'
        }
        
        result = publisher.publish(blog_data)
        
        assert result == 'https://test.hashnode.dev/test'
        mock_post.assert_called_once()


class TestTelegramPublisher:
    """Test suite for TelegramPublisher"""
    
    @pytest.fixture
    def publisher(self):
        """Create a TelegramPublisher instance for testing"""
        with patch('publishers.telegram_publisher.settings') as mock_settings:
            mock_settings.TELEGRAM_BOT_TOKEN = 'test_token'
            mock_settings.TELEGRAM_CHANNEL_ID = '@test_channel'
            return TelegramPublisher()
    
    @patch('publishers.telegram_publisher.requests.post')
    def test_publish_text_success(self, mock_post, publisher):
        """Test successful text message sending"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'ok': True,
            'result': {'message_id': 123}
        }
        mock_post.return_value = mock_response
        
        result = publisher.publish_text('Test message')
        
        assert result == 123
        mock_post.assert_called_once()


class TestTwitterPublisher:
    """Test suite for TwitterPublisher"""
    
    @pytest.fixture
    def publisher(self):
        """Create a TwitterPublisher instance for testing"""
        with patch('publishers.twitter_publisher.settings') as mock_settings, \
             patch('publishers.twitter_publisher.tweepy.Client') as mock_client, \
             patch('publishers.twitter_publisher.tweepy.API') as mock_api:
            
            mock_settings.TWITTER_API_KEY = 'test_key'
            mock_settings.TWITTER_API_SECRET = 'test_secret'
            mock_settings.TWITTER_ACCESS_TOKEN = 'test_token'
            mock_settings.TWITTER_ACCESS_TOKEN_SECRET = 'test_secret'
            
            publisher = TwitterPublisher()
            publisher.client = mock_client.return_value
            publisher.api_v1 = mock_api.return_value
            return publisher
    
    def test_publish_text_success(self, publisher):
        """Test successful tweet posting"""
        mock_response = Mock()
        mock_response.data = {'id': '123456'}
        publisher.client.create_tweet.return_value = mock_response
        
        result = publisher.publish_text('Test tweet')
        
        assert result == '123456'
        publisher.client.create_tweet.assert_called_once()


class TestDiscordPublisher:
    """Test suite for DiscordPublisher"""
    
    @pytest.fixture
    def publisher(self):
        """Create a DiscordPublisher instance for testing"""
        with patch('publishers.discord_publisher.settings') as mock_settings:
            mock_settings.DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/test'
            return DiscordPublisher()
    
    @patch('publishers.discord_publisher.requests.post')
    def test_publish_text_success(self, mock_post, publisher):
        """Test successful Discord message sending"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = publisher.publish_text('Test message')
        
        assert result == True
        mock_post.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
