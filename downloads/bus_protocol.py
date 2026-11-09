"""Shared, minimal protocol helpers for the downloadable examples."""
import math
import time
import serial

def packet(device, command, params=b''):
    if not 0 <= device <= 254:
        raise ValueError('servo ID must be 0–254')
    payload = bytes([device, len(params) + 3, command]) + params
    return b'\x55\x55' + payload + bytes([(~sum(payload)) & 255])

def motor(device, pwm, seconds=0):
    if not 0 <= device <= 255 or not 500 <= pwm <= 2500 or not 0 <= seconds <= 9999:
        raise ValueError('motor ID, PWM or duration out of range')
    return f'#{device:03d}P{pwm:04d}T{seconds:04d}!'.encode('ascii')

def ask_servo(port, device, command, count):
    port.reset_input_buffer()
    port.write(packet(device, command))
    buf = bytearray()
    end = time.monotonic() + 0.6
    while time.monotonic() < end:
        buf.extend(port.read(port.in_waiting or 1))
        while len(buf) >= 4:
            if buf[:2] != b'\x55\x55':
                del buf[0]
                continue
            length = buf[3]
            if not 3 <= length <= 64:
                del buf[0]
                continue
            size = length + 3
            if len(buf) < size:
                break
            frame = buf[:size]
            if frame[-1] != (~sum(frame[2:-1]) & 255):
                del buf[0]
                continue
            del buf[:size]
            if frame[2] == device and frame[4] == command and len(frame[5:-1]) >= count:
                return int.from_bytes(frame[5:5+count], 'little')
    raise TimeoutError('No valid response. Check power, ID, wiring and adapter RX.')

def checked_time(value):
    value = float(value)
    if not 0.2 <= value <= 10:
        raise ValueError('duration must be 0.2–10 seconds')
    return value

def open_bus(port, baud):
    return serial.Serial(port, baudrate=baud, timeout=0.025, write_timeout=0.3)

def timed_motors(port, outputs, seconds):
    seconds = checked_time(seconds)
    try:
        for device, speed in outputs:
            if not 0 <= device <= 254 or not -1000 <= speed <= 1000:
                raise ValueError('motor ID or speed out of range')
            port.write(motor(device, 1500 + speed, math.ceil(seconds)))
        time.sleep(seconds)
    finally:
        port.write(motor(255, 1500))
        port.flush()
