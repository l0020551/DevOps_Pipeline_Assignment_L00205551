
import sys
import time
import board
import digitalio
import usb_hid

import os
import sys

# Get the directory of injector.py (src/)
src_dir = os.path.dirname(os.path.abspath(__file__))

# Move up one level to the project root directory where 'lib' actually lives
project_root = os.path.dirname(src_dir)
sys.path.append(project_root)

# Now Python can see the 'lib' folder properly
from lib.Adafruit_CircuitPython_HID.adafruit_hid.keyboard import Keyboard
from lib.Adafruit_CircuitPython_HID.adafruit_hid.keyboard import Keyboard
from lib.Adafruit_CircuitPython_HID.adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from lib.Adafruit_CircuitPython_HID.adafruit_hid.keyboard import Keycode

 

# Initialize USB HID
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set D0 as a trigger input
trigger = digitalio.DigitalInOut(board.D0)
trigger.direction = digitalio.Direction.INPUT
trigger.pull = digitalio.Pull.UP

# Allow Linux to recognize the USB device
time.sleep(3)

while True:
    if not trigger.value:
        time.sleep(0.05)

        if not trigger.value:
            # Send keystrokes
            layout.write("Hello from XIAO nRF52840!")
            keyboard.send(Keycode.ENTER)

            layout.write("CircuitPython HID on Linux")
            keyboard.send(Keycode.ENTER)

            keyboard.send(Keycode.CONTROL, Keycode.A)
            keyboard.release_all()

            # Wait for trigger release
            while not trigger.value:
                time.sleep(0.01)

    time.sleep(0.02)
