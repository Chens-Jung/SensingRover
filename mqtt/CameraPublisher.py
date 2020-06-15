import cv2
import paho.mqtt.client as mqtt
import threading
import base64
from module.Camera import Camera


class ImageMqttPublisher:
    def __init__(self, brokerIp=None, brokerPort=1883, pubTopic=None):
        self.brokerIp = brokerIp
        self.brokerPort = brokerPort
        self.pubTopic = pubTopic
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.camera = Camera(0)

    def start(self):
        thread = threading.Thread(target=self.__run, daemon=True)
        thread.start()

    def __run(self):
        print("실행쓰")
        self.client.connect(self.brokerIp, self.brokerPort)
        self.client.loop_start()
        while True:
            if self.camera.videoCapture.isOpened():
                retval, frame = self.camera.read()
                if not retval:
                    print("video capture fail")
                    break
                self.sendBase64(frame)
                # print("send")
            else:
                print("videoCapture is not opened")
                break
        self.client.loop_stop()

    def __on_connect(self, client, userdata, flags, rc):
        print("ImageMqttClient mqtt broker connect")

    def __on_disconnect(self, client, userdata, rc):
        print("ImageMqttClient mqtt broker disconnect")

    def disconnect(self):
        self.client.disconnect()

    def sendBase64(self, frame):
        if self.client is None:
            return
        # MQTT Broker가 연결되어 있지 않을 경우
        if not self.client.is_connected():
            return
        # JPEG 포맷으로 인코딩
        retval, bytes = cv2.imencode(".jpg", frame)
        # 인코딩이 실패했을 경우
        if not retval:
            print("image encoding fail")
            return
        # Base64 문자열로 인코딩
        b64_bytes = base64.b64encode(bytes)
        # MQTT Broker로 보내기
        self.client.publish(self.pubTopic, b64_bytes)


if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)
    videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    imageMqttPublisher = ImageMqttPublisher("192.168.3.183", 1883, "/camerapub")
    imageMqttPublisher.connect()

    while True:
        if videoCapture.isOpened():
            retval, frame = videoCapture.read()
            if not retval:
                print("video capture fail")
                break
            imageMqttPublisher.sendBase64(frame)
            # print("send")
        else:
            print("videoCapture is not opened")
            break

    imageMqttPublisher.disconnect()
    videoCapture.release()

