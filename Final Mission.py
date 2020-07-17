######## INITIALISATION

#### LIBRAIRIES

import cv2
import numpy as np
import math

from easytello import tello
from darkflow.net.build import TFNet
import yolotools

#### MODELE

# Parametres du modele
options = {"model" : "yolo/cfg/yolo-lite.cfg", "load": "yolo/weights/yolo-lite.weights", "threshold" : 0.26}
# Initialisaton du modele
yolo = TFNet(options)

#### TELLO 

# Objet Tello() 
my_drone = tello.Tello()

######## FONCTIONS 

def beginMission():
    return 0

def patrol():
    return 0

def detection():
    return 0

def action():
    return 0

def endMission():
    return 0

######## MISSION 

my_drone.streamon() 

beginMission()

while my_drone.stream_state:
    return 0

endMission()

my_drone.streamoff()

