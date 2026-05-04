"""
Text Cleaner Utility - Cleans and formats text for various outputs
Handles Markdown stripping, HTML cleaning, and TTS preparation
"""

import re
from bs4 import BeautifulSoup
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TextCleaner:
    """Cleans and formats text for different output formats"""
    
    def clean_markdown(self, text):
        """Remove Markdown formatting from text"""
        if not text:
            return ""
        
        # Remove headers (# ## ###)
        text = re.sub(r'#{1,6}\s+', '', text)
        
        # Remove bold/italic markers
        text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
        text = re.sub(r'_{1,2}(.*?)_{1,2}', r'\1', text)
        
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`.*?`', '', text)
        
        # Remove links but keep text
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        
        # Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Remove horizontal rules
        text = re.sub(r'[-*_]{3,}', '', text)
        
        # Remove blockquotes
        text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def strip_markdown(self, text):
        """Alias for clean_markdown (for compatibility)"""
        return self.clean_markdown(text)
    
    def clean_html(self, text):
        """Remove HTML tags from text"""
        if not text:
            return ""
        
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def prepare_for_tts(self, text):
        """
        Prepare text for Text-to-Speech
        Removes special characters, expands abbreviations, adds pauses
        """
        if not text:
            return ""
        
        # First clean markdown
        text = self.clean_markdown(text)
        
        # Remove URLs (TTS can't read them well)
        text = re.sub(r'https?://\S+', 'link omitted', text)
        
        # Expand common abbreviations
        abbreviations = {
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Misses',
            'Ms.': 'Miss',
            'Prof.': 'Professor',
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'etcetera',
            'vs.': 'versus',
            'w/': 'with',
            'w/o': 'without',
            'AI': 'Artificial Intelligence',
            'API': 'Application Programming Interface',
            'UI': 'User Interface',
            'UX': 'User Experience',
            'URL': 'Uniform Resource Locator',
            'HTML': 'Hypertext Markup Language',
            'CSS': 'Cascading Style Sheets',
            'JS': 'JavaScript',
        }
        
        for abbr, full in abbreviations.items():
            text = re.sub(r'\b' + re.escape(abbr) + r'\b', full, text, flags=re.IGNORECASE)
        
        # Add pauses after sentences (for more natural TTS)
        text = re.sub(r'([.!?])\s+', r'\1\n\n', text)
        
        # Remove special characters that TTS might mispronounce
        text = re.sub(r'[^\w\s\.,!?;:\-\'\"]', '', text)
        
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_meta_description(self, text, max_length=160):
        """Extract or generate meta description from text"""
        if not text:
            return ""
        
        # Clean text
        clean = self.clean_markdown(text)
        
        # Take first few sentences
        sentences = re.split(r'[.!?]+', clean)
        description = ""
        
        for sentence in sentences:
            if len(description) + len(sentence) < max_length:
                description += sentence.strip() + ". "
            else:
                break
        
        if not description:
            description = clean[:max_length]
        
        return description.strip()
    
    def generate_slug(self, text):
        """Generate URL-friendly slug from text"""
        if not text:
            return ""
        
        from slugify import slugify
        return slugify(text[:100])  # Limit to 100 chars for slug
    
    def count_words(self, text):
        """Count words in text"""
        if not text:
            return 0
        
        # Clean and split
        clean = self.clean_markdown(text)
        words = clean.split()
        return len(words)
    
    def truncate(self, text, max_length=200, suffix="..."):
        """Truncate text to max length"""
        if not text or len(text) <= max_length:
            return text
        
        # Try to cut at sentence boundary
        truncated = text[:max_length - len(suffix)]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.5:  # If we can find a period in first half
            return text[:last_period + 1]
        
        return truncated + suffix
