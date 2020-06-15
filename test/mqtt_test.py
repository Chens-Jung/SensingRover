import paho.mqtt as mqtt
from mqtt.SensorPublisher import MqttPublisher
from mqtt.SensorSubscriber import MqttSubscriber
from mqtt.CameraPublisher import ImageMqttPublisher

mqttPublisher = MqttPublisher("192.168.3.183", topic="/sensor")
mqttPublisher.start()

imageMqttPublisher = ImageMqttPublisher("192.168.3.183", 1883, "/camerapub")
imageMqttPublisher.start()
mqttSubscriber = MqttSubscriber("192.168.3.183", topic="/lcd")
mqttSubscriber.start()
