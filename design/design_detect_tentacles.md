# Given: Tentacle with USB Hub

* Goal: Identify all tentacles

* Prerequisits
  * RP2 Infra powered on
  * RP2 Infra in application mode


* Detect RP2 Infra in programming mode: Fix rp_unique_id
  * Action: Programm and reboot

* Detect RP2 Infra not powered on
  * `lsusb -v` returns a Micrchip hub where Plug 1 is not powered
  * Action: Power Plug 1, restart search

