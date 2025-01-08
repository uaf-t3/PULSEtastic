#!/usr/bin/env python3

import time
import sys
from meshtastic.serial_interface import SerialInterface

def load_config(filename="config.txt"):
    """Load key-value pairs from config.txt."""
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

def get_node_info(serial_port):
    """Retrieve node information from the connected Meshtastic device."""
    print("Initializing SerialInterface to get node info...")
    local = SerialInterface(serial_port)
    node_info = local.nodes
    local.close()
    print("Node info retrieved.")
    return node_info

def parse_node_info(node_info):
    """Parse node information to map node IDs to short names."""
    print("Parsing node info...")
    nodes = {}
    for node_id, node in node_info.items():
        short_name = node.get("user", {}).get("shortName", "Unknown")
        nodes[node_id] = short_name
    print("Node info parsed.")
    return nodes

def on_receive(packet, desired_index, node_list):
    """
    Callback for incoming packets.
    Prints messages only if they are on the desired channel index.
    """
    try:
        # Debug: Print the entire packet
        print("\n=== Packet Received ===")
        print(packet)

        # Check if it's a text message
        decoded = packet.get('decoded', {})
        portnum = decoded.get('portnum', '')

        if portnum == 'TEXT_MESSAGE_APP':
            # Get channel (field is 'channel' not 'channelIndex')
            ch_index = packet.get('channel', packet.get('channelIndex', None))
            print(f"[DEBUG] Packet channel: {ch_index} (type: {type(ch_index)})")
            print(f"[DEBUG] Desired index: {desired_index} (type: {type(desired_index)})")
            print(f"[DEBUG] Comparing: {ch_index == desired_index}")
            if ch_index == desired_index:
                # Get text
                text = decoded.get('text', '')
                from_id = packet.get('fromId', 'Unknown')
                sender = node_list.get(from_id, 'UnknownSender')
                print(f"** Received TEXT on channel {ch_index} from {sender} ({from_id}): {text}")
            else:
                print(f"[DEBUG] Packet channel {ch_index} != desired {desired_index}. Ignored.")
    except KeyError as e:
        print(f"[DEBUG] KeyError encountered: {e}. Packet skipped.")
    except UnicodeDecodeError:
        print("[DEBUG] UnicodeDecodeError encountered. Packet skipped.")

def main():
    # Load configuration
    config = load_config("config.txt")
    serial_port = config.get("PORT", "/dev/ttyUSB0")
    index_str = config.get("INDEX", "0")

    try:
        desired_index = int(index_str)
    except ValueError:
        print(f"Invalid INDEX '{index_str}' in config. Defaulting to 0.")
        desired_index = 0

    print(f"Using serial port: {serial_port}")
    print(f"Filtering for channel index: {desired_index}")

    # Retrieve and parse node information
    node_info = get_node_info(serial_port)
    node_list = parse_node_info(node_info)

    print("Known Nodes:")
    for node_id, short_name in node_list.items():
        print(f"  {node_id}: {short_name}")

    # Initialize the SerialInterface for listening
    try:
        listener_iface = SerialInterface(serial_port)
        print("SerialInterface setup for listening.")
    except Exception as e:
        print(f"Failed to connect to {serial_port}: {e}")
        sys.exit(1)

    # Assign the on_receive callback directly
    listener_iface.onReceive += lambda packet, iface: on_receive(packet, desired_index, node_list)

    print("Listening for incoming messages. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting receiver...")
    finally:
        listener_iface.close()

if __name__ == "__main__":
    main()
