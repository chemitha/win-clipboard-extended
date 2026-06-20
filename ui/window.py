import customtkinter as ctk
import keyboard
from ui.sidebar import Sidebar
from ui.view_text import TextWorkspace
from ui.view_image import ImageWorkspace

ctk.set_appearance_mode("dark")

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Windows Clipboard Note & Gallery")
        self.geometry("1000x600")
        self.minsize(800, 500)
        
        # Global Hotkey binding via keyboard module
        # Using lambda to safely push the UI update to the main Tkinter thread
        keyboard.add_hotkey('alt+v', lambda: self.after(0, self.toggle_visibility))
        self.is_visible = True

        self.setup_layout()
        self.poll_database_updates()

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=300) # Sidebar column
        self.grid_columnconfigure(1, weight=1)              # Main workspace column
        self.grid_rowconfigure(0, weight=1)

        # Initialize Sidebar
        self.sidebar = Sidebar(self, on_item_select=self.handle_item_selection)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Initialize the two view engines (hidden by default)
        self.view_text = TextWorkspace(self)
        self.view_image = ImageWorkspace(self)
        
        # Default empty state
        self.empty_label = ctk.CTkLabel(self, text="Select an item to view", font=ctk.CTkFont(size=14), text_color="gray")
        self.empty_label.grid(row=0, column=1)

    def handle_item_selection(self, item):
        # Hide default state and both views
        self.empty_label.grid_forget()
        self.view_text.grid_forget()
        self.view_image.grid_forget()

        # Show appropriate view based on type
        if item["type"] == "text":
            self.view_text.grid(row=0, column=1, sticky="nsew")
            self.view_text.load_data(item["content"])
        elif item["type"] == "image":
            self.view_image.grid(row=0, column=1, sticky="nsew")
            self.view_image.load_data(item["content"])

    def poll_database_updates(self):
        """Asks the UI to check for new database entries every 1 second."""
        self.sidebar.refresh_list()
        self.after(1000, self.poll_database_updates)

    def toggle_visibility(self):
        """Hides or unhides the application globally."""
        if self.is_visible:
            self.withdraw() # Hide window
            self.is_visible = False
        else:
            self.deiconify() # Show window
            self.focus_force() # Bring to front
            self.is_visible = True