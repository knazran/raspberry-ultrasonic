#!/user/bin/python
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.110", 1883, 60)


try:
    GPIO.setmode(GPIO.BCM)

    PIN_TRIGGER = 21
    PIN_ECHO = 20

    while True:
       # print("Distance Measurement")
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        
        GPIO.output(PIN_TRIGGER, False)

        #print("Waiting for sensor to settle")

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
        client.publish("kitchen/distance",distance)
        print("Distance: {}cm".format(distance))
        time.sleep(1)
except Exception as e:
    print(e)

