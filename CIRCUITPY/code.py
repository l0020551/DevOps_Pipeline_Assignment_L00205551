import time
import board
import digitalio
import busio
import displayio
import terminalio
import digitalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Dynamic display bus importer (Handles all CircuitPython 8.x, 9.x, and 10.x firmware styles)
try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    try:
        from displayio import I2CDisplay as I2CDisplayBus
    except ImportError:
        # Fallback for alternative structures
        from displayio import FourWire as I2CDisplayBus

print("--- INITIALIZING BIOS AUTOMATION SYSTEM ---")


#----- setup LED for user feedback without expansion board. ------

led_red = digitalio.DigitalInOut(board.LED_RED)
led_green = digitalio.DigitalInOut(board.LED_GREEN)
led_blue = digitalio.DigitalInOut(board.LED_BLUE)

led_red.direction = digitalio.Direction.OUTPUT
led_green.direction  = digitalio.Direction.OUTPUT
led_blue.direction  = digitalio.Direction.OUTPUT

## set all LEDs to OFF

def clear_all_LEDs():
    led_blue.value = True
    led_red.value = True
    led_green.value = True

def flash_RED_ERR():
    clear_all_LEDs()
    while (True):
        led_red.value=not led_red.value
        time.sleep(0.25)


# --- 1. SET UP OLED DISPLAY ---
try:
    displayio.release_displays()
    i2c = busio.I2C(board.SCL, board.SDA) # XIAO Expansion uses default HW I2C pins
    
    # Initialize using the dynamically imported bus class
    display_bus = I2CDisplayBus(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    # Create a display group and text label
    splash = displayio.Group()
    display.root_group = splash
    print("Display initialized successfully.")
except Exception as e:
    print(f"Display Init Failed: {e}. Continuing script via Serial Only...")
    splash = None

def update_screen(text_message):
    """Prints status to serial console and refreshes the OLED if available."""
    print(f"[STATUS] {text_message}")
    if splash is not None:
        while len(splash) > 0:
            splash.pop()
        
        # Header Banner
        title_area = label.Label(terminalio.FONT, text=" SET PXE ", color=0xFFFFFF, x=10, y=15)
        splash.append(title_area)
        
        # Current Stage Text
        text_area = label.Label(terminalio.FONT, text=text_message, color=0xFFFFFF, x=10, y=40)
        splash.append(text_area)

# --- 2. SET UP HARDWARE PINS & HID ---
power_pin = digitalio.DigitalInOut(board.D1)
power_pin.direction = digitalio.Direction.OUTPUT
power_pin.value = False

# Initialize Native USB Keyboard
try:
    kbd = Keyboard(usb_hid.devices)
    print("USB HID Keyboard initialized successfully.")
except Exception as e:
    print(f"USB HID Init Failed: {e}")

def goToPwrPnl():
    led_green.value= not led_green.value
    time.sleep(0.5)
    led_green.value= not led_green.value
    update_screen("goto advanced")
    kbd.send(Keycode.RIGHT_ARROW)
    return

def goToAdvPnl():
    led_green.value= not led_green.value
    time.sleep(0.5)
    led_green.value= not led_green.value
    update_screen("goto pwr mgr")
    for i in range(7):
        led_green.value= not led_green.value
        time.sleep(0.2)
        led_green.value= not led_green.value
        kbd.send(Keycode.DOWN_ARROW)
    led_green.value= not led_green.value
    time.sleep(0.2)
    led_green.value= not led_green.value
    kbd.send(Keycode.ENTER)
    return

def goToPXE_Toggle():
    led_green.value= not led_green.value
    time.sleep(0.5)
    led_green.value= not led_green.value
    update_screen("enable pxe select")
    for i in range(6):
        led_green.value= not led_green.value
        time.sleep(0.2)
        led_green.value= not led_green.value
        kbd.send(Keycode.DOWN_ARROW)
    led_green.value= not led_green.value
    time.sleep(0.2)
    led_green.value= not led_green.value
    kbd.send(Keycode.ENTER)
    led_green.value= not led_green.value
    time.sleep(0.2)
    led_green.value= not led_green.value
    kbd.send(Keycode.UP_ARROW)
    led_green.value= not led_green.value
    time.sleep(0.2)
    led_green.value= not led_green.value
    kbd.send(Keycode.ENTER)
    led_green.value= not led_green.value
    time.sleep(1.0)
    led_green.value= not led_green.value
    return


# --- 3. EXECUTION SEQUENCE ---
def execute_sequence():
    try:
        clear_all_LEDs()
        # Phase 1: Trigger the Hardware Power Button
        update_screen("Triggering Power...")
        power_pin.value = True   # Drive high to close transistor switch
        #time.sleep(0.5)          # Hold for 500ms
        power_pin.value = False  # Release switch
        
        # Phase 2: Enter the LattePanda BIOS
        update_screen("Entering BIOS...")
        led_blue.value=False
        # Spam DELETE key for roughly 10 seconds to catch the POST screen
        for i in range(20):
            kbd.send(Keycode.DELETE)
            led_blue.value=not led_blue.value
            time.sleep(0.5)
            led_blue.value=not led_blue.value

        led_blue.value=True
        led_green.value=False
        # Phase 3: Wait for BIOS layout to fully render
        update_screen("Navigating Setup")
        led_green.value= not led_green.value
        time.sleep(1.0)  # Move right to the Exit/Save tab
        led_green.value= not led_green.value
        goToPwrPnl()
        goToAdvPnl()
        goToPXE_Toggle()

        # Phase 4: Reset configuration defaults
        update_screen("Resetting Defaults")
        kbd.send(Keycode.ENTER)       # Open confirmation modal
        time.sleep(0.5)
        kbd.send(Keycode.ENTER)       # Select "Yes"
        time.sleep(1.0)

        # Phase 5: Save and Exit
        update_screen("Saving & Exiting")
        time.sleep(1.0)
        kbd.send(Keycode.F4)         # Direct hotkey to Save changes
        time.sleep(0.5)
        kbd.send(Keycode.ENTER)       # Final confirm

        update_screen("Sequence Complete")
        time.sleep(5)
        flash_RED_ERR()
    except:
        flash_RED_ERR()

# Execute immediately on boot
time.sleep(2.0) # Grace period for USB attachment
execute_sequence()

# Stay completely idle so the script doesn't repeat automatically
print("Entering standby mode.")
while True:
    time.sleep(1)