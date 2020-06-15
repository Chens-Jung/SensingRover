import paho.mqtt.client as mqtt
import threading
import json
from sensing_rover.SensingRover import SensingRover

class MqttSubscriber:
    def __init__(self, brokerip=None, brokerport=1883, topic=None):
        self.__brokerip = brokerip
        self.__brokerport = brokerport
        self.__topic = topic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__sensing_rover = SensingRover()

    def __on_connect(self, client, userdata, flags, rc):
        print("** connection **")
        self.__client.subscribe(self.__topic)


    def __on_disconnect(self, client, userdata, rc):
        print("** disconnection **")

    def __on_message(self, client, userdata, message):
        strMessage = str(message.payload, encoding="UTF-8")
        self.__sensing_rover.lcd_test(json.loads(strMessage))



    def __subscribe(self):
        self.__client.connect(self.__brokerip, self.__brokerport)
        self.__client.loop_forever()


    def start(self):
        thread = threading.Thread(target=self.__subscribe())
        thread.start()

    def stop(self):
        self.__client.unsubscribe(self.__topic)
        self.__client.disconnect()

if __name__ == '__main__':
    mqttSubscriber = MqttSubscriber("192.168.3.131", topic="/sensor/distance")
    mqttSubscriber.start()
