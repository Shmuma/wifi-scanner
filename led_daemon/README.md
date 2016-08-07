# Overview

This daemon works on RPi side and controls intelligent RGB LED attached to GPIO 0.
The protocol for daemon is REST.

# Hardware

I've used WS2812B LED IC which can be powered by 3.3V and controlled from GPIO using one wire.

* LED pin 1 (VCC) is attached to RPi PIN 1 (+3.3V)
* LED pin 2 (Out) is not attached (it can be used to cascading multiple LEDs)
* LED pin 3 (GND) is attached to RPi PIN 6 (GND)
* LED pin 4 (In) is attached to RPi PIN 11 (BCM17 == GPIO0)

# Protocol

By default it listens to port 8000