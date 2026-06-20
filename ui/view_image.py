import customtkinter as ctk
from PIL import Image
import os

class ImageWorkspace(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#101010", **kwargs) # Darker background for image contrast
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self, text="Image Asset", font=ctk.CTkFont(size=14, weight="bold"))
        self.header.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def load_data(self, filepath):
        if not os.path.exists(filepath):
            self.image_label.configure(text="Image file lost or deleted.", image=None)
            return

        img = Image.open(filepath)
        # Scale to a safe preview size (maintaining aspect ratio)
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        self.image_label.configure(image=ctk_img, text="")
        self.image_label.image = ctk_img # Keep reference to prevent garbage collection