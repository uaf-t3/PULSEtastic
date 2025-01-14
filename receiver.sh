#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Activate the virtual environment
source meshtastic-env/bin/activate

# Run the Python script and echo its output
python3 -u receiver.py 2>&1 | tee output.log

# Deactivate the virtual environment
deactivate