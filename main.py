import os
import watcher
import pathlib
from pathlib import PureWindowsPath


if __name__ == "__main__":
    # Directory to test locally
    # If the application is run as a script
    # WATCHED_FOLDER = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample')

    # If the application is run as a bundled executable
    # Run the watcher to monitor the current directory for new files
    WATCHED_FOLDER = PureWindowsPath('X:\\GPViewer_data\\mcal\\ResultCSVs\\')
    watcher.start_watching(os.path.join(WATCHED_FOLDER))

