import csv, argparse, ipaddress, socket, pathlib, os, time, sys
from concurrent import futures
from itertools import repeat
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

PORTS = "services.csv"
console = Console()

def main():
    open_ports = []
    args = parse()
    ports = load_ports(args.file)
    target_ip = validate_target(args.target)

    console.print(Panel("[magenta]Recon-Tool v1.0[magenta]",
                            subtitle = "Made by Abhishek Karmakar"))
    time.sleep(0.02)
    try:
        with futures.ThreadPoolExecutor() as executor:
            iterator = zip(repeat(target_ip), ports.keys())
            results = executor.map(scan_port, iterator)
            found_ports = zip(ports.keys(), results)
            for port_num, r in found_ports:
                if r == 0:
                    x = {"port" : port_num}
                    y = ports.get(port_num)
                    open_ports.append(x | y)
    except KeyboardInterrupt:
        console.print("\n[red]Scan aborted by user[/red]")
        sys.exit(1)
    else:
        table = Table(title = "Open Ports on Target", title_justify = "center")
        table.add_column("Port")
        table.add_column("Service")
        table.add_column("Severity")
        table.add_column("Description")
        for item in open_ports:
            if item["severity"] == "Low":
                sev_color = "green"
            elif item["severity"] == "Medium":
                sev_color = "yellow"
            elif item["severity"] == "High":
                sev_color = "red"
            else:
                sev_color = "bold red"
            table.add_row(str(item['port']),
                          item['service'],
                          f"[{sev_color}]{item['severity']}[/{sev_color}]",
                          item['description'])

    console.print(f"\n[green]Target[/green]: {target_ip}")
    console.print("[cyan]Scanning targets.... Please wait[/cyan]")
    console.print(table)

        
def parse():
    parser = argparse.ArgumentParser(
        description = """Scan for open ports for the given IP Address or URL""",
        epilog = """Made by Abhishek Karmakar""")
    parser.add_argument("-f", "--file", 
                        help = "Loads the ports from this file. By default set to 'services.csv'",
                        default = PORTS, 
                        type = pathlib.Path)
    parser.add_argument("-t", "--target",
                        help = "Scans the target for the loaded ports. The target could be a URL or an IPv4 Address",
                        type = str,
                        required = True)
    args = parser.parse_args()
    return args

def load_ports(data):
    ports = {}
    if not os.path.isfile(data):
        console.print("[red]Services database not found. Ensure [bold]'services.csv'[/bold] is in the current directory[/red]")
        sys.exit(1)
    with open(data) as file:
        reader = csv.DictReader(file)
        for row in reader:
            port_int = int(row['port'])
            ports[port_int] = {"service" : row['service'], 
                               "severity" : row['severity'], 
                               "description" : row['description']}
    return ports

def validate_target(address):
    socket.setdefaulttimeout(3)
    try:
        ip = ipaddress.ip_address(address)
        return str(ip)
    except ValueError:
        try:
            ip = socket.gethostbyname(address)
            return ip
        except socket.gaierror:
            console.print("[red]Could not resolve hostname[/red]")
            sys.exit(1)

def scan_port(ipandport: tuple):
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    s.settimeout(1)
    result = s.connect_ex(ipandport)
    s.close()
    return result

if __name__ == "__main__":
    main()