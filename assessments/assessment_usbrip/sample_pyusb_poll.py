import time
import usb.core
import usb.util

# lsusb -d 2e8a:0005 -v

RP2_VENDOR = 0x2E8A
RP2_PRODUCT_BOOT_MODE = 0x0003
RP2_PRODUCT_APPLICATION_MODE = 0x0005


def main():
    begin_s = time.monotonic()
    for dev in usb.core.find(
        find_all=True,
        idVendor=RP2_VENDOR,
    ):
        mode = "BOOT" if dev.idProduct == RP2_PRODUCT_BOOT_MODE else "APPLICATION"
        print(f"*********** {dev.bus=} {dev.address=} {mode=}")
        # print(dev)

    print(f"*********** duration={time.monotonic()-begin_s:0.3f}s")


if __name__ == "__main__":
    main()
