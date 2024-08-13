# Goal

* Start sigrok-cli for every test
* Store dumps
* Automatically verify dumpys
* Allow PulseView to verify dump

## Summary

I could not find a python implementation which reads/writes sr2-files.
`pysigrok/sigrokdecode` started a implementation but it is far from useful.

It probably would not be difficult to implement it.

* https://github.com/sigrokproject/sigrok-dumps/blob/master/onewire/ds2432/ds2432.sr
  * 'metadata' contains `capturefile=logic-1`
  * However, the files `logic-1-1` `logic-1-2` are stored
  * What is correct?

## Examaple dumps

* https://sigrok.org/wiki/Example_dumps
* https://github.com/sigrokproject/sigrok-dumps


## A specific dump

* https://github.com/sigrokproject/sigrok-dumps/tree/master/i2c/eeprom_24xx/atmel_at24c16c

assessments/assessment_sigrok/specific_dump/dreamsourcelab_dslogic_powerup.sr

```bash
mkdir dreamsourcelab_dslogic_powerup
cd dreamsourcelab_dslogic_powerup
unzip ../dreamsourcelab_dslogic_powerup.sr

~maerki/experiment_sigrok/appimage_sigrok/pulseview-NIGHTLY-x86_64-release.appimage dreamsourcelab_dslogic_powerup.sr

~maerki/experiment_sigrok/appimage_sigrok/pulseview-NIGHTLY-x86_64-release.appimage --dont-scan --clean --settings pulseview_session.pvs --input-file dreamsourcelab_dslogic_powerup.sr

~maerki/experiment_sigrok/appimage_sigrok/pulseview-NIGHTLY-x86_64-release.appimage --dont-scan --clean --settings pulseview_session.pvs --input-file lcsoft-mini-board-fx2-init.sr
```

## Read `.sr` files from python

```bash
sigrok-cli -i dreamsourcelab_dslogic_powerup.sr
libsigrok 0.5.2
Acquisition with 8/8 channels at 4 MHz
SCL:00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
SDA:00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
WP:00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
D3:11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111
D4:11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111
D5:11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111
D6:11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111
D7:11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111
SCL:00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000

sigrok-cli --protocol-decoder-samplenum -i dreamsourcelab_dslogic_powerup.sr -P i2c,eeprom24xx

```

* https://github.com/sdbbs/sigrok_pulseview_combine_merge/blob/master/code/merge_sr_sessions.py
* https://github.com/pysigrok/pysigrok/blob/main/sigrokdecode/srzip.py
* https://pypi.org/project/wavebin/
  * https://github.com/sam210723/wavebin

## Try `https://github.com/pysigrok/pysigrok/blob/main/sigrokdecode/srzip.py`

```bash
pip install git+https://github.com/pysigrok/pysigrok
```