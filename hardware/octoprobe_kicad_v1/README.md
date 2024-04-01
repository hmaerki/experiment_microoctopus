# Octoprobe v1

## Terms
`opto-pico`: The raspberry pi pico which controls the tentacle


## Goals to be achieved with this board

### No button update of opto-pico

Setup
* 1 tentacle with opto-pico

Result
* Tune TP6 cap for BOOTSEL-mode

### Automate opto-pico

Setup
* 1 RHS USB Hub (2 opto-pico)
* Two tentacles

Result
* Automatically detect tentacles on USB hub (pyusb, pyudev)
* Automatically update micropython on opto-pico
* Assignments of opto-pico serial to USB hub port identifier

### Update DUT

Setup
* 1 RHS USB Hub (2 opto-pico, 1 DUT-pico, 1 DUT-pyboard)
* Tentacle A: Raspberry Pi Pico
  * update pico using `picotool`
* Tentacle B: pyboard
  * update pybard using `dfu-util`

Result
* Automatically update FW on tentacle A
  * Optorelays on boot button
  * install micropython and testcode
* Automatically update FW on tentacle B
  * Optorelays on boot button
  * install micropython and testcode
