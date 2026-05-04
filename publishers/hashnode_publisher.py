"""
Hashnode Publisher - Publishes blog posts to Hashnode (free blog platform)
Uses Hashnode's GraphQL API (completely free, no rate limits for personal use)
"""

import requests
import json
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HashnodePublisher:
    """Publishes blog posts to Hashnode via GraphQL API"""
    
    def __init__(self):
        self.api_key = settings.HASHNODE_API_KEY
        self.publication_id = settings.HASHNODE_PUBLICATION_ID.strip()  # Remove newlines/spaces
        self.api_url = 'https://gql.hashnode.com'
        
        if not self.api_key:
            logger.warning("Hashnode API key not configured")
    
    def publish(self, blog_data):
        """
        Publish a blog post to Hashnode
        Returns: URL of published post or None if failed
        """
        if not self.api_key or not self.publication_id:
            logger.error("Hashnode not configured. Missing API key or Publication ID")
            return None
        
        logger.info(f"Publishing to Hashnode: {blog_data['title']}")
        
        # Prepare the blog post content
        title = blog_data['title']
        content = blog_data['content']
        tags = blog_data.get('tags', [])
        slug = blog_data.get('slug', '')
        
        # Convert tags to Hashnode format
        tag_slugs = []
        for tag in tags[:5]:  # Max 5 tags
            tag_slug = self._slugify_tag(tag)
            if tag_slug:
                # Hashnode requires both slug and name for tag input
                tag_slugs.append({
                    'slug': tag_slug,
                    'name': tag  # Original tag name (not slugified)
                })
        
        # GraphQL mutation for creating a post (simplified - only valid fields)
        mutation = """
        mutation PublishPost($input: PublishPostInput!) {
            publishPost(input: $input) {
                post {
                    id
                    title
                    slug
                    url
                }
            }
        }
        """
        
        # Prepare input variables (only valid fields)
        variables = {
            'input': {
                'title': title,
                'contentMarkdown': content,
                'tags': tag_slugs,
                'publicationId': self.publication_id,  # Clean ID without newlines
            }
        }
        
        # Add slug if provided
        if slug:
            variables['input']['slug'] = slug
        
        # Make the API request
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'query': mutation,
            'variables': variables
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for errors
                if 'errors' in result:
                    logger.error(f"Hashnode API errors: {result['errors']}")
                    return None
                
                # Get the published post URL
                post_data = result.get('data', {}).get('publishPost', {}).get('post', {})
                post_url = post_data.get('url')
                
                if post_url:
                    logger.info(f"Published to Hashnode: {post_url}")
                    return post_url
                else:
                    logger.error("Hashnode publish succeeded but no URL returned")
                    return None
            else:
                logger.error(f"Hashnode API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Hashnode publish failed: {str(e)}")
            return None
    
    def _slugify_tag(self, tag):
        """Convert tag to URL-friendly slug"""
        if not tag:
            return ''
        # Simple slugify: lowercase, replace spaces with hyphens
        slug = tag.lower().replace(' ', '-').replace('_', '-')
        # Remove special characters
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return slug[:50]  # Limit length
