# Robot Motor & Servo Tester

A local browser-based test bench for Hiwonder HTD-45H bus servos and ZL 370 bus motors. It helps you connect to a serial adapter, verify device IDs, test individual devices, and run short four-wheel drive patterns without sending data to a cloud service.

> **Safety first:** Lift the robot's wheels off the ground before testing. Use the correct external power supply, keep a physical power switch within reach, and verify one wheel at a time. A stop command is not a guaranteed emergency stop.

## Features

- Local Web Serial connection from a supported Chromium-based browser
- Hiwonder servo testing: read status, find or change IDs, move to a position, run briefly, and control torque
- ZL 370 motor testing: read ID, pulses, and firmware information; run forward/reverse timed tests
- Four-wheel mapping with per-wheel IDs and direction inversion
- Normal differential-drive and 45-degree omniwheel patterns
- English and Traditional Chinese interface text
- Downloadable Python examples for command-line testing

## Quick start

1. Open the app in a Chromium-based browser that supports Web Serial.
2. Connect the correct half-duplex serial adapter and external power supply.
3. Open the **Guide & downloads** page and confirm the wiring and voltage for your device.
4. Select **Servo tester**, **Motor tester**, or **Four wheels**.
5. Choose the serial port, set the baud rate (default: `115200`), and connect.
6. Start with the lowest practical speed and the shortest available test duration.

The browser app is static and can be served by any local web server. For example:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000> in the browser. Opening `index.html` directly may prevent JavaScript modules or Web Serial from working correctly.

## Hardware and protocols

The servo and motor buses are different and are **not interchangeable**:

| Device | Protocol | Recommended supply | Typical app workspace |
| --- | --- | --- | --- |
| Hiwonder HTD-45H servo | Binary bus, `0x55` frame header | 9.6–12.6 V | Servo tester |
| ZL 370 motor | ASCII bus commands | 6–8.4 V | Motor tester / Four wheels |

Use the adapter, wiring, power source, and device IDs appropriate for the hardware. Disconnect other serial programs before connecting. The app sends timed test commands, but it cannot confirm that a motor physically stopped or that a motion command completed.

## Four-wheel testing

Configure the four motor IDs in this order:

```text
front-left, front-right, rear-right, rear-left
```

Test and verify every wheel individually before using a coordinated pattern. For normal wheels, use forward, backward, left, and right. For a 45-degree roller chassis, select **Omniwheel** to enable strafe-left and strafe-right. The direction setting can invert each wheel without changing its motor ID.

## Python command-line examples

The `downloads/` directory contains small examples that use the same device families and bus speeds. Install the dependency first:

```bash
cd downloads
python3 -m pip install -r requirements.txt
python3 list_ports.py
```

Windows users can use `py` instead of `python3`:

```powershell
py -m pip install -r requirements.txt
py list_ports.py
```

Examples:

```bash
python3 servo_status.py --port /dev/ttyUSB0 --id 1
python3 servo_move.py --port /dev/ttyUSB0 --id 1 --position 500 --ms 1500
python3 motor_run.py --port /dev/ttyUSB1 --id 0 --speed 100 --seconds 2
python3 four_wheels.py --port /dev/ttyUSB1 --ids 0 1 2 3 --action fl
python3 four_wheels.py --port /dev/ttyUSB1 --ids 0 1 2 3 --mode omni --action strafe-left
```

Run any script with `--help` for all options. Motor speed is a signed PWM offset, not RPM. On Linux, serial-port access may require adding your user to the `dialout` group and then signing in again.

## Project structure

```text
index.html                 Web app layout
app.js                     UI, serial connection, and test actions
protocol.js                Servo and motor packet helpers
style.css                  Interface styling
group-test.js              Group-test validation and controls
downloads/                 Python examples and requirements
```

## Limitations

This project is intended for bench testing and education. Hardware behavior depends on the adapter, wiring, power supply, firmware, motor load, and configured IDs. The examples and interface should be validated on the actual robot before regular use; software success only means that a command was sent or a valid response was received.
