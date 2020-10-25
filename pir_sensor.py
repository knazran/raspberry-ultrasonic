from gpiozero import LED
from gpiozero import MotionSensor
import paho.mqtt.client as mqtt
import time

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

# Setup sensor
led = LED(17)
pir = MotionSensor(4)
led.on()

while True:
	#pir.wait_for_motion()
	while not pir.motion_detected:
		client.publish("kitchen/motion",0)
		time.sleep(1)
	# Motion detected
	print("Motion Detected")
	led.on()
	client.publish("kitchen/motion",1)
	
	# Motion passes by
	pir.wait_for_no_motion()
	led.off()
	print("Motion Stopped")
