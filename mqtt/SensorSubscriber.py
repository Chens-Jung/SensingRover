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
            if "forward" in message.topic:
                self.__sensing_rover.forward()
            elif "backward" in message.topic:
                self.__sensing_rover.backward()
            elif "stop" in message.topic:
                self.__sensing_rover.stop()
            elif "respeed" in message.topic:
                self.__sensing_rover.respeed()
            elif "button" in message.topic:
                strMessage = str(message.payload, encoding="UTF-8")
                messageObject = json.loads(strMessage)
                print(messageObject)
                if messageObject["pwm"] != 0:
                    self.__sensing_rover.button_setSpeed(800 + int(messageObject["pwm"]) * 400)
                if messageObject["direction"] == "forward":
                    self.__sensing_rover.button_forward()
                elif messageObject["direction"] == "backward":
                    self.__sensing_rover.button_backward()
                elif messageObject["direction"] == "stop":
                    self.__sensing_rover.button_stop()
        elif "frontTire" in message.topic:
            if "left" in message.topic:
                self.__sensing_rover.handle_left()
            elif "right" in message.topic:
                self.__sensing_rover.handle_right()
            elif "front" in message.topic:
                self.__sensing_rover.handle_refront()


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
