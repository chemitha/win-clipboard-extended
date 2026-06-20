import customtkinter as ctk

class TextWorkspace(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#1c1c1c", **kwargs)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header utility
        self.header = ctk.CTkLabel(self, text="Text Snippet", font=ctk.CTkFont(size=14, weight="bold"))
        self.header.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Text Editor component
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Segoe UI", size=14), 
                                      fg_color="#2d2d2d", border_color="#3f3f3f", border_width=1)
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def load_data(self, content):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", content)