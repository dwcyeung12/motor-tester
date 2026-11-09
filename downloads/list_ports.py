"""List serial ports. Run: python list_ports.py"""
from serial.tools import list_ports
for port in list_ports.comports():
    print(f'{port.device}: {port.description}')
