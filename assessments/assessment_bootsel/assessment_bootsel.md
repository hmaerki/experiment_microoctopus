# Assessment: Automated update of firmware

## Explore rp2040

* rp2040 FS mode:

  Micropython 1.23
  idVendor=2e8a, idProduct=0005
  SerialNumber: e6609103c36d7f26

* rp2040 in BOOTSEL mode:
  
  New USB device found, idVendor=2e8a, idProduct=0003
  New USB device strings: Mfr=1, Product=2, SerialNumber=3
  Product: RP2 Boot
  Manufacturer: Raspberry Pi
  SerialNumber: E0C912952D54 (this is hardcoded...)


## Assessment

https://forums.raspberrypi.com/viewtopic.php?t=336083

### USB Reset

```bash
# Using the Pico's <vid>:<pid> when stdio_usb is enabled
# See https://github.com/raspberrypi/usb-pid
$ sudo usbreset 2e8a:000a
```

* rp2040 in BOOTSEL mode
* `sudo usbreset 2e8a:0003`
* rp2040 resets and stays in BOOSEL mode


## Draft

* picotool
* usb hub with powerswitch
* configuration
  rp2040 serial: bootsel mode
  rp2040 serial: run mode
  usb hub port rp2040

### virgin board

* power up
* Use `pyusb` to find rp2040 serial
* TODO: find corresponding `picotool --address`
