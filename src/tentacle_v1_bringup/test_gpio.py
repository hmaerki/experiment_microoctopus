"""
sudo /home/maerki/tmp/fork_picotool/build/picotool load --update -x ~/Downloads/firmware.uf2

pip install mpremote

mpremote run test_gpio.py
"""
from machine import Pin
import time

ACTIVE_LED = "GPIO0"

pin_active_led = Pin(ACTIVE_LED, Pin.OUT)    # create output pin on GPIO0
for _ in range(4):
    pin_active_led.toggle()
    time.sleep(0.5)

gpio_relais= (
     "GPIO1",
     "GPIO2",
     "GPIO3",
     "GPIO4",
     "GPIO8",
)
pin_relais = [Pin(pin, Pin.OUT) for pin in gpio_relais]

if False:
    for _ in range(4):
        for pin in pin_relais:
            pin.toggle()
        time.sleep(10)

if True:
    for i, pin in enumerate(pin_relais):
        print(f"Relais {i}")
        for _ in range(4):
            pin.toggle()
            time.sleep(0.5)
print("Done")