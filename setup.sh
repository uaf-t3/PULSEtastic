#!/usr/bin/env bash
#
# setup.sh - Configure a Meshtastic node by directly using a base64 PSK.
#            Sets up a virtual environment if missing, installs dependencies,
#            and configures the Meshtastic node.

set -e  # Exit on error

VENV_DIR="meshtastic-env"

# 1) Function to install dependencies
install_dependencies() {
  echo "Installing dependencies..."
  python3 -m venv "$VENV_DIR"
  source "$VENV_DIR/bin/activate"
  echo "Upgrading pip..."
  pip install --upgrade pip
  echo "Installing Meshtastic Python package..."
  pip install meshtastic
  pip install pubsub
  echo "Dependencies installed successfully."
}

# 2) Check if the virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment '$VENV_DIR' not found."
  read -p "Would you like to create it and install dependencies now? (y/n): " response
  if [[ "$response" == "y" || "$response" == "Y" ]]; then
    install_dependencies
  else
    echo "Aborting setup. Please create the virtual environment and install dependencies manually."
    exit 1
  fi
else
  echo "Activating existing virtual environment '$VENV_DIR'..."
  source "$VENV_DIR/bin/activate"
fi

# 3) Load config from config.txt
if [[ ! -f "config.txt" ]]; then
  echo "Error: config.txt not found!"
  exit 1
fi

source config.txt

# Debug: Print loaded variables
echo "Loaded configuration:"
echo "  PSK: $PSK"
echo "  PORT: $PORT"
echo "  INDEX: $INDEX"
echo "  CHANNEL_NAME: $CHANNEL_NAME"

# Check for essential variables
if [[ -z "$PSK" || -z "$PORT" || -z "$INDEX" ]]; then
  echo "Error: PSK, PORT, and INDEX must be set in config.txt"
  exit 1
fi

echo "Applying settings to Meshtastic node on port: $PORT"
echo "Setting channel $INDEX with base64 PSK: $PSK"

# 4) Set the PSK on the chosen channel using the new base64 flag
meshtastic --port "$PORT" --ch-set psk "base64:$PSK" --ch-index "$INDEX"

# 5) (Optional) Set the channel name if provided
if [[ -n "$CHANNEL_NAME" ]]; then
  echo "Naming channel $INDEX as: $CHANNEL_NAME"
  meshtastic --port "$PORT" --ch-set name "$CHANNEL_NAME" --ch-index "$INDEX"
fi

# 6) Reboot the node so it applies the changes
echo "Rebooting the node..."
meshtastic --port "$PORT" --reboot

echo "All done! Your Meshtastic node should now use the specified PSK."
chmod +x nr-sender.sh
chmod +x setup.sh
chmod +x sender.py
chmod +x receiver.py

echo "All necessary scripts have been made executable."
