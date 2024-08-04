# Crystal

Links

* https://github.com/hmaerki/fork_micropython/tree/hmaerki/XTAL

* https://github.com/micropython/micropython/pull/14402
  * https://wiki.seeedstudio.com/XIAO-RP2040/
  * CRYSTAL_4P_2520
  * Crystal datasheet: http://sjk-crystal.com/1-8-2520-smd-crystal/169859/ http://sjk-crystal.com/upload/2640/download/1/pdf/14_8_smd_crystal_3.pdf

* Crystal auf Filament Dryer, Heizung Dezentral, Octoprobe
  * C9002
  * 12MHz SMD crystal oscillator 20pF
  * https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2403291504_YXC-Crystal-Oscillators-X322512MSB4SI_C9002.pdf

* Raspberry Pico
  * https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf
  * ABM8-272-T3, https://abracon.com/parametric/crystals/ABM8-12.000MHZ-B2-T3
  * Reference:
    * ESR=50 Ohm MAX
    * C0=3pF shunt capacitance
    * CL=10pF load capacitance
    * DL=10uW TYP Drive Level

* https://forums.raspberrypi.com/viewtopic.php?t=314935
  * They have parts which are a lot closer to those specifications (although you'd need to bear the $3 Extended Part fee), such as:
    * C112573
    * C114436

* https://github.com/Breadstick-Innovations/22008-RP2040-Dev-Board
    * He is using C9002

* https://hackaday.com/2023/10/11/how-not-to-build-an-rp2040-board/



| jlc | USD/Stock | Manufacturer | Spec | Comments |
| - | - | - | - | - |
| C9002 | 0.06/200k | YXC | ESR=80Ohm,CL=20pF,C0=3pF,DL100uW |
| C112573 | 0.19/1k | YXC | ESR=80Ohm,CL=20pF,C0=5pF,DL100uW |
| C114436 | 0.14/0k | YXC | ESR=80Ohm,CL=20pF,C0=5pF,DL100uW |


https://jlcpcb.com/partdetail/6016764-OT2EL89CJI_111YLC12M/C5280582


## Open Soucre, Kicad, EliteMicro2040

* https://github.com/Envious-Data/EnvOpenPico/blob/main/EliteMicro2040/production/bom.csv

Crystal: C6071564, USD0.05/3k, [Datasheet](
https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2306211546_SST-3225-12M-18PF-20PPM_C6071564.pdf)
  * ESR=50 Ohnm
  * CL=18pF
  * C0=7pF MAX
  * Dl=100uW

Schematics
 * 1k, 22pF
 * EnvPicoLiPo/EnvPicoLiPo.kicad_pro: 1, 15pF


## Crystal Oscillators

### Package Evaluation

* SMD3225-4P 3.2x2.5
* SMD2520-4P 2.5x2

Search: https://jlcpcb.com/parts/2nd/Crystals_Oscillators_Resonators/Crystal_Oscillators_82508

| jlc | USD/Stock | Package | Comments |
| - | - | - | - |
| C2901596  | 0.37/1k  | SMD2520-4P | 1th |
| C437139   | 0.29/188 | SMD2520-4P | 2nd |
| C2831468  | 0.37/1k  | SMD2520-4P | 2nd |
| C387449   | 0.49/3k  | SMD2520-4P | 2nd |
| C409301   | 0.55/2k  | SMD2520-4P | 2nd |
| - |
| C2901561  | 0.4/3k   | SMD3225-4P | |
| C2681268  | 0.4/634  | SMD3225-4P | |
| C387348   | 0.36/760 | SMD3225-4P | |


