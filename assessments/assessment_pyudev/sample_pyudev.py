import os
import dataclasses
import select
import subprocess
from typing import List
import pyudev
import time
import pathlib
import syslog


RP2_VENDOR = 0x2E8A
RP2_PRODUCT_BOOT_MODE = 0x0003
RP2_PRODUCT_APPLICATION_MODE = 0x0005

DEVICES = (
    (RP2_VENDOR, RP2_PRODUCT_APPLICATION_MODE),
    (RP2_VENDOR, RP2_PRODUCT_BOOT_MODE),
)
DEVICES_STR = [(f"{v:04x}", f"{p:04x}") for v, p in DEVICES]

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent
DIRECTORY_BIN = DIRECTORY_OF_THIS_FILE / "bin"


@dataclasses.dataclass
class UdevFilter:
    id_vendor: int
    id_product: int
    subsystem: str
    device_type: str
    actions: List[str]
    label: str

    @property
    def id_vendor_str(self) -> str:
        return f"{self.id_vendor:04x}"

    @property
    def id_product_str(self) -> str:
        return f"{self.id_product:04x}"

    def matches(self, device: pyudev.Device) -> bool:
        if device.action not in self.actions:
            return False
        if device.subsystem != self.subsystem:
            return False
        try:
            id_vendor = device.properties["ID_USB_VENDOR_ID"]
            id_product = device.properties["ID_USB_MODEL_ID"]
        except KeyError:
            return False
        if id_vendor != self.id_vendor_str:
            return False
        if id_product != self.id_product_str:
            return False
        if device.device_type != self.device_type:
            return False
        return True


UDEV_FILTERS = (
    UdevFilter(
        id_vendor=RP2_VENDOR,
        id_product=RP2_PRODUCT_BOOT_MODE,
        subsystem="usb",
        device_type="usb_device",
        actions=[
            "add",
        ],
        label="Boot Mode",
    ),
    UdevFilter(
        id_vendor=RP2_VENDOR,
        id_product=RP2_PRODUCT_APPLICATION_MODE,
        subsystem="tty",
        device_type=None,
        actions=[
            "add",
            "remove",
        ],
        label="Application Mone",
    ),
)


def log(entry, eol="\n"):
    global LOG_FILE
    if entry[-1] == "\r":
        entry = entry[:-1]
    print(entry, end=eol, file=LOG_FILE)


def log_print(entry, eol="\n"):
    print(entry, end=eol)
    log(entry, eol=eol)


def is_usb_serial(device, serial_num=None, vendor=None):
    """Checks device to see if its a USB Serial device.

    The caller already filters on the subsystem being "tty".

    If serial_num or vendor is provided, then it will further check to
    see if the serial number and vendor of the device also matches.
    """

    if "ID_VENDOR" not in device:
        return False
    if vendor is not None:
        if not device.properties["ID_VENDOR"].startswith(vendor):
            return False
    if serial_num is not None:
        if device.properties["ID_SERIAL_SHORT"] != serial_num:
            return False
    return True


def extra_info(device):
    extra_items = []
    if "ID_VENDOR" in device:
        extra_items.append("vendor '{0}'".format(device["ID_VENDOR"]))
    if "ID_SERIAL_SHORT" in device:
        extra_items.append("serial '{0}'".format(device["ID_SERIAL_SHORT"]))
    if extra_items:
        return " with " + " ".join(extra_items)
    return ""


def main():
    context = pyudev.Context()
    context.log_priority = syslog.LOG_NOTICE

    monitor = pyudev.Monitor.from_netlink(context)
    monitor.start()
    monitor.filter_by(subsystem="tty")
    monitor.filter_by(subsystem="usb")

    # Otherwise wait for the teensy device to connect
    while True:
        epoll = select.epoll()
        epoll.register(monitor.fileno(), select.POLLIN)
        while True:
            events = epoll.poll()
            for fileno, _ in events:
                if fileno == monitor.fileno():
                    device = monitor.poll()
                    for udev_filter in UDEV_FILTERS:
                        if udev_filter.matches(device):
                            print(
                                f"{device.action=} {device.subsystem=} {device.device_type=} {device.device_node=} {device.time_since_initialized.microseconds}ms"
                            )
                            if udev_filter.subsystem == "tty":
                                print(
                                    f"  serial={device.properties['ID_SERIAL_SHORT']}"
                                )
                            if udev_filter.subsystem == "usb":
                                # Flash the program
                                #
                                # sudo chown root:root bin/picotool
                                # sudo chmod a+s bin/picotool
                                def subprocess_run(args):
                                    begin_s = time.monotonic()
                                    proc = subprocess.run(
                                        args,
                                        check=False,
                                        capture_output=True,
                                        text=True,
                                        cwd=str(DIRECTORY_OF_THIS_FILE),
                                    )
                                    print(f"{args}")
                                    print(
                                        f"  returncode={proc.returncode}, duration={time.monotonic()-begin_s:0.3f}s"
                                    )
                                    print(f"  stdout: {proc.stdout}")
                                    print(f"  stderr: {proc.stderr}")
                                    if proc.returncode != 0:
                                        print("**** ERROR !!!!")

                                dev_num = device.properties["DEVNUM"]
                                bus_num = device.properties["BUSNUM"]
                                print(f"  FLASH {bus_num=} {dev_num=}")
                                args = [
                                    "bin/picotool",
                                    "load",
                                    "--update",
                                    # "--verify",
                                    "--execute",
                                    "bin/RPI_PICO-20240222-v1.22.2.uf2",
                                    "--bus",
                                    bus_num,
                                    "--address",
                                    dev_num,
                                ]
                                time.sleep(5.0)
                                subprocess_run(args)

                                if False:
                                    time.sleep(2.0)
                                    args = [
                                        "bin/picotool",
                                        "info",
                                        "--bus",
                                        bus_num,
                                        "--address",
                                        dev_num,
                                        # "--force",
                                        # "--force-no-reboot"
                                    ]
                                    subprocess_run(args)

                                time.sleep(10.0)

                                if False:
                                    args = [
                                        "bin/picotool",
                                        "reboot",
                                        "--application",
                                        # "--usb",
                                        "--bus",
                                        bus_num,
                                        "--address",
                                        dev_num,
                                        # "--force",
                                        # "--force-no-reboot"
                                    ]
                                    subprocess_run(args)
                    continue
                    if False:
                        try:
                            id_vendor = device.properties["ID_USB_VENDOR_ID"]
                            id_product = device.properties["ID_USB_MODEL_ID"]
                        except KeyError:
                            continue
                        print(
                            f"{device.action=} {device.subsystem=} {device.device_type}"
                        )
                        print(device)
                    if False:
                        print(f"{device.action=}")
                        for k, v in device.properties.items():
                            print(f"  {k=} {v=}")
                        # if device.action != "add":
                        #     print(f"action {device.device_node} {device.action=}")
                        #     continue
                        # if is_usb_serial(device, serial_num=None, vendor=None):
                        #     print(f"New device: {device.device_node}")
                        #     break
                    try:
                        id_vendor = device.properties["ID_USB_VENDOR_ID"]
                        id_product = device.properties["ID_USB_MODEL_ID"]
                    except KeyError:
                        continue
                    if not (id_vendor, id_product) in DEVICES_STR:
                        continue
                    print(f"{device.action=} {device.device_node}")


if __name__ == "__main__":
    main()
