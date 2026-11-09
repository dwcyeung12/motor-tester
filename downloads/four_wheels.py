"""Test four ZL 370 motors. Order: front-left, front-right, rear-right, rear-left."""
import argparse
from bus_protocol import open_bus, timed_motors
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--port', required=True)
p.add_argument('--ids', nargs=4, type=int, required=True, metavar=('FL','FR','RR','RL'))
p.add_argument('--directions', nargs=4, type=int, default=[1,1,1,1], metavar=('FL','FR','RR','RL'), help='per-wheel direction, each 1 or -1')
p.add_argument('--mode', choices=['normal','omni'], default='normal')
p.add_argument('--action', choices=['fl','fr','rr','rl','forward','back','left','right','strafe-left','strafe-right'], required=True)
p.add_argument('--speed', type=int, default=100)
p.add_argument('--seconds', type=float, default=2)
p.add_argument('--baud', type=int, default=115200)
a = p.parse_args()
if len(set(a.ids)) != 4 or any(not 0 <= i <= 254 for i in a.ids): p.error('four unique IDs from 0 to 254 are required')
if any(d not in (-1,1) for d in a.directions): p.error('directions must be 1 or -1')
if not 0 <= a.speed <= 1000: p.error('speed must be 0–1000')
patterns = {'fl':[1,0,0,0], 'fr':[0,1,0,0], 'rr':[0,0,1,0], 'rl':[0,0,0,1], 'forward':[1,1,1,1], 'back':[-1,-1,-1,-1], 'left':[-1,1,1,-1], 'right':[1,-1,-1,1], 'strafe-left':[-1,1,-1,1], 'strafe-right':[1,-1,1,-1]}
if a.mode == 'normal' and a.action.startswith('strafe'): p.error('strafe requires omni mode')
print('Lift the robot. Verify each individual wheel direction before using coordinated movement.')
outputs = [(a.ids[i], v * a.directions[i] * a.speed) for i, v in enumerate(patterns[a.action]) if v]
with open_bus(a.port, a.baud) as bus:
    timed_motors(bus, outputs, a.seconds)
