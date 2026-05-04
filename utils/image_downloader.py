"""
Image Downloader Utility - Downloads free stock images from Unsplash, Pexels, Pixabay
All APIs are free with reasonable limits
"""

import os
import requests
from pathlib import Path
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageDownloader:
    """Downloads images from free stock photo APIs"""
    
    def __init__(self):
        self.unsplash_key = settings.UNSPLASH_ACCESS_KEY
        self.pexels_key = settings.PEXELS_API_KEY
        self.pixabay_key = settings.PIXABAY_API_KEY
        self.output_dir = 'assets/downloaded_images'
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
    def download_images(self, keywords, count=5, size=(1280, 720)):
        """
        Download images based on keywords
        Tries Unsplash first, then Pexels, then Pixabay
        Returns: List of downloaded image paths
        """
        logger.info(f"Downloading {count} images for keywords: {keywords}")
        
        images = []
        
        # Try each API until we get enough images
        if self.unsplash_key and len(images) < count:
            images.extend(self._download_from_unsplash(keywords, count - len(images)))
        
        if self.pexels_key and len(images) < count:
            images.extend(self._download_from_pexels(keywords, count - len(images)))
        
        if self.pixabay_key and len(images) < count:
            images.extend(self._download_from_pixabay(keywords, count - len(images)))
        
        # Resize images if needed
        if images:
            images = self._resize_images(images, size)
        
        logger.info(f"Downloaded {len(images)} images")
        return images
    
    def _download_from_unsplash(self, keywords, count):
        """Download from Unsplash API (50 requests/hour free)"""
        images = []
        query = ' '.join(keywords[:3])  # Use top 3 keywords
        
        try:
            url = 'https://api.unsplash.com/search/photos'
            headers = {'Authorization': f'Client-ID {self.unsplash_key}'}
            params = {'query': query, 'per_page': min(count, 10), 'orientation': 'landscape'}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for i, photo in enumerate(results[:count]):
                    img_url = photo['urls']['regular']
                    filepath = os.path.join(self.output_dir, f'unsplash_{hash(query)}_{i}.jpg')
                    
                    if self._download_image(img_url, filepath):
                        images.append(filepath)
                        
            else:
                logger.warning(f"Unsplash API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Unsplash download failed: {str(e)}")
        
        return images
    
    def _download_from_pexels(self, keywords, count):
        """Download from Pexels API (200 requests/hour free)"""
        images = []
        query = ' '.join(keywords[:3])
        
        try:
            url = 'https://api.pexels.com/v1/search'
            headers = {'Authorization': self.pexels_key}
            params = {'query': query, 'per_page': min(count, 15), 'orientation': 'landscape'}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get('photos', [])
                
                for i, photo in enumerate(photos[:count]):
                    img_url = photo['src']['large']
                    filepath = os.path.join(self.output_dir, f'pexels_{hash(query)}_{i}.jpg')
                    
                    if self._download_image(img_url, filepath):
                        images.append(filepath)
                        
            else:
                logger.warning(f"Pexels API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Pexels download failed: {str(e)}")
        
        return images
    
    def _download_from_pixabay(self, keywords, count):
        """Download from Pixabay API (100 requests/minute free)"""
        images = []
        query = ' '.join(keywords[:3])
        
        try:
            url = 'https://pixabay.com/api/'
            params = {
                'key': self.pixabay_key,
                'q': query,
                'per_page': min(count, 20),
                'image_type': 'photo',
                'orientation': 'horizontal'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', [])
                
                for i, hit in enumerate(hits[:count]):
                    img_url = hit['largeImageURL']
                    filepath = os.path.join(self.output_dir, f'pixabay_{hash(query)}_{i}.jpg')
                    
                    if self._download_image(img_url, filepath):
                        images.append(filepath)
                        
            else:
                logger.warning(f"Pixabay API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Pixabay download failed: {str(e)}")
        
        return images
    
    def _download_image(self, url, filepath):
        """Download a single image from URL"""
        try:
            response = requests.get(url, timeout=10, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                logger.debug(f"Downloaded: {filepath}")
                return True
        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
        return False
    
    def _resize_images(self, image_paths, size):
        """Resize images to target size"""
        try:
            from PIL import Image
            
            resized = []
            target_width, target_height = size
            
            for img_path in image_paths:
                try:
                    img = Image.open(img_path)
                    
                    # Resize maintaining aspect ratio
                    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Create new image with target size and paste resized image centered
                    new_img = Image.new('RGB', (target_width, target_height), (0, 0, 0))
                    left = (target_width - img.width) // 2
                    top = (target_height - img.height) // 2
                    new_img.paste(img, (left, top))
                    
                    # Save
                    new_img.save(img_path, 'JPEG', quality=85)
                    resized.append(img_path)
                    
                except Exception as e:
                    logger.error(f"Failed to resize {img_path}: {str(e)}")
                    resized.append(img_path)  # Keep original if resize fails
            
            return resized
            
        except Exception as e:
            logger.error(f"Image resizing failed: {str(e)}")
            return image_paths
    
    def get_fallback_image(self):
        """Return path to a fallback image if downloads fail"""
        fallback = 'assets/templates/default_news.jpg'
        if os.path.exists(fallback):
            return fallback
        
        # Create a simple fallback image
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (1280, 720), color=(30, 60, 120))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            text = "News Update"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1280 - text_width) // 2
            y = (720 - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Save
            Path('assets/templates').mkdir(parents=True, exist_ok=True)
            img.save(fallback, 'JPEG')
            
            return fallback
            
        except Exception as e:
            logger.error(f"Failed to create fallback image: {str(e)}")
            return None
