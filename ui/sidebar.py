import customtkinter as ctk
import core.database as db

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_item_select, **kwargs):
        super().__init__(master, fg_color="#202020", corner_radius=0, **kwargs)
        self.on_item_select = on_item_select
        self.current_item_count = 0
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Clipboard History", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=15, pady=15)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5)

    def refresh_list(self):
        items = db.get_recent_items()
        
        # Only rebuild UI if database has changed (prevents flickering)
        if len(items) == self.current_item_count and self.current_item_count != 0:
            return

        self.current_item_count = len(items)

        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Build list cards
        for item in items:
            preview_text = ""
            if item["type"] == "text":
                preview_text = item["content"].replace('\n', ' ')[:35] + "..."
            else:
                preview_text = "📷 Image Asset"

            btn = ctk.CTkButton(
                self.scroll_frame, 
                text=preview_text,
                anchor="w",
                fg_color="#2d2d2d", hover_color="#3d3d3d",
                command=lambda i=item: self.on_item_select(i) # Capture item data safely
            )
            btn.pack(fill="x", pady=2, padx=5)