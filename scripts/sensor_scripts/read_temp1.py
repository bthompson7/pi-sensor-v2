'''

Basement Sensor

'''
import Adafruit_DHT, time,requests,json, os, socket, ssl
import paho.mqtt.client as paho

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

time_delay = 600 #default is 600 seconds / 10 minutes

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# AWS IoT Core "Thing" settings
awshost = ""
awsport = 8883
caPath = "AmazonRootCA1.pem"
certPath = "certificate.pem.crt"
keyPath = "private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()

while True:
	humid, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

	if humid is not None and temp is not None:
		try:
			tempToF = (temp * 1.8) + 32.0
			tempRounded = round(tempToF,4)
			humidRounded = round(humid,4)
			if connflag == True:
				message = json.dumps(dict(Temperature=tempRounded, Humidity=humidRounded))
				mqttc.publish("basementData", payload, qos=1)
				print("msg sent: " + payload)
			else:
				print("Connection issue with AWS IoT Core, is the policy setup correctly?")
		except:
			print("request failed sleeping. The server must be down")
			time.sleep(time_delay)
	else:
		print("Error!")

	time.sleep(time_delay)
