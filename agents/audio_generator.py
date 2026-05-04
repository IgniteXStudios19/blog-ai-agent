"""
Audio Generator Agent - Converts text to speech using free TTS tools
Primary: Edge-TTS (Microsoft's free neural voices, no API key needed)
Backup: gTTS (Google Text-to-Speech)
"""

import os
import asyncio
from pathlib import Path
from config.settings import settings
from utils.logger import setup_logger
from utils.text_cleaner import TextCleaner

logger = setup_logger(__name__)


class AudioGenerator:
    """Generates MP3 audio files from text using free TTS services"""
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.output_dir = settings.AUDIO_DIR
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
    def generate_audio(self, text, filename=None, voice=None):
        """
        Generate MP3 audio from text
        Returns: Path to generated MP3 file or None if failed
        """
        if not text:
            logger.error("No text provided for audio generation")
            return None
        
        # Clean text for TTS
        text = self.text_cleaner.prepare_for_tts(text)
        
        # Generate filename if not provided
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.mp3"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Try Edge-TTS first (best free option)
        try:
            return self._generate_with_edge_tts(text, output_path, voice)
        except Exception as e:
            logger.warning(f"Edge-TTS failed: {str(e)}, trying gTTS...")
        
        # Fallback to gTTS
        try:
            return self._generate_with_gtts(text, output_path)
        except Exception as e:
            logger.error(f"gTTS also failed: {str(e)}")
            return None
    
    def _generate_with_edge_tts(self, text, output_path, voice=None):
        """Generate audio using Edge-TTS (Microsoft's free neural TTS)"""
        logger.info("Generating audio with Edge-TTS...")
        
        if voice is None:
            voice = settings.TTS_VOICE  # Default: en-US-AriaNeural
        
        # Edge-TTS requires asyncio
        async def _generate():
            import edge_tts
            
            # Split text into chunks if too long (Edge-TTS limit ~1000 chars)
            chunks = self._split_text(text, max_length=900)
            
            # Create communicate object
            communicate = edge_tts.Communicate(
                text=chunks[0] if len(chunks) == 1 else '. '.join(chunks),
                voice=voice,
                rate=settings.TTS_RATE
            )
            
            # Save to file
            await communicate.save(output_path)
        
        # Run async function
        asyncio.run(_generate())
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"Audio generated: {output_path} ({file_size / 1024:.1f} KB)")
            return output_path
        else:
            raise Exception("Output file not created")
    
    def _generate_with_gtts(self, text, output_path):
        """Generate audio using gTTS (Google Text-to-Speech)"""
        logger.info("Generating audio with gTTS...")
        
        from gtts import gTTS
        
        # gTTS works better with shorter text
        text = text[:3000]  # Limit to 3000 chars
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"Audio generated with gTTS: {output_path} ({file_size / 1024:.1f} KB)")
            return output_path
        else:
            raise Exception("Output file not created")
    
    def _split_text(self, text, max_length=900):
        """Split text into chunks for TTS"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > max_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def get_available_voices(self):
        """List available Edge-TTS voices (for reference)"""
        try:
            import edge_tts
            
            async def _list_voices():
                voices = await edge_tts.list_voices()
                return voices
            
            return asyncio.run(_list_voices())
        except:
            return []
    
    def generate_audio_for_blog(self, blog_data):
        """Generate audio specifically for a blog post"""
        logger.info(f"Generating audio for blog: {blog_data['title']}")
        
        # Use blog content (strip markdown)
        text = blog_data['content']
        text = self.text_cleaner.strip_markdown(text)
        
        # Create filename from title
        from slugify import slugify
        slug = slugify(blog_data['title'])[:50]
        filename = f"{slug}.mp3"
        
        return self.generate_audio(text, filename)
