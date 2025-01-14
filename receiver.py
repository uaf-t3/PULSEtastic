import time
import sys
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

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

config = load_config()

# Get PORT and INDEX from the config, or use defaults
port = config.get("PORT", "/dev/ttyUSB0")

def get_node_info(port):
# Initializing SerialInterface to get node info
    local = SerialInterface(port)
    node_info = local.nodes
    local.close()
# Node info retrieved
    return node_info

def parse_node_info(node_info):
# Parsing node info
    nodes = []
    for node_id, node in node_info.items():
        nodes.append({
            'num': node_id,
            'user': {
                'shortName': node.get('user', {}).get('shortName', 'Unknown')
            }
        })
    return nodes

def on_receive(packet, interface, node_list):
    try:
        if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message = packet['decoded']['payload'].decode('utf-8')
            fromnum = packet['fromId']
            shortname = next((node['user']['shortName'] for node in node_list if node['num'] == fromnum), 'Unknown')
            incomingChannel = packet['channel']
            channel = config.get("INDEX")
        #Uncomment for debugging
            #print("Channel index is: "+str(channel))
            #print("Message incoming  from channel: "+str(incomingChannel))
            if int(incomingChannel) == int(channel):
                print(str(message).strip(), flush=True)
    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():

    # Retrieve and parse node information
    node_info = get_node_info(port)
    node_list = parse_node_info(node_info)


    # Subscribe the callback function to message reception
    def on_receive_wrapper(packet, interface):
        on_receive(packet, interface, node_list)

    pub.subscribe(on_receive_wrapper, "meshtastic.receive")

    # Set up the SerialInterface for message listening
    local = SerialInterface(port)

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Script terminated by user")
        local.close()

if __name__ == "__main__":
    main()