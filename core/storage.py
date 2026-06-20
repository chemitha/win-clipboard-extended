import os
import time

CACHE_DIR = "cache"

def save_image_to_cache(pil_image):
    """Saves PIL Image to cache and returns the relative file path."""
    timestamp = int(time.time() * 1000)
    filename = f"img_{timestamp}.png"
    filepath = os.path.join(CACHE_DIR, filename)
    
    # Save the image to the disk
    pil_image.save(filepath, format="PNG")
    return filepath