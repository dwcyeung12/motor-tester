"""Move a Hiwonder servo to a position. Clear the shaft before use."""
import argparse
from bus_protocol import open_bus, packet
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--port', required=True)
p.add_argument('--id', type=int, default=1, choices=range(254))
p.add_argument('--position', type=int, default=500, choices=range(1001), metavar='0-1000')
p.add_argument('--ms', type=int, default=1500)
p.add_argument('--baud', type=int, default=115200)
a = p.parse_args()
if not 20 <= a.ms <= 30000:
    p.error('--ms must be 20–30000')
with open_bus(a.port, a.baud) as bus:
    try:
        bus.write(packet(a.id, 29, b'\x00\x00\x00\x00'))
        bus.write(packet(a.id, 31, b'\x01'))
        bus.write(packet(a.id, 1, a.position.to_bytes(2, 'little') + a.ms.to_bytes(2, 'little')))
        print('Move command sent; motion is not confirmed.')
    except BaseException:
        bus.write(packet(a.id, 12))
        raise
