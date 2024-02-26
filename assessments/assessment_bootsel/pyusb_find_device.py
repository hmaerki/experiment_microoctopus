"""
Address: ok
Serial number: not
  ValueError: The device has no langid (permission issue, no string descriptors s
  ==> Requires to add udev-rules
"""

import usb.core

# find USB devices
# devices = usb.core.find(find_all=True)
devices = usb.core.find(find_all=True, idVendor=0x2e8a, idProduct=0x0003)
# loop through devices, printing vendor and product ids in decimal and hex
for device in devices:
    # if device.idVendor != 0x2e8a:
    #     continue
    # if device.idProduct != 0x0003:
    #     continue

    try:
        device.set_configuration()
        x = device.get_active_configuration()
    except usb.core.USBError as usb_error:
        if 'Resource busy' in str(usb_error):
            if device.is_kernel_driver_active(0):
                device.detach_kernel_driver(0)
                device.set_configuration()

    print(f"  Vendor=0x{device.idVendor:04X} Product=0x{device.idProduct:04X} Address={device.address}")
    serial = usb.util.get_string(device, device.iSerialNumber)
    device.serial_number
