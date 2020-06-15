import paho.mqtt as mqtt
from mqtt.sensorPublisher import MqttPublisher
from mqtt.cameraPublisher import ImageMqttPublisher

mqttPublisher = MqttPublisher("192.168.3.183", topic="/sensor")
mqttPublisher.start()
imageMqttPublisher = ImageMqttPublisher("192.168.3.183", 1883, "/camerapub")
imageMqttPublisher.start()