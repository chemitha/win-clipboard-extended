import time
import pyperclip
from PIL import ImageGrab, Image
import core.database as db
import core.storage as storage
import hashlib

class ClipboardListener:
    def __init__(self, poll_interval=0.5):
        self.poll_interval = poll_interval
        self.last_text_hash = None
        self.last_image_hash = None

    def start_listening(self):
        while True:
            self.check_clipboard()
            time.sleep(self.poll_interval)

    def check_clipboard(self):
        # 1. Check for Text
        try:
            text = pyperclip.paste()
            if text and text.strip() != "":
                text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                if text_hash != self.last_text_hash:
                    self.last_text_hash = text_hash
                    db.add_item("text", text)
        except Exception:
            pass # Ignore text read errors

        # 2. Check for Images
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                # Create a quick thumbnail hash to check uniqueness efficiently
                thumb = img.copy()
                thumb.thumbnail((50, 50))
                img_hash = hash(thumb.tobytes())
                
                if img_hash != self.last_image_hash:
                    self.last_image_hash = img_hash
                    filepath = storage.save_image_to_cache(img)
                    db.add_item("image", filepath)
        except Exception:
            pass # Ignore image read errors