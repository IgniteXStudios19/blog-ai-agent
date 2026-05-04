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
        self.publication_id = settings.HASHNODE_PUBLICATION_ID
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
        meta_description = blog_data.get('meta_description', '')
        slug = blog_data.get('slug', '')
        
        # Convert tags to Hashnode format
        tag_slugs = []
        for tag in tags[:5]:  # Max 5 tags
            tag_slug = self._slugify_tag(tag)
            if tag_slug:
                tag_slugs.append({'slug': tag_slug})
        
        # GraphQL mutation for creating a post
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
        
        # Prepare input variables
        variables = {
            'input': {
                'title': title,
                'contentMarkdown': content,
                'tags': tag_slugs,
                'coverImageURL': blog_data.get('cover_image', ''),
                'brief': meta_description,
                'publicationId': self.publication_id,
                'hideFromFeed': False,
                'isRepublished': {
                    'originalArticleURL': ''
                }
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
                data = response.json()
                
                if 'errors' in data:
                    logger.error(f"Hashnode API errors: {data['errors']}")
                    return None
                
                post_data = data.get('data', {}).get('publishPost', {}).get('post', {})
                
                if post_data:
                    post_url = post_data.get('url', '')
                    logger.info(f"Successfully published to Hashnode: {post_url}")
                    return post_url
                else:
                    logger.error("No post data in response")
                    return None
            else:
                logger.error(f"Hashnode API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to publish to Hashnode: {str(e)}")
            return None
    
    def update_post(self, post_id, blog_data):
        """Update an existing post (if needed)"""
        logger.info(f"Updating Hashnode post: {post_id}")
        
        # Similar to publish but with update mutation
        # Implementation depends on Hashnode's API for updates
        pass
    
    def get_publication_info(self):
        """Get information about the publication"""
        query = """
        query GetPublication($host: String!) {
            publication(host: $host) {
                id
                title
                url
                posts(first: 5) {
                    edges {
                        node {
                            title
                            slug
                            url
                        }
                    }
                }
            }
        }
        """
        
        variables = {'host': 'your-hashnode-host'}  # e.g., 'yourblog.hashnode.dev'
        
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'query': query,
            'variables': variables
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get publication info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting publication info: {str(e)}")
            return None
    
    def _slugify_tag(self, tag):
        """Convert tag to slug format"""
        if not tag:
            return ''
        
        # Simple slugify for tags
        slug = tag.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return slug[:50]  # Limit length
