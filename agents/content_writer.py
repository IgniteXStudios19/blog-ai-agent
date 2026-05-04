"""
Content Writer Agent - Generates blog posts and social media content using free AI models
Supports Groq (primary) and Gemini (fallback) - both completely free
"""

import json
import re
from config.settings import settings
from config.prompts import PromptTemplates
from utils.logger import setup_logger
from utils.text_cleaner import TextCleaner

logger = setup_logger(__name__)


class ContentWriter:
    """Generates high-quality, SEO-optimized content using free AI models"""
    
    def __init__(self):
        self.primary_client = None
        self.fallback_client = None
        self.text_cleaner = TextCleaner()
        self._initialize_ai_clients()
        
    def _initialize_ai_clients(self):
        """Initialize AI clients (Groq primary, Gemini fallback)"""
        
        # Initialize Groq (primary - fastest free LLM)
        if settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self.primary_client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq AI client initialized (primary)")
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {str(e)}")
        
        # Initialize Gemini (fallback)
        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.fallback_client = genai.GenerativeModel(settings.GEMINI_MODEL)
                logger.info("Gemini AI client initialized (fallback)")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {str(e)}")
        
        if not self.primary_client and not self.fallback_client:
            raise ValueError("No AI API keys configured! Need GROQ_API_KEY or GEMINI_API_KEY")
    
    def generate_blog_post(self, news_item, full_article=None):
        """Generate a complete blog post from news item"""
        logger.info(f"Generating blog post for: {news_item['title']}")
        
        # Step 1: Analyze the news
        analysis = self._analyze_news(news_item, full_article)
        if not analysis:
            logger.error("News analysis failed")
            return None
        
        # Step 2: Create blog outline
        outline = self._create_outline(analysis)
        if not outline:
            logger.error("Outline creation failed")
            return None
        
        # Step 3: Write full blog post
        blog_post = self._write_blog_post(analysis, outline)
        if not blog_post:
            logger.error("Blog writing failed")
            return None
        
        # Step 4: Humanize the content
        blog_post = self._humanize_content(blog_post)
        
        # Step 5: Generate SEO metadata
        seo_metadata = self._generate_seo_metadata(blog_post, analysis)
        
        # Step 6: Quality check
        quality = self._check_quality(blog_post)
        
        return {
            'title': seo_metadata.get('meta_title', analysis.get('main_topic', news_item['title'])),
            'content': blog_post,
            'summary': analysis.get('summary', ''),
            'meta_description': seo_metadata.get('meta_description', ''),
            'slug': seo_metadata.get('slug', ''),
            'tags': seo_metadata.get('tags', []),
            'seo_keywords': analysis.get('seo_keywords', []),
            'word_count': quality.get('word_count', 0),
            'quality_score': quality.get('quality_score', 0),
            'analysis': analysis
        }
    
    def _analyze_news(self, news_item, full_article=None):
        """Analyze news article using AI"""
        logger.info("Analyzing news article...")
        
        text = full_article['text'] if full_article else news_item.get('summary', '')
        text = text[:3000]  # Limit to 3000 chars for API
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'RESEARCH_ANALYSIS',
            title=news_item['title'],
            text=text,
            source=news_item.get('source', 'Unknown'),
            published=news_item.get('published', 'Unknown')
        )
        
        response = self._call_ai(prompt, max_tokens=1000)
        if not response:
            return None
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.error(f"Failed to parse analysis JSON: {str(e)}")
        
        return None
    
    def _create_outline(self, analysis):
        """Create blog post outline"""
        logger.info("Creating blog outline...")
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'BLOG_OUTLINE',
            summary=analysis.get('summary', ''),
            key_points='\n'.join(analysis.get('key_points', [])),
            target_audience=analysis.get('target_audience', 'General readers'),
            seo_keywords=', '.join(analysis.get('seo_keywords', [])),
            min_words=settings.MIN_ARTICLE_WORDS,
            max_words=settings.MAX_ARTICLE_WORDS
        )
        
        response = self._call_ai(prompt, max_tokens=1000)
        return response
    
    def _write_blog_post(self, analysis, outline):
        """Write full blog post"""
        logger.info("Writing full blog post...")
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'BLOG_WRITING',
            niche=settings.NICHE,
            outline=outline,
            news_details=json.dumps(analysis, indent=2),
            seo_keywords=', '.join(analysis.get('seo_keywords', [])),
            min_words=settings.MIN_ARTICLE_WORDS,
            max_words=settings.MAX_ARTICLE_WORDS,
            language=settings.BLOG_LANGUAGE
        )
        
        response = self._call_ai(prompt, max_tokens=4000)
        
        # Clean the response
        if response:
            response = self.text_cleaner.clean_markdown(response)
        
        return response
    
    def _humanize_content(self, text):
        """Make AI content sound more human"""
        logger.info("Humanizing content...")
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'HUMANIZE_CONTENT',
            text=text[:3000]  # Limit for API
        )
        
        response = self._call_ai(prompt, max_tokens=4000)
        return response if response else text
    
    def _generate_seo_metadata(self, blog_post, analysis):
        """Generate SEO metadata"""
        logger.info("Generating SEO metadata...")
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'SEO_METADATA',
            title=analysis.get('main_topic', ''),
            summary=blog_post[:500],
            keywords=', '.join(analysis.get('seo_keywords', []))
        )
        
        response = self._call_ai(prompt, max_tokens=500)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Return defaults
        return {
            'meta_title': analysis.get('main_topic', ''),
            'meta_description': blog_post[:160],
            'slug': '',
            'tags': analysis.get('seo_keywords', [])[:5]
        }
    
    def _check_quality(self, text):
        """Check content quality"""
        logger.info("Checking content quality...")
        
        word_count = len(text.split())
        
        prompt = PromptTemplates.FORMAT_PROMPT(
            'QUALITY_CHECK',
            text=text[:2000],
            min=settings.MIN_ARTICLE_WORDS,
            max=settings.MAX_ARTICLE_WORDS
        )
        
        response = self._call_ai(prompt, max_tokens=500)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result['word_count'] = word_count
                return result
        except:
            pass
        
        return {
            'word_count': word_count,
            'readability_score': 7,
            'seo_score': 7,
            'quality_score': 7,
            'issues': [],
            'passed': word_count >= settings.MIN_ARTICLE_WORDS
        }
    
    def generate_social_posts(self, blog_data):
        """Generate social media posts for all platforms"""
        logger.info("Generating social media posts...")
        
        posts = {}
        
        # Twitter/X
        posts['twitter'] = self._generate_twitter_post(blog_data)
        
        # LinkedIn
        posts['linkedin'] = self._generate_linkedin_post(blog_data)
        
        # Reddit
        posts['reddit'] = self._generate_reddit_post(blog_data)
        
        # Telegram
        posts['telegram'] = self._generate_telegram_post(blog_data)
        
        # Discord
        posts['discord'] = self._generate_discord_embed(blog_data)
        
        # Mastodon
        posts['mastodon'] = self._generate_mastodon_post(blog_data)
        
        return posts
    
    def _generate_twitter_post(self, blog_data):
        """Generate Twitter/X post"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'TWITTER_POST',
            title=blog_data['title'],
            summary=blog_data['summary'],
            url='[BLOG_URL]',  # Will be replaced after publishing
            keywords=', '.join(blog_data.get('seo_keywords', []))
        )
        return self._call_ai(prompt, max_tokens=300)
    
    def _generate_linkedin_post(self, blog_data):
        """Generate LinkedIn post"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'LINKEDIN_POST',
            title=blog_data['title'],
            summary=blog_data['summary'],
            key_points='\n'.join(blog_data.get('analysis', {}).get('key_points', [])),
            url='[BLOG_URL]'
        )
        return self._call_ai(prompt, max_tokens=1500)
    
    def _generate_reddit_post(self, blog_data):
        """Generate Reddit post"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'REDDIT_POST',
            title=blog_data['title'],
            summary=blog_data['summary'],
            key_points='\n'.join(blog_data.get('analysis', {}).get('key_points', [])),
            url='[BLOG_URL]',
            subreddit='[SUBREDDIT]'
        )
        return self._call_ai(prompt, max_tokens=500)
    
    def _generate_telegram_post(self, blog_data):
        """Generate Telegram post"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'TELEGRAM_POST',
            title=blog_data['title'],
            summary=blog_data['summary'],
            url='[BLOG_URL]'
        )
        return self._call_ai(prompt, max_tokens=500)
    
    def _generate_discord_embed(self, blog_data):
        """Generate Discord embed"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'DISCORD_EMBED',
            title=blog_data['title'],
            summary=blog_data['summary'],
            url='[BLOG_URL]',
            image_url='[IMAGE_URL]',
            niche=settings.NICHE
        )
        
        response = self._call_ai(prompt, max_tokens=500)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return None
    
    def _generate_mastodon_post(self, blog_data):
        """Generate Mastodon post"""
        prompt = PromptTemplates.FORMAT_PROMPT(
            'MASTODON_POST',
            title=blog_data['title'],
            summary=blog_data['summary'],
            url='[BLOG_URL]',
            keywords=', '.join(blog_data.get('seo_keywords', []))
        )
        return self._call_ai(prompt, max_tokens=600)
    
    def _call_ai(self, prompt, max_tokens=2000):
        """Call AI model with fallback logic"""
        
        # Try primary (Groq) first
        if self.primary_client:
            try:
                response = self.primary_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Groq API failed: {str(e)}, trying fallback...")
        
        # Fallback to Gemini
        if self.fallback_client:
            try:
                response = self.fallback_client.generate_content(
                    prompt,
                    generation_config={'max_output_tokens': max_tokens, 'temperature': 0.7}
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini API also failed: {str(e)}")
        
        return None
