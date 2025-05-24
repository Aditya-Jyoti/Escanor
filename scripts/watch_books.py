import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

WATCH_DIR = "/home/aditya/Volumns/Reading/book"

def sanitize_filename(name):
    name = os.path.splitext(name)[0]
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

class BookHandler(FileSystemEventHandler):
    def process(self, filepath):
        if filepath.endswith('.epub') and os.path.isfile(filepath):
            print("file seen: ", filepath)
            filename = os.path.basename(filepath)
            foldername = sanitize_filename(filename)
            folderpath = os.path.join(WATCH_DIR, foldername)

            # Wait for file to be fully ready
            time.sleep(1)

            if not os.path.exists(folderpath):
                os.makedirs(folderpath)

            new_path = os.path.join(folderpath, filename)
            shutil.move(filepath, new_path)
            print(f"Moved {filename} to {folderpath}")

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"[CREATE] Detected file: {event.src_path}")
        self.process(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        print(f"[MOVE] Detected move from {event.src_path} to {event.dest_path}")
        self.process(event.dest_path)

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