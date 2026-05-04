"""
Test cases for Content Writer Agent
Run with: pytest tests/test_content_writer.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.content_writer import ContentWriter
from config.settings import settings


class TestContentWriter:
    """Test suite for ContentWriter agent"""
    
    @pytest.fixture
    def writer(self):
        """Create a ContentWriter instance for testing"""
        with patch('agents.content_writer.Groq') as mock_groq, \
             patch('agents.content_writer.genai') as mock_genai:
            
            # Mock Groq client
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '{"test": "response"}'
            mock_client.chat.completions.create.return_value = mock_response
            mock_groq.return_value = mock_client
            
            writer = ContentWriter()
            writer.primary_client = mock_client
            writer.fallback_client = None
            yield writer
    
    def test_initialization(self, writer):
        """Test that ContentWriter initializes correctly"""
        assert writer is not None
        assert hasattr(writer, 'primary_client')
        assert hasattr(writer, 'text_cleaner')
    
    @patch('agents.content_writer.ContentWriter._call_ai')
    def test_analyze_news(self, mock_call_ai, writer):
        """Test news analysis with AI"""
        mock_call_ai.return_value = '{"main_topic": "AI", "key_points": ["Point 1"], "seo_keywords": ["AI"]}'
        
        news_item = {
            'title': 'Test News',
            'summary': 'Test summary',
            'source': 'Test Source',
            'published': '2026-05-03'
        }
        
        result = writer._analyze_news(news_item)
        
        assert result is not None
        assert 'main_topic' in result
    
    @patch('agents.content_writer.ContentWriter._call_ai')
    def test_generate_blog_post(self, mock_call_ai, writer):
        """Test full blog post generation"""
        # Mock AI responses
        mock_call_ai.side_effect = [
            '{"main_topic": "Test", "key_points": ["Point 1"], "seo_keywords": ["test"]}',
            'Blog outline here',
            '# Test Title\n\nBlog content here',
            '# Test Title\n\nHumanized content',
            '{"meta_title": "Test", "meta_description": "Desc", "slug": "test", "tags": ["test"]}',
            '{"word_count": 500, "quality_score": 8}'
        ]
        
        news_item = {
            'title': 'Test News',
            'url': 'https://example.com',
            'source': 'Test'
        }
        
        result = writer.generate_blog_post(news_item)
        
        assert result is not None
        assert 'title' in result
        assert 'content' in result
        assert 'meta_description' in result
    
    def test_generate_social_posts(self, writer):
        """Test social media post generation"""
        blog_data = {
            'title': 'Test Blog Post',
            'summary': 'This is a test summary',
            'seo_keywords': ['test', 'blog'],
            'slug': 'test-blog',
            'analysis': {
                'key_points': ['Point 1', 'Point 2']
            }
        }
        
        with patch.object(writer, '_call_ai', return_value='Test social post'):
            posts = writer.generate_social_posts(blog_data)
        
        assert isinstance(posts, dict)
        assert 'twitter' in posts
        assert 'linkedin' in posts
        assert 'telegram' in posts
    
    def test_call_ai_with_groq(self, writer):
        """Test AI API call with Groq"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'AI response text'
        writer.primary_client.chat.completions.create.return_value = mock_response
        
        result = writer._call_ai('Test prompt', max_tokens=100)
        
        assert result == 'AI response text'
        writer.primary_client.chat.completions.create.assert_called_once()
    
    def test_call_ai_fallback_to_gemini(self, writer):
        """Test fallback to Gemini when Groq fails"""
        writer.primary_client = None
        
        # Mock Gemini
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = 'Gemini response'
        mock_model.generate_content.return_value = mock_response
        writer.fallback_client = mock_model
        
        result = writer._call_ai('Test prompt', max_tokens=100)
        
        assert result == 'Gemini response'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
