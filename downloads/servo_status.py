"""Read Hiwonder servo position, temperature, voltage and torque."""
import argparse
from bus_protocol import open_bus, ask_servo
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--port', required=True, help='COM3 or /dev/ttyUSB0')
p.add_argument('--id', type=int, default=1, choices=range(254))
p.add_argument('--baud', type=int, default=115200)
a = p.parse_args()
with open_bus(a.port, a.baud) as bus:
    for name, cmd, count in [('Position', 28, 2), ('Temperature C', 26, 1), ('Voltage mV', 27, 2), ('Torque', 32, 1)]:
        try:
            print(f'{name}: {ask_servo(bus, a.id, cmd, count)}')
        except TimeoutError as exc:
            print(f'{name}: {exc}')
