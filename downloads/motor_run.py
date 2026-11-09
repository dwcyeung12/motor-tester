"""Run one ZL 370 motor briefly, then send broadcast STOP."""
import argparse
from bus_protocol import open_bus, timed_motors
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--port', required=True)
p.add_argument('--id', type=int, default=0, choices=range(255), metavar='0-254')
p.add_argument('--speed', type=int, default=100, help='signed PWM offset: -1000 to 1000')
p.add_argument('--seconds', type=float, default=2)
p.add_argument('--baud', type=int, default=115200)
a = p.parse_args()
print('Lift wheels; keep a physical power switch within reach. Command sent is not confirmation.')
with open_bus(a.port, a.baud) as bus:
    timed_motors(bus, [(a.id, a.speed)], a.seconds)
