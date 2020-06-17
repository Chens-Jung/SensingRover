import paho.mqtt as mqtt
from sensing_rover.SensingRover import SensingRover
from mqtt.SensorPublisher import MqttPublisher
from mqtt.SensorSubscriber import MqttSubscriber
from mqtt.CameraPublisher import ImageMqttPublisher
sensingRover = SensingRover()
sensingRover.angle_handle(90)

mqttPublisher = MqttPublisher("192.168.3.183", topic="/sensor", sensingRover=sensingRover)
mqttPublisher.start()

imageMqttPublisher = ImageMqttPublisher("192.168.3.183", 1883, "/camerapub")
imageMqttPublisher.start()
mqttSubscriber = MqttSubscriber("192.168.3.183", topic="command/#", sensingRover=sensingRover)
mqttSubscriber.start()
