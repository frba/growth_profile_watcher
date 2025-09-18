import subprocess
import sys
import os
import shutil

# --- Configuration ---
APP_SCRIPT = "main.py"
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
ICON_FILE = "growth_profile.ico"  # Make sure you have this in your project root

DATA_FILES = [
    # ("path/to/my/data_folder", "data_folder"), # Example: --add-data "path/to/my/data_folder;data_folder"
    # ("path/to/my/config.ini", "."),            # Example: --add-data "path/to/my/config.ini;."
]

# PyInstaller options. Add or remove as necessary.
PYINSTALLER_OPTIONS = [
    "--onefile",  # Create a single executable file
    "--noconsole",  # No console window for GUI apps
    f"--icon={ICON_FILE}"  # Use a custom icon
]

# Add data files to PyInstaller options
for source, dest in DATA_FILES:
    PYINSTALLER_OPTIONS.append(f"--add-data={source};{dest}")


# --- Utility Functions ---

def run_command(command, cwd=None, shell=False):
    """Executes a shell command and prints its output."""
    print(f"\nExecuting: {' '.join(command) if isinstance(command, list) else command}")
    try:
        # Use shell=True for simple commands that might require shell features (like 'pip install' on Windows)
        # However, for complex commands with arguments, it's safer to use a list and shell=False
        process = subprocess.run(command, cwd=cwd, shell=shell, check=True, capture_output=True, text=True)
        print(process.stdout)
        if process.stderr:
            print("Stderr:\n", process.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stdout:\n{e.stdout}")
        print(f"Stderr:\n{e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: Command not found. Is it in your PATH? (Command: {command[0] if isinstance(command, list) else command.split(' ')[0]})")
        sys.exit(1)


def ensure_virtual_environment():
    """Checks if a virtual environment exists, otherwise creates and activates it."""
    venv_path = os.path.join(os.getcwd(), VENV_DIR)
    if not os.path.exists(venv_path):
        print(f"Virtual environment not found at '{VENV_DIR}'. Creating...")
        run_command([sys.executable, "-m", "venv", VENV_DIR])
        print("Virtual environment created.")
    else:
        print(f"Virtual environment found at '{VENV_DIR}'.")


def install_dependencies():
    """Installs dependencies from requirements.txt into the virtual environment."""
    print(f"Installing dependencies from '{REQUIREMENTS_FILE}'...")
    pip_executable = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    if not os.path.exists(pip_executable):
        print(f"Error: pip executable not found in '{VENV_DIR}/Scripts'. Virtual environment might be corrupted.")
        sys.exit(1)
    run_command([pip_executable, "install", "-r", REQUIREMENTS_FILE])
    print("Dependencies installed.")


def run_pyinstaller():
    """Runs PyInstaller to create the executable."""
    print(f"\nRunning PyInstaller for '{APP_SCRIPT}'...")
    pyinstaller_executable = os.path.join(VENV_DIR, "Scripts", "pyinstaller.exe")
    if not os.path.exists(pyinstaller_executable):
        print(f"Error: PyInstaller executable not found in '{VENV_DIR}/Scripts'. Ensure it's in {REQUIREMENTS_FILE}.")
        sys.exit(1)

    command = [pyinstaller_executable, APP_SCRIPT] + PYINSTALLER_OPTIONS
    run_command(command)
    print("\nPyInstaller finished.")


def clean_build_artifacts():
    """Removes build and spec files after successful creation."""
    print("\nCleaning up build artifacts...")
    build_path = os.path.join(os.getcwd(), "build")
    spec_file = f"{os.path.splitext(APP_SCRIPT)[0]}.spec"
    dist_path = os.path.join(os.getcwd(), "dist")

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
        print(f"Removed '{build_path}'")
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"Removed '{spec_file}'")

    if os.path.exists(dist_path) and os.path.isdir(dist_path):
        print(f"Executable located in '{dist_path}'.")
    else:
        print("Dist directory not found or is empty. PyInstaller might have failed.")


# --- Main Execution Flow ---
if __name__ == "__main__":
    print("--- Starting Application Build Process ---")

    # Create a dummy icon file if it doesn't exist for demonstration
    if not os.path.exists(ICON_FILE):
        print(f"Warning: '{ICON_FILE}' not found. PyInstaller might use a default icon or fail.")
        print("You can create an empty file for demonstration purposes or provide a real .ico file.")
        # Create a dummy file for demonstration to prevent script from failing immediately
        try:
            with open(ICON_FILE, 'w') as f:
                f.write('')
        except IOError:
            print(f"Could not create dummy icon file: {ICON_FILE}")

    ensure_virtual_environment()
    install_dependencies()  # This will install pyinstaller into the venv
    run_pyinstaller()
    clean_build_artifacts()

    print("\n--- Build Process Completed ---")
    print(f"Your executable should be in the '{os.path.join(os.getcwd(), 'dist')}' directory.")