#!/usr/bin/env bash
#
# setup.sh - Configure a Meshtastic node by directly using a base64 PSK.
#            Reads PSK, PORT, INDEX, and optional CHANNEL_NAME from config.txt,
#            then sets the channel PSK and (optionally) name.

set -e  # Exit on error

# 1) Load config from config.txt
if [[ ! -f "config.txt" ]]; then
  echo "Error: config.txt not found!"
  exit 1
fi

source config.txt

# Check for essential variables
if [[ -z "$PSK" || -z "$PORT" || -z "$INDEX" ]]; then
  echo "Error: PSK, PORT, and INDEX must be set in config.txt"
  exit 1
fi

echo "Applying settings to Meshtastic node on port: $PORT"
echo "Setting channel $INDEX with base64 PSK: $PSK"

# 2) Set the PSK on the chosen channel using the new base64 flag
meshtastic --port "$PORT" --ch-set psk "base64:$PSK" --ch-index "$INDEX"

# 3) (Optional) Set the channel name if provided
if [[ -n "$CHANNEL_NAME" ]]; then
  echo "Naming channel $INDEX as: $CHANNEL_NAME"
  meshtastic --port "$PORT" --ch-set name "$CHANNEL_NAME" --ch-index "$INDEX"
fi

# 4) Reboot the node so it applies the changes
echo "Rebooting the node..."
meshtastic --port "$PORT" --reboot

echo "All done! Your Meshtastic node should now use the specified PSK."
