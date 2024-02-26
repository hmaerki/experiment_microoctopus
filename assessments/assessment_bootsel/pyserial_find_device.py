from serial.tools import list_ports

for port in list_ports.comports(include_links=False):
    print(port)
