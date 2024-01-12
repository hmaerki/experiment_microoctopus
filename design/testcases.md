# Testcases

## Update firmware

* Boot button
* Power on
* Program
* Power cycle
* repl: verify version

## Test WDT

Precondition: Up and running

Testprogramm: gpio -> interrupt -> wdt.feed()

```python

```

* Stimuli: pulse gpio
* Stimuli: stop pulse gpio
* Expected response: reboot
* Expected response: boot cause: wdt

## Test lcd

Precondition: Up and running

Testprogramm: display rolling text

* Stimuli: display text
* Expected response: Image

==> How to capture images?

## Test Bus

FET leaks, how to detect.
