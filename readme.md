# Growth Profile Watcher

## Overview
The **Growth Profile Watcher** is a background tool designed to monitor a `.csv` file defined by the user. 
It analyzes growth profile data from Enzyscreen, like OD, green values and growth rate from a `.csv` file and generates an XML file for the Momentum Thermo Scientific system when a specified growth criterion is met.

## Features
- Monitors the `.csv` files in real-time.
- Reads and processes growth profile data from the detected files.
- Evaluates the data against predefined growth criteria.
- Generates and outputs an XML file for the Momentum Thermo Scientific system when the criteria are satisfied.

## Requirements
- **OS Windows 11**
- Download the `.exe` file from the project's GitHub page.

## Installation
Download the `.exe` file from the GitHub Releases page.

## Pre-requisite Workflow: Enzyscreen & Momentum Setup 🧪
Before starting the Growth Profile Watcher, you must initiate Enzyscreen GP. Go to GP960 Control software and click idle and start to initiate the instrument.

### 1. Enzyscreen Setup and Plate Loading in Momentum
- **Start Enzyscreen**: Navigate to the Enzyscreen software and ensure the GP960 Control software is started (shaking) or set to pause.
- **Momentum Inventory**: Add all plates for the experiment—both dummy and normal Enzyscreen plates—to the Momentum Inventory.
  - Crucially: Every plate must have an associated barcode.
- **Load Plates**: Place the prepared plate(s) at Hotel on the Momentum system.
- **Initiate Loading**: Call a Momentum process to load the plate(s) onto the Enzyscreen instrument.

### 2. Post-Acquisition Data Processing
- **First Acquisition**: Once the Enzyscreen completes its first measurement acquisition, the instrument will momentarily stop and then resume shaking.
- **GPviewer Configuration**: Go to the Enzyscreen GPviewer application.
  - Set up a new experiment.
  - Select the folder where the current experiment's data is running.
  - Select the appropriate calibration curve to enable the calculation of Optical Densities (ODs).
- **OD File Generation**: Once configured, the system will automatically create a new version of the raw `.csv` file, appending `_OD` to the filename (e.g., `experiment_data_OD.csv`). This file contains the calculated OD values.

## Usage
- Run the `.exe` as an application launcher in Momentum process to start.
- The tool will the file path and the type of parameter should be tracked (OD, Green values or Growth rate).
- Once a threshold is met the GP watcher will generate XML file and place the new worklist in Momentum watcher folder.


## Output
- XML files are generated in the Momentum watcher folder when the growth criteria are met.
- The XML files are formatted for compatibility with the Momentum system.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.
"""