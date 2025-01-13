#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Check if the virtual environment directory exists
if [ ! -d "meshtastic-env" ]; then
    echo "Virtual environment not found. Please create it using 'python3 -m venv meshtastic-env'"
    exit 1
fi

# Activate the virtual environment
source meshtastic-env/bin/activate

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

# Run the Python script with the provided message
python3 sender.py "$1"

# Deactivate the virtual environment
deactivate