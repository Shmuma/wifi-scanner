#!/bin/env python3

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

def usleep(ms):
    sleep(ms / 1000000.0)

while True:
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)
#    usleep(100.0)
    GPIO.output(11, GPIO.LOW)
#    usleep(200.0)
