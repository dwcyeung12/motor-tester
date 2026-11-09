# Robot motor and servo examples / 機器人馬達與舵機範例

The Hiwonder HTD-45H servo and ZL 370 motor use different, incompatible protocols. Use the correct half-duplex adapter, correct wiring and separate external power. HTD-45H: 9.6–12.6 V. ZL 370: 6–8.4 V. Lift wheels, clear moving parts and keep a physical power switch available. These examples have not been verified on physical hardware. A STOP command is not a guaranteed emergency stop.

Hiwonder HTD-45H 舵機與 ZL 370 馬達使用不同、不能互換的通訊協定。請使用正確半雙工轉接器、接線及外接電源。HTD-45H：9.6–12.6 V；ZL 370：6–8.4 V。將車輪架空，清除活動部件附近的障礙物，並準備實體電源開關。這些範例尚未經實體硬體驗證；停止指令不能保證緊急停止。

Windows:
```
py -m pip install -r requirements.txt
py list_ports.py
py servo_status.py --port COM3 --id 1
py servo_move.py --port COM3 --id 1 --position 500
py motor_run.py --port COM4 --id 0 --speed 100 --seconds 2
py four_wheels.py --port COM4 --ids 0 1 2 3 --action fl
```
Linux:
```
python3 -m pip install -r requirements.txt
python3 list_ports.py
python3 servo_status.py --port /dev/ttyUSB0 --id 1
python3 motor_run.py --port /dev/ttyUSB1 --id 0 --speed 100 --seconds 2
python3 four_wheels.py --port /dev/ttyUSB1 --ids 0 1 2 3 --action fl
```
Run each script with `--help` for options. Set IDs and directions to match the robot and verify each wheel individually before using coordinated movement. For example, add `--mode omni --action strafe-left` for a 45° roller chassis. The IDs are in FL FR RR RL order. The speed value is a PWM offset, not RPM. Disconnect other programs from the port first.

使用 `--help` 查看各程式的選項。依機器人設定 ID 和方向，在整車移動前逐一確認車輪。例如 45° 滾輪車可使用 `--mode omni --action strafe-left`。ID 次序為左前、右前、右後、左後。速度為 PWM 偏移值，並非 RPM。請先關閉其他佔用序列埠的程式。

Linux: if access is denied, run `sudo usermod -aG dialout "$USER"`, then log out and back in. / 如 Linux 權限不足，執行此指令後登出再登入。
