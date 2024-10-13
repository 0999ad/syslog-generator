import random
import socket
import time
import requests
import logging
from rich.console import Console
from rich.prompt import Prompt
from rich import print

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MAX_IP_COUNT = 20000
RFC1918_RANGES = [
    ('10.0.0.0', '10.255.255.255'),
    ('172.16.0.0', '172.31.255.255'),
    ('192.168.0.0', '192.168.255.255')
]
COMMON_PORTS = [80, 443, 389, 53, 22]

console = Console()

# SyslogSimulator class definition remains unchanged...

def get_syslog_type():
    """Prompt the user to select a syslog type using numbered choices."""
    console.print("\n[bold]Choose the syslog format:[/bold]")
    console.print("1 - Cisco ASA")
    console.print("2 - Snare Windows 2008 Event log")
    console.print("3 - MS Windows Event Logging XML")
    console.print("4 - AWS")
    console.print("5 - Nessus")
    console.print("6 - Netflow")
    console.print("7 - eStreamer")
    console.print("8 - Check Point")

    while True:
        choice = Prompt.ask("Enter the number corresponding to the syslog type", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")
        syslog_types = {
            "1": "Cisco ASA",
            "2": "Snare Windows 2008 Event log",
            "3": "MS Windows Event Logging XML",
            "4": "AWS",
            "5": "Nessus",
            "6": "Netflow",
            "7": "eStreamer",
            "8": "Check Point"
        }
        return syslog_types[choice]

def main():
    console.print("[bold blue]Welcome to the Syslog Simulator![/bold blue]\n")
    url = Prompt.ask("[bold cyan]Enter the URL with a list of external IP addresses[/bold cyan]", default="http://example.com/iplist")
    splunk_ip = Prompt.ask("[bold cyan]Enter the IP address of the Splunk server[/bold cyan]", default="192.168.1.100")
    
    live_ip_percentage = float(Prompt.ask("[bold cyan]Enter the percentage of traffic using live (external) IPs (0.1 to 99.99)[/bold cyan]", default="10.0"))
    
    # Get the syslog type before creating the simulator object
    log_type = get_syslog_type()
    
    # Create the simulator with the selected syslog type
    simulator = SyslogSimulator(splunk_ip, url, live_ip_percentage, log_type)
    
    # Get the logging speed
    delay_range = simulator.get_logging_speed()
    
    # Start the simulation
    simulator.start_simulation(delay_range)

if __name__ == "__main__":
    main()
