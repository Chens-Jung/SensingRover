import paho.mqtt.client as mqtt
import threading
import json
import time
import random
from sensing_rover.SensingRover import SensingRover
from module.Camera import Camera


class MqttPublisher:
    def __init__(self, brokerIp=None, brokerPort=1883, topic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__topic = topic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__sensingrover = SensingRover()
        self.__stop = False

    def __on_connect(self, client, userdata, flags, rc):
        print("** connection **")

    def __on_disconnect(self, client, userdata, rc):
        print("** disconnection **")

    def start(self):
        thread = threading.Thread(target=self.__publish)
        thread.start()

    def __publish(self):
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__stop = False
        self.__client.loop_start()
        while not self.__stop:
            self.__client.publish(self.__topic, self.__sensingrover.sensorRead())
            time.sleep(1)
        self.__client.loop_stop()

    def stop(self):
        self.__client.disconnect()
        self.__stop = True



if __name__ == '__main__':
    mqttPublisher = MqttPublisher("192.168.3.131", topic="/sensor/distance")
    mqttPublisher.start()

    # time.sleep(5)
    #
    # mqttPublisher.stop()