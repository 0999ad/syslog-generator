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

class SyslogSimulator:
    def __init__(self, splunk_ip, url, live_ip_percentage, log_type, max_ip_count=MAX_IP_COUNT):
        self.splunk_ip = splunk_ip
        self.url = url
        self.live_ip_percentage = live_ip_percentage
        self.log_type = log_type
        self.max_ip_count = max_ip_count
        self.external_ips = self.fetch_external_ips()
        self.ip_list = self.generate_ip_list()
        self.speed_options = {
            1: (5, 120),  # Snail Speed
            2: (2, 5),    # Slow
            3: (1, 2),    # Medium
            4: (0.5, 1),  # Fast
            5: (0.1, 0.5), # Super Fast
            6: (0, 0)     # Armageddon Speed
        }
        self.syslog_port = 514  # Default syslog port for UDP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket for syslog

    def fetch_external_ips(self):
        """Fetch a list of external IPs from a given URL and limit to max_ip_count."""
        try:
            logging.info(f"Fetching external IPs from {self.url}")
            response = requests.get(self.url, verify=False)
            response.raise_for_status()
            ip_list = response.text.strip().splitlines()
            logging.info(f"Fetched {len(ip_list)} external IPs.")
            return ip_list[:self.max_ip_count]
        except requests.RequestException as e:
            console.print(f"[red]Error fetching external IPs: {e}[/red]")
            return []

    def generate_ip_list(self):
        """Generate a combined list of external and RFC1918 IPs."""
        rfc1918_ips = [self.generate_rfc1918_ip() for _ in range(50)]
        return self.external_ips + rfc1918_ips

    @staticmethod
    def generate_rfc1918_ip():
        """Generate a random RFC1918 private IP address."""
        range_choice = random.choice(RFC1918_RANGES)
        ip_parts = [int(octet) for octet in range_choice[0].split('.')]
        for i in range(4):
            ip_parts[i] += random.randint(0, int(range_choice[1].split('.')[i]) - ip_parts[i])
        return '.'.join(map(str, ip_parts))

    def choose_source_and_destination_ips(self):
        """Randomly choose source and destination IPs based on the live IP percentage."""
        if random.random() < self.live_ip_percentage / 100:  # Use live IP
            src_ip = random.choice(self.external_ips)
        else:  # Use RFC1918 IP
            src_ip = self.generate_rfc1918_ip()
        
        # Always generate a matching RFC1918 destination IP for inbound/outbound simulation
        dest_ip = self.generate_rfc1918_ip()

        return src_ip, dest_ip

    def format_syslog_message(self, src_ip, dest_ip, src_port, dest_port):
        """Generate a syslog message based on the chosen log type."""
        timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())
        if self.log_type == "Cisco ASA":
            return (
                f"{timestamp} {self.splunk_ip} : %ASA-6-302015: Built outbound TCP connection "
                f"{random.randint(100000, 999999)} for outside:{src_ip}/{src_port} to inside:{dest_ip}/{dest_port}"
            )
        elif self.log_type == "Snare Windows 2008 Event log":
            return (
                f"{timestamp} {self.splunk_ip} MSWinEventLog 5 Security 600 None {random.randint(1000000, 9999999)} "
                f"{src_ip} Administrator {dest_ip} - User authentication succeeded"
            )
        elif self.log_type == "MS Windows Event Logging XML":
            return (
                f"{timestamp} {self.splunk_ip} <Event><System><EventID>{random.randint(1000, 9999)}</EventID><Level>4</Level>"
                f"<Provider Name='Microsoft-Windows-Security-Auditing'/><EventRecordID>{random.randint(50000, 100000)}</EventRecordID></System>"
                f"<EventData><Data>{src_ip}</Data><Data>{dest_ip}</Data></EventData></Event>"
            )
        elif self.log_type == "AWS":
            return (
                f"{timestamp} {self.splunk_ip} AWSCloudTrail [INFO] Event {random.randint(1000, 9999)}: "
                f"Action performed by {src_ip} targeting {dest_ip}"
            )
        elif self.log_type == "Nessus":
            return (
                f"{timestamp} Nessus Scan Report: Host {src_ip} scanned, vulnerability detected on port {dest_port}"
            )
        elif self.log_type == "Netflow":
            return (
                f"{timestamp} Netflow Event: {src_ip}:{src_port} -> {dest_ip}:{dest_port} "
                f"Protocol TCP, {random.randint(1000, 10000)} bytes transferred"
            )
        elif self.log_type == "eStreamer":
            return (
                f"{timestamp} eStreamer: Alert triggered from {src_ip} to {dest_ip}, Event ID {random.randint(10000, 99999)}"
            )
        elif self.log_type == "Check Point":
            return (
                f"{timestamp} CheckPoint Log: Accept packet from {src_ip} to {dest_ip}, Action accept"
            )
        else:
            return f"{timestamp} {src_ip} -> {dest_ip} : No specific log type"

    def send_syslog_message(self, message):
        """Send the syslog message to the specified IP over port 514 using UDP."""
        try:
            self.socket.sendto(message.encode('utf-8'), (self.splunk_ip, self.syslog_port))
            logging.info(f"Sent syslog message to {self.splunk_ip}:{self.syslog_port}")
        except Exception as e:
            logging.error(f"Error sending syslog message: {e}")

    def simulate_syslog_event(self):
        """Simulate and send a syslog event to the external IP."""
        src_ip, dest_ip = self.choose_source_and_destination_ips()
        src_port = random.randint(1024, 65535)
        dest_port = random.choice(COMMON_PORTS)

        log_message = self.format_syslog_message(src_ip, dest_ip, src_port, dest_port)
        self.send_syslog_message(log_message)

    def get_logging_speed(self):
        """Prompt the user to choose a logging speed and return the corresponding delay range."""
        console.print("\n[bold]Choose the logging speed:[/bold]")
        console.print("1 - Snail (5 to 120 seconds)")
        console.print("2 - Slow (2 to 5 seconds)")
        console.print("3 - Medium (1 to 2 seconds)")
        console.print("4 - Fast (0.5 to 1 second)")
        console.print("5 - Super Fast (0.1 to 0.5 seconds)")
        console.print("[bold red]6 - Armageddon Speed (No delay, constant log generation)[/bold red]")

        while True:
            choice = Prompt.ask("Enter the number corresponding to the logging speed", choices=["1", "2", "3", "4", "5", "6"], default="3")
            choice = int(choice)
            if choice == 6:
                confirm = Prompt.ask(
                    "[bold red]Warning: Armageddon Speed generates logs continuously without delay. "
                    "This can overwhelm your system or network. Do you wish to continue? (yes/no)[/bold red]", 
                    choices=["yes", "no"], default="no"
                )
                if confirm == "yes":
                    return self.speed_options[choice]
                else:
                    console.print("[yellow]Please choose another logging speed.[/yellow]\n")
            else:
                return self.speed_options[choice]

    def get_syslog_type(self):
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

    def start_simulation(self, delay_range):
        """Start the syslog event simulation based on the selected delay."""
        try:
            while True:
                self.simulate_syslog_event()
                if delay_range != (0, 0):  # Only delay if not in Armageddon Speed mode
                    time.sleep(random.uniform(*delay_range))
        except KeyboardInterrupt:
            console.print("\n[green]Simulation stopped by user.[/green]")
        finally:
            self.socket.close()  # Ensure socket is closed

def main():
    console.print("[bold blue]Welcome to the Syslog Simulator![/bold blue]\n")
    url = Prompt.ask("[bold cyan]Enter the URL with a list of external IP addresses[/bold cyan]", default="http://example.com/iplist")
    splunk_ip = Prompt.ask("[bold cyan]Enter the IP address of the Splunk server[/bold cyan]", default="192.168.1.100")
    
    live_ip_percentage = float(Prompt.ask("[bold cyan]Enter the percentage of traffic using live (external) IPs (0.1 to 99.99)[/bold cyan]", default="10.0"))
    
    log_type = simulator.get_syslog_type()
    
    simulator = SyslogSimulator(splunk_ip, url, live_ip_percentage, log_type)
    delay_range = simulator.get_logging_speed()
    simulator.start_simulation(delay_range)

if __name__ == "__main__":
    main()
