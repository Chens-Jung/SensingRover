import paho.mqtt.client as mqtt
import threading
import json
from sensing_rover.SensingRover import SensingRover

class MqttSubscriber:
    def __init__(self, brokerip=None, brokerport=1883, topic=None, sensingRover=None):
        self.__brokerip = brokerip
        self.__brokerport = brokerport
        self.__topic = topic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__sensing_rover = sensingRover

    def __on_connect(self, client, userdata, flags, rc):
        print("** connection **")
        self.__client.subscribe(self.__topic)


    def __on_disconnect(self, client, userdata, rc):
        print("** disconnection **")

    def __on_message(self, client, userdata, message):
        if "lcd" in message.topic:
            print(message.topic)
            strMessage = str(message.payload, encoding="UTF-8")
            self.__sensing_rover.lcd_test(json.loads(strMessage))
        elif "laser" in message.topic:
            if "on" in message.topic:
                self.__sensing_rover.laserOn()
            else:
                self.__sensing_rover.laserOff()
        elif "backTire" in message.topic:
            strMessage = str(message.payload, encoding="UTF-8")
            messageObject = json.loads(strMessage)
            if messageObject["direction"] == "forward":
                self.__sensing_rover.forward()
                self.__sensing_rover.setSpeed(1000)
            if messageObject["direction"] == "backward":
                self.__sensing_rover.backward()
                self.__sensing_rover.setSpeed(1000)
            if messageObject["direction"] == "stop":
                self.__sensing_rover.stop()
            if messageObject["direction"] == "left":
                self.__sensing_rover.handle_left()
            if messageObject["direction"] == "right":
                self.__sensing_rover.handle_right()
            if messageObject["direction"] == "front":
                self.__sensing_rover.handle_refront()

            self.__sensing_rover.setSpeed(800+int(messageObject["pwm"])*400)

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
