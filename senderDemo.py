#!/usr/bin/env python3

import meshtastic
import meshtastic.serial_interface

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
        print(f"Warning: {filename} not found. Using defaults.")
    return cfg

def main():
    # Load the config
    config = load_config()

    # Get PORT and INDEX from the config, or use defaults
    port = config.get("PORT", "/dev/ttyUSB0")
    index_str = config.get("INDEX", "0")
    try:
        channel_index = int(index_str)
    except ValueError:
        print(f"Invalid INDEX in config ({index_str}), defaulting to 0.")
        channel_index = 0

    # Initialize the Meshtastic interface
    interface = meshtastic.serial_interface.SerialInterface(port)

    print(f"Meshtastic node ready on port {port}, channel index {channel_index}.")
    print("Enter a message and press Enter to send. Press Ctrl+C to exit.")

    try:
        while True:
            message = input("Type your message: ")
            interface.sendText(message, channelIndex=channel_index)
            print("Message sent!")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        interface.close()

if __name__ == "__main__":
    main()
