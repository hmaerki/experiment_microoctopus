# Photocouplers

* Search for `PhotoMOS Supsic`

| USD | JLC |  Datasheet | Specs | Comment |
| - | - | - | - | - |
| 0.51 | C261926 | [TLP172GM]() |  |
| 1.06 | C2152276 | [TLP172AM]() |  |  |
| 0.55 | C7435105 | [GAQY221S](https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2308151358_SUPSiC-GAQY221S_C7435105.pdf) | Roff=2OOhm,Cout=12pF | A-Wahl |
| 0.72 | C81521 | [CPC1017NTR](https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1807271520_Littelfuse-IXYS-CPC1017NTR_C81521.pdf) | Ron-max=16Ohm,Cout=5pF |  |


## GAQY221S

Possible Kicad footprints
* TLP3123
* CPC1117N
* CPC1017N
* CPC1002N

Calculation of the input resistor
  Vdiff = 3.3V - Vf = 3.3V- 1.2V = 2.1V
  I_Fon = 0.5mA
  R = 2.1V / 0.5mA = 4.2kOhm

