import csv, argparse, ipaddress, socket, sys, pathlib, os, tabulate, pyfiglet
from concurrent import futures
from itertools import repeat

PORTS = "services.csv"

def main():
    open_ports = []
    args = parse()
    banner = pyfiglet.figlet_format("Recon-Tool", font = "doom")
    print(banner)
    ports = load_ports(args.file)
    target_ip = validate_target(args.target)
    with futures.ThreadPoolExecutor() as executor:
        iterator = zip(repeat(target_ip), ports.keys())
        results = executor.map(scan_port, iterator)
        found_ports = zip(ports.keys(), results)
        for port_num, r in found_ports:
            if r == 0:
                x = {"port" : port_num}
                y = ports.get(port_num)
                open_ports.append(x | y)
    print(tabulate.tabulate(open_ports, headers = "keys", tablefmt = "grid"))

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
        sys.exit("Services database not found. Ensure 'services.csv' is in the current directory")
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
            sys.exit("Could not resolve hostname")

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