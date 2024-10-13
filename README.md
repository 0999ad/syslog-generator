Here is a `README.md` file that you can use for your GitHub repository. It provides an overview of the project, installation steps, usage instructions, and customization options.

### `README.md`

```markdown
# Syslog Traffic Simulator

This Python-based **Syslog Traffic Simulator** is designed to generate and send syslog messages to a specified IP address over UDP (port 514). It supports different syslog types (e.g., Cisco ASA, AWS, Netflow) and allows for configurable logging speeds, live IP percentage, and message formats. This tool can be used for testing syslog ingestion systems like Splunk, ELK, etc.

## Features

- **Supports multiple syslog types**: Cisco ASA, AWS, Nessus, Check Point, Netflow, and more.
- **Configurable logging speed**: From "Snail" to "Armageddon Speed" with no delay.
- **Live IP percentage**: Allows you to specify the percentage of logs that should use live (external) IP addresses.
- **Sends syslog messages over UDP** to a specified IP on port 514.

## Requirements

- Python 3.6 or higher
- The following Python libraries are required:
  - `requests`
  - `rich`

You can install the required dependencies using the following command:

```bash
pip install requests rich
```

## Usage

1. Clone this repository to your local machine.

```bash
git clone https://github.com/your-username/syslog-traffic-simulator.git
cd syslog-traffic-simulator
```

2. Run the syslog simulator:

```bash
python syslog_simulator.py
```

3. The script will guide you through the following steps:
   - **Enter the URL** where external IPs can be fetched (or use the default `http://example.com/iplist`).
   - **Enter the Splunk server IP** where syslog messages will be sent (UDP, port 514).
   - **Select the percentage of live traffic**: You can specify the percentage of syslog messages that should contain live (external) IP addresses.
   - **Select the syslog format**: Choose from a list of syslog types (e.g., Cisco ASA, AWS, Nessus, etc.).
   - **Choose the logging speed**: Select the speed at which syslog messages are generated and sent.

4. The simulator will continuously send syslog messages to the specified IP until interrupted (e.g., by pressing `Ctrl+C`).

## Customization

### Syslog Types Supported

The following syslog types are supported:

1. Cisco ASA
2. Snare Windows 2008 Event Log
3. MS Windows Event Logging XML
4. AWS CloudTrail
5. Nessus Scan
6. Netflow
7. eStreamer
8. Check Point

Each syslog type has its own message format that mimics real-world logs from the respective system.

### Logging Speed

You can choose from the following logging speeds:

1. **Snail**: 5 to 120 seconds delay between messages.
2. **Slow**: 2 to 5 seconds.
3. **Medium**: 1 to 2 seconds.
4. **Fast**: 0.5 to 1 second.
5. **Super Fast**: 0.1 to 0.5 seconds.
6. **Armageddon**: Continuous log generation with no delay.

### Live IP Traffic

You can configure the percentage of syslog messages that use live (external) IPs. For example, if you set the live IP percentage to 10%, 10% of the messages will contain external IPs, while the rest will contain randomly generated internal (RFC1918) IPs.

## Example

Here’s an example session:

```bash
Welcome to the Syslog Simulator!

Enter the URL with a list of external IP addresses: [default: http://example.com/iplist]
Enter the IP address of the Splunk server: 192.168.1.100
Enter the percentage of traffic using live (external) IPs (0.1 to 99.99): 10.0
Choose the syslog format:
1 - Cisco ASA
2 - Snare Windows 2008 Event log
3 - MS Windows Event Logging XML
4 - AWS
5 - Nessus
6 - Netflow
7 - eStreamer
8 - Check Point
Enter the number corresponding to the syslog type: 1
Choose the logging speed:
1 - Snail (5 to 120 seconds)
2 - Slow (2 to 5 seconds)
3 - Medium (1 to 2 seconds)
4 - Fast (0.5 to 1 second)
5 - Super Fast (0.1 to 0.5 seconds)
6 - Armageddon Speed (No delay, constant log generation)
Enter the number corresponding to the logging speed: 3

Simulation started! Logs are being sent to 192.168.1.100 over port 514.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request.
```

### Key Sections:
- **Overview**: Introduction to the project, its features, and what it does.
- **Installation**: Simple installation instructions.
- **Usage**: Step-by-step guide on how to run the simulator.
- **Customization**: Describes available syslog types, logging speeds, and live IP traffic options.
- **Example**: Sample session to show what the user can expect.
- **License and Contributions**: Information about the license and how to contribute.

You can copy this `README.md` file into your GitHub repository. Let me know if you'd like to make any adjustments!
