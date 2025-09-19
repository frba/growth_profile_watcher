# Growth Profile Watcher

## Overview
The **Growth Profile Watcher** is a background tool designed to monitor the folder where the executable (`.exe`) is located. It analyzes growth profile data from newly created files in this folder and generates an XML file for the Momentum system when a specified growth criterion is met.

## Features
- Monitors the folder containing the `.exe` file for new files in real-time.
- Reads and processes growth profile data from the detected files.
- Evaluates the data against predefined growth criteria.
- Generates and outputs an XML file for the Momentum system when the criteria are satisfied.

## Requirements
- **Windows OS**
- Download the `.exe` file from the project's GitHub page.

## Installation
1. Download the `.exe` file from the [GitHub Releases page](https://github.com/your-repo/growth_profile_watcher/releases).
2. Place the `.exe` file in the desired folder to monitor.

## Usage
1. Run the `.exe` file by double-clicking it.
2. The tool will automatically monitor the folder where the `.exe` is located, process new files, and generate XML files when criteria are met.

## Configuration
The configuration is embedded in the tool. Ensure the files placed in the folder meet the expected format for growth profile data.

## Output
- XML files are generated in the same folder as the `.exe` file when the growth criteria are met.
- The XML files are formatted for compatibility with the Momentum system.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.