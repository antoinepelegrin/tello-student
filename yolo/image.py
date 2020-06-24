from darkflow.net.build import TFNet
import cv2 as cv

options = {"model" : "cfg/yolo-lite.cfg", "load": "weights/yolo-lite.weights", "threshold" : 0.26}

tfnet = TFNet(options)

imgcv = cv.imread("dog.jpg")
result = tfnet.return_predict(imgcv)
print(result)
