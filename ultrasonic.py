#!/user/bin/python
import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BCM)

    PIN_TRIGGER = 21
    PIN_ECHO = 20

    while True:
        print("Distance Measurement")
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        
        GPIO.output(PIN_TRIGGER, False)

        print("Waiting for sensor to settle")

        time.sleep(0.2)
        GPIO.output(PIN_TRIGGER, True)

        time.sleep(0.0001)
        GPIO.output(PIN_TRIGGER, False)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start=time.time()

        while GPIO.input(PIN_ECHO) == 1:
            pulse_end=time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration*17150
        distance = round(distance, 2)

        print("Distance: {}cm".format(distance))
        time.sleep(2)
except Exception as e:
    print(e)
