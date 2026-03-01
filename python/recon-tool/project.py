import csv, argparse, ipaddress, socket, sys, pathlib, os, tabulate

PORTS = "services.csv"

def main():
    open = []
    args = parse()
    ports = load_ports(args.file)
    target_ip = validate_target(args.target)
    for port in ports:
        r = scan_port((target_ip, port))
        if r == 0:
            x = {"port" : port}
            y = ports.get(port, {'service': 'Unknown', 'severity' : 'N/A', 'description' : 'No data available'})
            open.append(x | y)
    print(tabulate.tabulate(open, headers = "keys", tablefmt = "grid"))

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
    socket.setdefaulttimeout(1)
    result = s.connect_ex(ipandport)
    s.close()
    return result

if __name__ == "__main__":
    main()