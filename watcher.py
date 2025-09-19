import time
import os
import sys
import csv
import momentum_xml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File extensions to process. Set to None or empty list to process all files.
FILE_EXTENSIONS = ['.csv']


def verify_wells_growth(plate_info, plate_data):
    """
    Verify if at least 50% of wells growth data is higher than 1 and return the time when it happened.
    :param plate_info: Dictionary containing plate information such as plate_id, plate_type, num_rows, and num_columns.
    :param plate_data: List of dictionaries containing time and wells growth data.
    :return: Time when at least 50% of wells growth data is higher than 1, or None if not found.
    """
    # Extract plate information
    num_columns = plate_info[0]['num_columns']
    num_rows = plate_info[0]['num_rows']
    plate_id = plate_info[0]['plate_id']
    plate_type = plate_info[0]['plate_type']

    # Calculate 50% of total wells
    threshold = (num_rows * num_columns) / 2
    print(f"Threshold for 50% of wells: {threshold}")
    min_value = 1

    for entry in plate_data:
        print(entry)
        wells_growth = entry['wells_growth']
        count_above_one = sum(1 for value in wells_growth if float(value) > 1)
        print(f"Count of wells with growth > 1 at time {entry['time']}: {count_above_one}")

        if count_above_one >= threshold:
            print(f"Time: {entry['time']}, Count above 1: {count_above_one}, Threshold: {threshold} at {plate_id} ({plate_type})")
            return entry['time']

    print("No time found where at least 50% of wells growth data is higher than 1.")
    return None


def process_csv_file(csv_path):
    """
    Process the CSV file to extract relevant information.
    :param csv_path: Path to the CSV file.
    """

    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Extract plate type (line 5, column 2)
        plate_type = rows[4][1]  # Line 5 is index 4 (0-based indexing)

        # Extract number of columns in the plate (line 6, column 2)
        num_columns = int(rows[5][1])  # Line 6 is index 5 (0-based indexing)

        # Extract number of rows in the plate (line 7, column 2)
        num_rows = int(rows[6][1])  # Line 7 is index 6

        # Extract plate id (line 10, column 2)
        plate_id = rows[9][1]  # Line 10 is index 9

        # Create a list to hold plate information
        plate_info = []
        plate_info.append({"plate_type": plate_type, "num_columns": num_columns, "num_rows": num_rows, "plate_id": plate_id})

        # Extract plate growth data starting from line 35
        plate_data = []
        for row in rows[35:]:  # Line 35 is index 34
            if not row or len(row) < num_rows * num_columns + 1:
                continue
            time = row[0]  # First column is time
            wells = row[1:num_rows*num_columns+1]  # Remaining columns are plate wells (excluding the last column)
            plate_data.append({"time": time, "wells_growth": wells})

        # Print extracted information
        print(f"Number of Columns: {num_columns}")
        print(f"Number of Rows: {num_rows}")
        print(f"Plate Type: {plate_type}")
        print(f"Plate ID: {plate_id}")
        print(f"Plate Data: {plate_data[:1]}")

        return plate_info, plate_data


# --- File Processing Logic ---
def process_new_file(file_path):
    """
    This function processes the newly created file.
    Replace this with your actual Python script logic.

    Args:
        file_path (str): The full path to the newly created file.
    """
    print(f"\n--- Processing new file: {file_path} ---")
    try:
        # Process the CSV file
        plate_info, plate_data = process_csv_file(file_path)

        # Verify wells growth
        time_of_growth = verify_wells_growth(plate_info, plate_data)

        print(f"Successfully processed: {file_path}")

        if time_of_growth: # If a valid time is returned
            '''Create a worklist for Momentum XML'''
            print(f"\n--- Create new XML worklist ---")
            momentum_xml.create(plate_data, plate_info)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. It might have been moved or deleted quickly.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
    finally:
        print(f"--- Finished processing: {file_path} ---\n")


# --- Watchdog Event Handler ---
class NewFileHandler(FileSystemEventHandler):
    """
    Custom event handler for watchdog to detect file creation events.
    """
    def on_created(self, event):
        """
        Called when a file or directory is created.
        """
        if not event.is_directory: # Ensure it's a file, not a directory
            file_path = event.src_path
            file_extension = os.path.splitext(file_path)[1].lower()

            # Check if the file extension is in our allowed list (if defined)
            if FILE_EXTENSIONS is None or file_extension in [ext.lower() for ext in FILE_EXTENSIONS]:
                print(f"Detected new file: {file_path}")
                process_new_file(file_path)
            else:
                print(f"Ignored file (unsupported extension): {file_path}")


# --- Main Script Execution ---
def start_watching(watched_folder):
    """
    Start watching the specified folder for new files.
    :param watched_folder: The folder is where the .exe file is placed, and where new files will be created.
    :return: None
    """

    # Validate the watched folder
    if not os.path.isdir(watched_folder):
        print(f"Error: The specified WATCHED_FOLDER '{watched_folder}' does not exist or is not a directory.")
        print("Please create the folder or update the WATCHED_FOLDER variable in the script.")
        sys.exit(1)

    print(f"Watching folder: {watched_folder}")
    if FILE_EXTENSIONS:
        print(f"Processing only files with extensions: {', '.join(FILE_EXTENSIONS)}")
    else:
        print("Processing all new files.")
    print("Press Ctrl+C to stop the script.")

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, watched_folder, recursive=False) # Set recursive=True to watch subdirectories

    observer.start()
    try:
        while True:
            time.sleep(1) # Keep the main thread alive
    except KeyboardInterrupt:
        observer.stop()
        print("\nFolder watcher stopped.")
    observer.join()
