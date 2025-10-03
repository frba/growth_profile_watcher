# Growth Profile Watcher

## Overview
The **Growth Profile Watcher** is a background tool designed to monitor a pre-defined folder (`.exe`). It analyzes growth profile data from newly created files in this folder and generates an XML file for the Momentum Thermo Scientific system when a specified growth criterion is met.

## Features
- Monitors the pre-defined folder for new `.csv` files in real-time.
- Reads and processes growth profile data from the detected files.
- Evaluates the data against predefined growth criteria.
- Generates and outputs an XML file for the Momentum Thermo Scientific system when the criteria are satisfied.

## Requirements
- **OS Windows 11**
- Download the `.exe` file from the project's GitHub page.

## Installation
Download the `.exe` file from the [GitHub Releases page](https://github.com/your-repo/growth_profile_watcher/releases).

## Usage
1. Run the `.exe` as an application launcher in Momentum process to start.
2. The tool will automatically monitor the folder, process new `.csv` files, and generate XML files when criteria are met.

## Output
- XML files are generated in the same folder as the `.exe` file when the growth criteria are met.
- The XML files are formatted for compatibility with the Momentum system.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.