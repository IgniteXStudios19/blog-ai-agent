"""
Music Manager Utility - Manages background music for videos
Pre-downloaded free music stored in assets/music/
"""

import os
from pathlib import Path
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MusicManager:
    """Manages background music files for video generation"""
    
    def __init__(self):
        self.music_dir = 'assets/music'
        Path(self.music_dir).mkdir(parents=True, exist_ok=True)
        self.default_music = None
        self._scan_music_files()
        
    def _scan_music_files(self):
        """Scan for available music files"""
        self.music_files = []
        
        if not os.path.exists(self.music_dir):
            return
        
        for ext in ['*.mp3', '*.wav', '*.ogg', '*.m4a']:
            self.music_files.extend(Path(self.music_dir).glob(ext))
        
        if self.music_files:
            self.default_music = str(self.music_files[0])
            logger.info(f"Found {len(self.music_files)} music files")
        else:
            logger.warning(f"No music files found in {self.music_dir}")
    
    def get_background_music(self, index=0):
        """
        Get a background music file path
        If no music available, returns None (video will have no BG music)
        """
        if not self.music_files:
            return None
        
        # Cycle through available music
        idx = index % len(self.music_files)
        return str(self.music_files[idx])
    
    def download_free_music(self):
        """
        Download free background music from Free Music Archive
        This is a one-time setup function
        """
        logger.info("Downloading free background music...")
        
        # List of free music URLs (instrumental, news-style)
        # These are royalty-free tracks suitable for news videos
        free_music_urls = [
            # Example: You would replace these with actual free music URLs
            # 'https://files.freemusicarchive.org/music/Creative_Commons/...'
        ]
        
        downloaded = 0
        for i, url in enumerate(free_music_urls[:5]):  # Limit to 5 files
            try:
                import requests
                response = requests.get(url, timeout=30, stream=True)
                
                if response.status_code == 200:
                    filename = f"bg_music_{i}.mp3"
                    filepath = os.path.join(self.music_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    
                    downloaded += 1
                    logger.info(f"Downloaded: {filename}")
                    
            except Exception as e:
                logger.error(f"Failed to download music from {url}: {str(e)}")
        
        # Rescan after download
        self._scan_music_files()
        
        return downloaded
    
    def create_silence_audio(self, duration=60, output_path=None):
        """
        Create a silence audio file as fallback
        Requires ffmpeg to be installed
        """
        if output_path is None:
            output_path = os.path.join(self.music_dir, 'silence.mp3')
        
        try:
            import subprocess
            
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo',
                '-t', str(duration), '-q:a', '9', '-acodec', 'libmp3lame',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Created silence audio: {output_path}")
            
            self._scan_music_files()
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create silence audio: {str(e)}")
            return None
    
    def get_music_info(self):
        """Get information about available music files"""
        info = {
            'music_dir': self.music_dir,
            'files_count': len(self.music_files),
            'files': [str(f) for f in self.music_files],
            'default': self.default_music
        }
        return info
    
    def add_music_file(self, source_path):
        """
        Add a music file to the music directory
        Use this to manually add pre-downloaded music
        """
        if not os.path.exists(source_path):
            logger.error(f"Source file not found: {source_path}")
            return False
        
        import shutil
        filename = os.path.basename(source_path)
        dest_path = os.path.join(self.music_dir, filename)
        
        try:
            shutil.copy2(source_path, dest_path)
            logger.info(f"Added music file: {filename}")
            self._scan_music_files()
            return True
        except Exception as e:
            logger.error(f"Failed to add music file: {str(e)}")
            return False
