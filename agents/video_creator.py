"""
Video Creator Agent - Generates videos from images, audio, and text overlays
Uses MoviePy (free, open-source) for video creation
"""

import os
from pathlib import Path
from config.settings import settings
from utils.logger import setup_logger
from utils.image_downloader import ImageDownloader
from utils.music_manager import MusicManager

logger = setup_logger(__name__)


class VideoCreator:
    """Creates engaging videos from blog content, images, and audio"""
    
    def __init__(self):
        self.output_dir = settings.VIDEOS_DIR
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.image_downloader = ImageDownloader()
        self.music_manager = MusicManager()
        
    def create_video(self, blog_data, audio_path=None, blog_url=None):
        """
        Create a video from blog content
        Returns: Path to generated video file or None if failed
        """
        logger.info(f"Creating video for: {blog_data['title']}")
        
        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
            from PIL import Image
            import numpy as np
            
            # Step 1: Download relevant images
            images = self._get_images(blog_data)
            if not images:
                logger.error("No images available for video")
                return None
            
            # Step 2: Create video clips from images
            clips = self._create_image_clips(images)
            if not clips:
                return None
            
            # Step 3: Concatenate image clips
            video = concatenate_videoclips(clips, method="compose")
            
            # Step 4: Add audio if available
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                # Loop or trim video to match audio duration
                if video.duration < audio_clip.duration:
                    video = video.loop(duration=audio_clip.duration)
                else:
                    video = video.subclip(0, audio_clip.duration)
                video = video.set_audio(audio_clip)
            
            # Step 5: Add background music (low volume)
            video = self._add_background_music(video)
            
            # Step 6: Add text overlays (title, key points)
            video = self._add_text_overlays(video, blog_data)
            
            # Step 7: Render and save video
            output_path = self._render_video(video, blog_data)
            
            # Cleanup
            video.close()
            if audio_path and os.path.exists(audio_path):
                AudioFileClip(audio_path).close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Video creation failed: {str(e)}")
            return None
    
    def _get_images(self, blog_data):
        """Download images related to blog content"""
        keywords = blog_data.get('seo_keywords', [])
        if not keywords:
            keywords = [blog_data['title'].split()[:3]]
        
        # Try to download images
        images = self.image_downloader.download_images(
            keywords=keywords[:3],  # Top 3 keywords
            count=5,  # 5 images for video
            size=(settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT)
        )
        
        return images
    
    def _create_image_clips(self, image_paths):
        """Create video clips from image paths"""
        try:
            from moviepy.editor import ImageClip
            
            clips = []
            duration_per_image = settings.IMAGE_DURATION
            
            for img_path in image_paths:
                if os.path.exists(img_path):
                    clip = ImageClip(img_path)
                    clip = clip.set_duration(duration_per_image)
                    clip = clip.resize((settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT))
                    clips.append(clip)
            
            return clips
        except Exception as e:
            logger.error(f"Error creating image clips: {str(e)}")
            return []
    
    def _add_background_music(self, video):
        """Add background music at low volume"""
        try:
            from moviepy.editor import AudioFileClip
            
            music_path = self.music_manager.get_background_music()
            if not music_path or not os.path.exists(music_path):
                return video
            
            bg_music = AudioFileClip(music_path)
            
            # Loop music to match video duration
            if bg_music.duration < video.duration:
                bg_music = bg_music.loop(duration=video.duration)
            else:
                bg_music = bg_music.subclip(0, video.duration)
            
            # Lower volume
            bg_music = bg_music.volumex(settings.BG_MUSIC_VOLUME)
            
            # Combine with existing audio
            if video.audio:
                from moviepy.editor import CompositeAudioClip
                final_audio = CompositeAudioClip([video.audio, bg_music])
                video = video.set_audio(final_audio)
            else:
                video = video.set_audio(bg_music)
            
            bg_music.close()
            return video
            
        except Exception as e:
            logger.warning(f"Failed to add background music: {str(e)}")
            return video
    
    def _add_text_overlays(self, video, blog_data):
        """Add text overlays (title, source, URL)"""
        try:
            from moviepy.editor import TextClip, CompositeVideoClip
            
            clips_with_text = [video]
            
            # Title overlay at the beginning
            title = blog_data['title'][:50]  # Limit title length
            title_clip = TextClip(
                title,
                fontsize=40,
                color='white',
                bg_color='rgba(0,0,0,0.5)',
                size=(settings.VIDEO_WIDTH - 100, None),
                method='caption'
            )
            title_clip = title_clip.set_position(('center', 'bottom'))
            title_clip = title_clip.set_duration(3)  # Show for 3 seconds
            clips_with_text.append(title_clip)
            
            # URL at the end
            if 'url' in blog_data:
                url_clip = TextClip(
                    "Read more: " + blog_data.get('slug', ''),
                    fontsize=30,
                    color='yellow',
                    bg_color='rgba(0,0,0,0.7)'
                )
                url_clip = url_clip.set_position(('center', 'top'))
                url_clip = url_clip.set_duration(2)
                url_clip = url_clip.set_start(video.duration - 2)
                clips_with_text.append(url_clip)
            
            return CompositeVideoClip(clips_with_text)
            
        except Exception as e:
            logger.warning(f"Failed to add text overlays: {str(e)}")
            return video
    
    def _render_video(self, video, blog_data):
        """Render and save the final video"""
        try:
            from slugify import slugify
            
            # Create filename
            slug = slugify(blog_data['title'])[:50]
            filename = f"{slug}.mp4"
            output_path = os.path.join(self.output_dir, filename)
            
            # Render video
            logger.info(f"Rendering video to: {output_path}")
            video.write_videofile(
                output_path,
                fps=settings.VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                preset='medium',  # Balance between speed and quality
                ffmpeg_params=['-crf', '23']  # Constant Rate Factor (quality)
            )
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            logger.info(f"Video created: {output_path} ({file_size:.1f} MB)")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Video rendering failed: {str(e)}")
            return None
    
    def create_simple_video(self, image_path, audio_path, output_filename=None):
        """Create a simple video with one image and audio (fallback method)"""
        try:
            from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
            
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return None
            
            # Create image clip
            img_clip = ImageClip(image_path)
            
            # Add audio
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                img_clip = img_clip.set_duration(audio.duration)
                img_clip = img_clip.set_audio(audio)
            else:
                img_clip = img_clip.set_duration(30)  # Default 30 seconds
            
            # Resize to video dimensions
            img_clip = img_clip.resize((settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT))
            
            # Render
            if not output_filename:
                output_filename = f"simple_video_{hash(image_path)}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            img_clip.write_videofile(
                output_path,
                fps=settings.VIDEO_FPS,
                codec='libx264'
            )
            
            img_clip.close()
            return output_path
            
        except Exception as e:
            logger.error(f"Simple video creation failed: {str(e)}")
            return None
