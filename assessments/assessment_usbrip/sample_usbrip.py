import asyncio.subprocess
import io
import json
from typing import AsyncIterable, Optional
import pprint


class DeviceDetector:
    def __init__(self):
        self.    kernel_device: Optional[str] = None

    def push(self, json_dict: dict)-> None:
        message = json_dict["MESSAGE"]
        if "idVendor=2e8a, idProduct=0003" in message:
            self.kernel_device = json_dict["_KERNEL_DEVICE"]
            udev_devnode = json_dict["_UDEV_DEVNODE"]
            udev_sysname = json_dict["_UDEV_SYSNAME"]
            print(
                f"*** rp2040 in boot mode: {self.kernel_device=} {udev_devnode=} {udev_sysname=}"
            )

        if "idVendor=2e8a, idProduct=0005" in message:
            self.kernel_device = json_dict["_KERNEL_DEVICE"]
            udev_devnode = json_dict["_UDEV_DEVNODE"]
            udev_sysname = json_dict["_UDEV_SYSNAME"]
            print(
                f"*** rp2040 in micropython mode: {self.kernel_device=} {udev_devnode=} {udev_sysname=}"
            )

        if self.kernel_device == json_dict.get("_KERNEL_DEVICE", "-"):
            print("MESSAGE: ", message)

async def main():
    program = "/usr/bin/journalctl"
    args = {
        "--output=json-pretty",
        "--follow",
    }
    process = await asyncio.create_subprocess_exec(
        program,
        *args,
        stdout=asyncio.subprocess.PIPE,
    )

    async def iter_json(stdout) -> AsyncIterable[dict]:
        """
        Returns a json string or
        None at EOF
        """
        json_io: Optional[io.BytesIO] = None
        while True:
            buf = await stdout.readline()
            if not buf:
                return
            if json_io is None:
                if buf != b"{\n":
                    continue
                json_io = io.BytesIO()
            json_io.write(buf)
            if buf == b"}\n":
                yield json.loads(json_io.getvalue())
                json_io = None

    pp = pprint.PrettyPrinter(indent=4)
    dd = DeviceDetector()
    async for json_dict in iter_json(process.stdout):
        message = json_dict["MESSAGE"]

        if False:
            print("MESSAGE: ", message)
            pp.pprint(json_dict)

        dd.push(json_dict=json_dict)

    # read data from the subprocess
    data, _ = await process.communicate()
    # report the data
    print("***", data)


# entry point
asyncio.run(main())
