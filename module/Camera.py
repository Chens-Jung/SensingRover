import cv2
import base64

class Camera:
    def __init__(self, cameraNo=0, width=320, height=240):
        self.videoCapture = cv2.VideoCapture(cameraNo)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        retval, frame = self.videoCapture.read()
        return retval, frame

    def release(self):
        self.videoCapture.release()