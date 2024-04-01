
# Picotool

* https://github.com/raspberrypi/picotool
* https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

```
picotool is a tool for inspecting RP2040 binaries, and interacting with RP2040 devices when they are in BOOTSEL mode. (As of version 1.1 of picotool it is also possible to interact with RP2040 devices that are not in BOOTSEL mode, but are using USB stdio support from the Raspberry Pi Pico SDK by using the -f argument of picotool).
```

## Build: in github codespace:

```bash
sudo apt update
sudo -y apt install build-essential pkg-config libusb-1.0-0-dev cmake
git clone https://github.com/raspberrypi/pico-sdk.git
export PICO_SDK_PATH=`pwd`/pico-sdk
mkdir build
cd build
cmake ..
make

ls -lh picotool 
-rwxrwxrwx 1 codespace codespace 390K Jan 28 19:03 picotool
```

## help

```
./picotool --help

ERROR: Expected command name before any options

SYNOPSIS:
    picotool info [-b] [-p] [-d] [-l] [-a] [--bus <bus>] [--address <addr>] [-f]
                [-F]
    picotool info [-b] [-p] [-d] [-l] [-a] <filename> [-t <type>]
    picotool load [-n] [-N] [-u] [-v] [-x] <filename> [-t <type>] [-o <offset>]
                [--bus <bus>] [--address <addr>] [-f] [-F]
    picotool save [-p] [--bus <bus>] [--address <addr>] [-f] [-F] <filename> [-t
                <type>]
    picotool save -a [--bus <bus>] [--address <addr>] [-f] [-F] <filename> [-t
                <type>]
    picotool save -r <from> <to> [--bus <bus>] [--address <addr>] [-f] [-F]
                <filename> [-t <type>]
    picotool verify [--bus <bus>] [--address <addr>] [-f] [-F] <filename> [-t
                <type>] [-r <from> <to>] [-o <offset>]
    picotool reboot [-a] [-u] [--bus <bus>] [--address <addr>] [-f] [-F]
    picotool version [-s]
    picotool help [<cmd>]

COMMANDS:
    info      Display information from the target device(s) or file.
              Without any arguments, this will display basic information for all
              connected RP2040 devices in BOOTSEL mode
    load      Load the program / memory range stored in a file onto the device.
    save      Save the program / memory stored in flash on the device to a file.
    verify    Check that the device contents match those in the file.
    reboot    Reboot the device
    version   Display picotool version
    help      Show general help or help for a specific command

Use "picotool help <cmd>" for more info
```

## rp2040 in BOOTSEL mode

```
sudo ./picotool info
[sudo] password for maerki: 
Program Information
 name:            MicroPython
 version:         v1.23.0-preview.72.g4a2e510a8
 features:        thread support
                  USB REPL
 frozen modules:  neopixel, dht, ds18x20, onewire, uasyncio, asyncio/stream,
                  asyncio/lock, asyncio/funcs, asyncio/event, asyncio/core,
                  asyncio, _boot_fat, _boot, rp2
```

```
sudo ./picotool info --all
Program Information
 name:            MicroPython
 version:         v1.23.0-preview.72.g4a2e510a8
 features:        thread support
                  USB REPL
 frozen modules:  neopixel, dht, ds18x20, onewire, uasyncio, asyncio/stream,
                  asyncio/lock, asyncio/funcs, asyncio/event, asyncio/core,
                  asyncio, _boot_fat, _boot, rp2
 binary start:    0x10000000
 binary end:      0x1004f560
 embedded drive:  0x100a0000-0x10200000 (1408K): MicroPython

Fixed Pin Information
 none

Build Information
 sdk version:       1.5.1
 pico_board:        pico
 boot2_name:        boot2_w25q080
 build date:        Jan 26 2024
 build attributes:  MinSizeRel

Device Information
 flash size:   2048K
 ROM version:  2
```

```
sudo ./picotool reboot
The device was rebooted into application mode.
```

```
sudo ./picotool reboot --address 30
The device was rebooted into application mode.
```

```
sudo ./picotool load ~/Downloads/RPI_PICO-20240126-v1.23.0-preview.72.g4a2e510a8.uf2 
Loading into Flash: [==============================]  100%
```

## rp2040 in run mode

```
sudo ./picotool info -f
No accessible RP2040 devices in BOOTSEL mode were found.

but:

Device at bus 3, address 33 appears to be a RP2040 MicroPython device not in BOOTSEL mode.
Device at bus 3, address 32 appears to be a RP2040 MicroPython device not in BOOTSEL mode.
```

```
sudo ./picotool reboot -u --address 33
No accessible RP2040 devices in BOOTSEL mode were found with address 33.
but:
Device at bus 3, address 33 appears to be a RP2040 MicroPython device not in BOOTSEL mode.
```

# 2024-03-31

```bash
sudo ./picotool load -x /home/maerki/Downloads/RPI_PICO-20240126-v1.23.0-preview.72.g4a2e510a8.uf2
```

==> When pressing BOOTSEL button reboots into BOOTSEL

```bash
sudo ./picotool load -f /home/maerki/Downloads/RPI_PICO-20240126-v1.23.0-preview.72.g4a2e510a8.uf2
sudo ./picotool load -F /home/maerki/Downloads/RPI_PICO-20240126-v1.23.0-preview.72.g4a2e510a8.uf2
```

==> When pressing BOOTSEL button does not even umount

```bash
sudo ./picotool reboot --application
REBOOT 00000000 20042000 500
       pc       sp       delay_ms
The device was rebooted into application mode.
```
==> Boots into application mode
==> When pressing BOOTSEL button boots into BOOTSEL mode
