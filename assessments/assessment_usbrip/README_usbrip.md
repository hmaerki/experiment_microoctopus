
* https://pypi.org/project/usbrip/
* https://github.com/snovvcrash/usbrip
* https://ostechnix.com/show-usb-devices-event-history-using-usbrip-in-linux/

* https://www.youtube.com/watch?v=Pag0FJfsyu0


journalctl

https://askubuntu.com/questions/1403946/how-to-find-out-which-unit-is-logging-to-journalctl

`journalctl --output verbose --follow | grep _SYSTEMD_UNIT`


`journalctl --unit=systemd-udevd.service --follow --output=json-pretty`


```json
{
	"__REALTIME_TIMESTAMP" : "1710514767455986",
	"_GID" : "0",
	"_BOOT_ID" : "6693ee947eba47b9b10d596f42aa8af5",
	"_SYSTEMD_UNIT" : "systemd-udevd.service",
	"_UID" : "0",
	"_MACHINE_ID" : "7eb3b265d30d4b448a1afd26defdf766",
	"_SYSTEMD_SLICE" : "system.slice",
	"PRIORITY" : "6",
	"_SELINUX_CONTEXT" : "unconfined\n",
	"_SYSTEMD_INVOCATION_ID" : "cc2d44eebe73428c946ebf812b36ae88",
	"__CURSOR" : "s=e25cea03d1fe46cfa3d4120146ab6884;i=30ea6a;b=6693ee947eba47b9b10d596f42aa8af5;m=95f2b185;t=613b44118e6f2;x=cba1a7d15eb6bf7a",
	"MESSAGE" : "bus: 3, device: 16 was not an MTP device",
	"_CAP_EFFECTIVE" : "1f7fdffffff",
	"_HOSTNAME" : "maerki-ideapad-320",
	"SYSLOG_FACILITY" : "1",
	"SYSLOG_IDENTIFIER" : "mtp-probe",
	"_SOURCE_REALTIME_TIMESTAMP" : "1710514767455946",
	"SYSLOG_RAW" : "<14>Mar 15 15:59:27 mtp-probe: bus: 3, device: 16 was not an MTP device\n",
	"_TRANSPORT" : "syslog",
	"_EXE" : "/usr/lib/udev/mtp-probe",
	"_PID" : "38423",
	"_RUNTIME_SCOPE" : "system",
	"_CMDLINE" : "/lib/udev/mtp-probe /sys/devices/pci0000:00/0000:00:14.0/usb3/3-6/3-6.2 3 16",
	"_COMM" : "mtp-probe",
	"SYSLOG_TIMESTAMP" : "Mar 15 15:59:27 ",
	"__MONOTONIC_TIMESTAMP" : "2515710341",
	"_SYSTEMD_CGROUP" : "/system.slice/systemd-udevd.service/udev"
}
```


`journalctl --identifier=kernel --facility=0 --output=json-pretty --follow`

```
--identifier=kernel
"SYSLOG_IDENTIFIER" : "kernel",

--facility=0
"SYSLOG_FACILITY" : "0",
```


`journalctl --follow --output=json-pretty`

```
{
	"_KERNEL_DEVICE" : "c189:275",
	"_UDEV_SYSNAME" : "3-6.2",
	"MESSAGE" : "usb 3-6.2: USB disconnect, device number 20",
	"SYSLOG_FACILITY" : "0",
	"_UDEV_DEVNODE" : "/dev/bus/usb/003/020",
	"_KERNEL_SUBSYSTEM" : "usb",
	"SYSLOG_IDENTIFIER" : "kernel",
}

{
	"_KERNEL_DEVICE" : "+usb:3-6.2",
	"MESSAGE" : "usb 3-6.2: new full-speed USB device number 21 using xhci_hcd",
	"SYSLOG_FACILITY" : "0",
	"_KERNEL_SUBSYSTEM" : "usb",
	"SYSLOG_IDENTIFIER" : "kernel",
}

{
	"_KERNEL_DEVICE" : "c189:276",
	"_UDEV_SYSNAME" : "3-6.2",
	"MESSAGE" : "usb 3-6.2: New USB device found, idVendor=046d, idProduct=c534, bcdDevice=29.01",
	"SYSLOG_FACILITY" : "0"
	"_KERNEL_SUBSYSTEM" : "usb",
	"SYSLOG_IDENTIFIER" : "kernel",
}

{
	"_KERNEL_DEVICE" : "c189:276",
	"_UDEV_DEVNODE" : "/dev/bus/usb/003/021",
	"_UDEV_SYSNAME" : "3-6.2",
	"MESSAGE" : "usb 3-6.2: Manufacturer: Logitech",
	"SYSLOG_FACILITY" : "0",
	"_KERNEL_SUBSYSTEM" : "usb",
	"SYSLOG_IDENTIFIER" : "kernel",
}

{
	"_KERNEL_DEVICE" : "c189:275",
	"_UDEV_SYSNAME" : "3-6.2",
	"_UDEV_DEVNODE" : "/dev/bus/usb/003/020",
	"MESSAGE" : "usb 3-6.2: USB disconnect, device number 20",
	"SYSLOG_FACILITY" : "0",
	"_KERNEL_SUBSYSTEM" : "usb",
	"SYSLOG_IDENTIFIER" : "kernel",
}
```

`journalctl --output=json-pretty --follow`

```
{
        "_KERNEL_SUBSYSTEM" : "usb",
        "SYSLOG_FACILITY" : "0",
        "PRIORITY" : "6",
        "_KERNEL_DEVICE" : "c189:143",
        "_TRANSPORT" : "kernel",
        "MESSAGE" : "usb 2-3: USB disconnect, device number 16",
        "_RUNTIME_SCOPE" : "system",
        "_UDEV_SYSNAME" : "2-3",
        "_UDEV_DEVNODE" : "/dev/bus/usb/002/016"
}
```



```bash
export PICO_BUS=3
export PICO_ADDRESS=39

$ lsusb -d  2e8a:0003
Bus 003 Device 031: ID 2e8a:0003 Raspberry Pi RP2 Boot
$ lsusb -s 3:31
Bus 003 Device 031: ID 2e8a:0003 Raspberry Pi RP2 Boot

$ /home/maerki/tmp/fork_picotool/build/picotool info
No accessible RP2040 devices in BOOTSEL mode were found.
but:
Device at bus 3, address 31 appears to be a RP2040 device in BOOTSEL mode, but picotool was unable to connect. Maybe try 'sudo' or check your permissions.

/home/maerki/tmp/fork_picotool/build/picotool info --bus 3 --address 31
No accessible RP2040 device in BOOTSEL mode was found at bus 3, address 31.
but:
Device at bus 3, address 31 appears to be a RP2040 device in BOOTSEL mode, but picotool was unable to connect. Maybe try 'sudo' or check your permissions.

# Flash the program
sudo /home/maerki/tmp/fork_picotool/build/picotool load --update --verify --execute RPI_PICO-20240222-v1.22.2.uf2 --bus $PICO_BUS --address $PICO_ADDRESS

# 4.8s with new firmware
# 1.4s with unchanged firmware

# Boot into application mode
sudo /home/maerki/tmp/fork_picotool/build/picotool reboot -a --bus $PICO_BUS --address $PICO_ADDRESS
```

