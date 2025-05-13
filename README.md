
![PULSEtastic Logo](https://raw.githubusercontent.com/ItalianSquirel/PULSEtastic/refs/heads/main/assets/pulseLogo.png)

**Some tools to make using your Meshtastic nodes via a serial connection all the easier!**

<img src="https://img.shields.io/badge/Node--Red-8F0000?style=for-the-badge&logo=nodered&logoColor=white" /> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white" /> <img src="https://img.shields.io/badge/MIT-green?style=for-the-badge" />
___
## Overview

PULSEtastic provides a set of tools designed to simplify the use of Meshtastic nodes through a serial connection. This project was originally developed for integration with a **Node-RED flow**, making it even easier to automate and visualize interactions with your Meshtastic network. Example flows and a highly useful Node-RED palette are provided to help you get started.

## Features

- **Serial Communication**: Easily connect and communicate with Meshtastic nodes using a serial interface.
- **Node-RED Integration**: Pre-built Node-RED flows and a custom palette for seamless integration.
- **Private Channel Configuration**: Tools for setting up private channels using PSK (Pre-Shared Key) and other channel details.
- **Python Environment Setup**: Automated setup for creating a Python virtual environment and installing necessary libraries.
- **Terminal-Friendly Demo Scripts**: Example scripts for testing communication directly from the terminal.
- **Node-RED-Compatible Scripts**: Specialized scripts for seamless use with Node-RED.

## Getting Started

### Prerequisites

- **Python**: Ensure Python (preferably version 3.7 or higher) is installed on your system.
- **Shell Environment**: A Unix-like shell environment for executing shell scripts.
- **Meshtastic Nodes**: Ensure you have your Meshtastic hardware ready for communication and enable serial communications in the radio configuration.
- **Node-RED**: Install Node-RED on your system for using the provided flows.

### Setup Instructions

1. **Enable the Serial Port** *(Raspberry Pi only)*:

   If you're using a Raspberry Pi, you first need to enable the serial port:

   - Open the Raspberry Pi Configuration tool.
   - Go to the **Interfaces** tab.
   - Enable the **Serial Port**.
   - Reboot the Raspberry Pi to apply the changes.

   *Note*: If you're not using a Raspberry Pi, you can skip this step.

2. **Clone the Repository**:

   ```bash
   git clone https://github.com/uaf-t3/PULSEtastic.git
   cd PULSEtastic
   ```

3. **Edit the Configuration**:

   The configuration file `config.txt` determines the Meshtastic private channel to connect to, and the path to the device for serial connection. This defaults to the `PulseTest` channel.
   To change the channel or serial port, open the `config.txt` file and adjust the parameters:

   ```bash
   nano config.txt
   ```

   In `config.txt`, you can set the following:

   - **PSK**: Pre-Shared Key for the private channel.
   - **CHANNEL_NAME**: The name of the channel.
   - **INDEX**: The channel index used by your Meshtastic device.
   - **PORT**: The path to the device for serial connection.

5. **Run Setup Script**:

   Execute the `setup.sh` script to set up the environment:

   ```bash
   ./setup.sh
   ```

   *What happens during setup*:
   - The script checks for an existing Python virtual environment in the current directory.
   - If no environment is found, it prompts the user to install one.
   - During the installation, it downloads the required Python libraries, including:
     - **Meshtastic Library**: For interacting with Meshtastic nodes.
     - **PubSub Library**: For handling publish/subscribe messaging patterns.

## Explanation of Tools

### Terminal-Friendly Demo Scripts

- **`senderDemo.py`** and **`receiverDemo.py`**: These scripts are designed for manual testing in a terminal. Both scripts need to be run within the virtual environment created by `setup.sh`.

  To enter the virtual environment, run:

  ```bash
  source meshtastic-env/bin/activate
  ```

  Once inside the virtual environment, you can run the demo scripts:

  ```bash
  python senderDemo.py
  python receiverDemo.py
  ```

  These scripts are useful for quickly testing the functionality of your Meshtastic nodes without relying on Node-RED.

### Node-RED-Compatible Scripts

- **`nr-sender.sh`**: This is a shell script designed to work seamlessly with Node-RED. Its primary purpose is to ensure it runs in the correct Python virtual environment before executing the sender script.
  
  The use of a shell script ensures that Node-RED can invoke the sender functionality without requiring the user to manually activate the virtual environment.

- **`receiver.py`**: This Python script handles data reception and is directly compatible with Node-RED. Unlike the sender, the receiver does not require a shell script because Node-RED can directly execute Python scripts using a special palette node designed for running Python code.

## Node-RED Integration

PULSEtastic was designed to work with Node-RED flows. Example flows are provided in the repository, along with a link to the custom Node-RED palette.

- [**Node-RED Python Node**](https://flows.nodered.org/node/node-red-contrib-pythonshell)
- [**Example Flows**](https://raw.githubusercontent.com/ItalianSquirel/PULSEtastic/refs/heads/main/assets/pulsetasticFlow.json)

Below is a preview of the Node-RED flow:
![Node-RED Flow Example](https://raw.githubusercontent.com/ItalianSquirel/PULSEtastic/refs/heads/main/assets/meshNodes.png)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ItalianSquirel/PULSEtastic/blob/main/LICENSE) file for details.

## Acknowledgments
This project is made possible through the generous support of several funding sources dedicated to fostering innovation, research, and education in Alaska. Special thanks to:  

- **[University of Alaska Fairbanks Undergraduate Research & Scholarly Activity (URSA) program](https://www.uaf.edu/ursa/)** for funding PULSE & STARTRAM supplies.  
- **[UAF Alaska Center for Energy and Power (ACEP)](https://www.uaf.edu/acep/)** for serving as the Cyber Pod research home base.  
- **[Office of Naval Research’s ARCTIC Program](https://thearcticprogram.net/)** for supporting integration into the T3 program (ONR Award # N00014-22-1-2049)  
- **[National Science Foundation’s STORM Project](https://www.uaf.edu/acep/news/2023/acep-and-partners-receive-6-million-to-help-secure-electric-grids.php)** for advancing secure and resilient electric grids in climate-impacted communities (NSF Award #2316402).  
- **[UAF Upward Bound and Alaska T3 Program](https://uaf-ub.alaska.edu/)** for being Target STEM program partners and supporting NPHS T3 student beta testing team.

Their immense help made our research and development possible.

Special thanks to all contributors and the open-source community for their invaluable support and resources.

The code for this project was developed by: 
- Petie Deveer (ORCID iD: 0009-0008-2103-6674).
