import os
import threading
from core.listener import ClipboardListener
from ui.window import AppWindow
from core.database import init_db

def setup_environment():
    # Ensure cache directory exists to prevent crash on first image copy
    if not os.path.exists("cache"):
        os.makedirs("cache")
    # Initialize the SQLite database
    init_db()

if __name__ == "__main__":
    setup_environment()

    # 1. Start the headless background clipboard monitor
    listener = ClipboardListener()
    listener_thread = threading.Thread(target=listener.start_listening, daemon=True)
    listener_thread.start()

    # 2. Start the Windows GUI (must run on the main thread)
    app = AppWindow()
    app.mainloop()