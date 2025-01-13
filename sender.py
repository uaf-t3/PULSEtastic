#!/usr/bin/env python3

import meshtastic
import meshtastic.serial_interface
import sys

def load_config(filename="config.txt"):
    """Load key-value pairs from a simple config file."""
    cfg = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, val = line.split("=", 1)
                cfg[key.strip()] = val.strip().strip('"')
    except FileNotFoundError:
        pass
    return cfg

def main(message):
    # Load the config
    config = load_config()

    # Get PORT and INDEX from the config, or use defaults
    port = config.get("PORT", "/dev/ttyUSB0")
    index_str = config.get("INDEX", "0")
    try:
        channel_index = int(index_str)
    except ValueError:
        channel_index = 0

    # Initialize the Meshtastic interface
    interface = meshtastic.serial_interface.SerialInterface(port)

    try:
        interface.sendText(message, channelIndex=channel_index)
    finally:
        interface.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        main(message)
    else:
        print("No message provided")