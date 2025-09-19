import os, sys
import watcher
import subprocess
import pathlib


def get_most_recent_file(directory):
    """
    Get the most recent file in the specified directory based on creation time.

    :param directory: Directory to search for files.
    :return: The most recent file name.
    """
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    most_recent_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
    print(f"Most Recent File to be Processed: {most_recent_file}")
    most_recent_file_path = os.path.join(directory, most_recent_file)
    return most_recent_file_path


if __name__ == "__main__":
    # Get the current working directory
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled executable
        current_directory = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        # current_directory = os.getcwd()
        current_directory = pathlib.Path(__file__).parent.resolve()
        print(f"Current Directory: {current_directory}")

    # Run the watcher to monitor the current directory for new files
    watcher.start_watching(os.path.join(current_directory))

