import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

WATCH_DIR = "/book"

def sanitize_filename(name):
    # Replace non-alphanumeric with hyphens and remove extension
    name = os.path.splitext(name)[0]
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

class BookHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = event.src_path
        if filepath.endswith('.epub'):
            filename = os.path.basename(filepath)
            foldername = sanitize_filename(filename)
            folderpath = os.path.join(WATCH_DIR, foldername)

            # Wait a bit for the file to be fully written
            time.sleep(1)

            if not os.path.exists(folderpath):
                os.makedirs(folderpath)
            
            new_path = os.path.join(folderpath, filename)
            shutil.move(filepath, new_path)
            print(f"Moved {filename} to {folderpath}")

if __name__ == "__main__":
    event_handler = BookHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()
    print(f"Watching directory: {WATCH_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
