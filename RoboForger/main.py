from RoboForger.app.application import RoboforgerApp
from RoboForger.utils import get_resources_dir

import sys
import os
import traceback
import ctypes

DEBUG = False

def show_crash_dialog(error_msg):
    """
    Displays a native Windows Error Dialog.
    We use ctypes because Qt might be the thing crashing!
    """
    ctypes.windll.user32.MessageBoxW(0, error_msg, "RoboForger Fatal Error", 0x10)

def main():
    try:
        resource_dir = get_resources_dir()

        if not os.path.exists(resource_dir):
            raise FileNotFoundError(f"Resource directory not found at {resource_dir}")
            
        app = RoboforgerApp(sys.argv, resource_dir)
        sys.exit(app.run())

    except Exception:
        full_traceback = traceback.format_exc()
        
        with open("crash_log.txt", "w") as f:
            f.write(full_traceback)
            
        show_crash_dialog(f"The application crashed!\n\nLog saved to crash_log.txt\n\nError:\n{full_traceback}")
        sys.exit(1)

if __name__ == "__main__":
    main()