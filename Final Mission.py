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

#### CONSTANTES

xcenter = 480
ycenter = 360 

distance_min = 40 

######## COMMANDES 

commands = []

commands.append("go 40 0 100 30 m1")

commands.append("cw 45")
commands.append("cw 45")

commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")

commands.append("cw 45")
commands.append("cw 45")

commands.append("go 0 0 100 30 m2")

commands.append("cw 45")
commands.append("cw 45")
commands.append("cw 45")

commands.append("go 40 -40 100 30 m2")

commands.append("cw 45")
commands.append("cw 45")

commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")

commands.append("cw 45")
commands.append("cw 45")

commands.append("go 0 0 100 30 m3")

commands.append("cw 45")
commands.append("cw 45")

commands.append("go 40 40 100 30 m3")

commands.append("cw 45")
commands.append("cw 45")

commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")
commands.append("ccw 45")

commands.append("cw 45")
commands.append("cw 45")

commands.append("go 0 0 100 30 m1")

commands.append("cw 45")
commands.append("cw 45")
commands.append("cw 45")

nb_steps = len(commands)

######## FONCTIONS 

# Appelee au debut de la mission
# Fait decoller le drone, l'amene a 150cm du sol, demarre le stream du tello et active la camera ventrale. 

def beginMission():
    my_drone.send_command("mon")
    my_drone.streamon()
    my_drone.takeoff()
    while my_drone.get_tof() < 150:
        my_drone.up(20)

# Fait suivre au drone le parcours de mission pads specifie dans les diapositives. 
        
def patrol(command):
    my_drone.send_command(command)

# Retourne la difference en x et y entre le centre de l'image et le centre de la meilleure boite englobante. 

def distances(predictions, label):
    
    max_confidence = 0
    index = 0
    
    iterations = len(predictions)
    
    for i in range(iterations):
        if predictions[i]["label"] == label and prediction[i]["confidence"] > max_confidence:
            index = i
            max_confidence = prediction["confidence"]
            
        target = predictions[index]
        
        x_centerbox = target["topleft"]["x"] + (target["bottomright"]["x"] - target["topleft"]["x"])/2
        y_centerbox = target["topleft"]["y"] + (target["bottomright"]["y"] - target["topleft"]["y"])/2
        
        x_diff = x_centerbox - xcenter
        y_diff = y_centerbox - ycenter 
        
        return [x_diff, y_diff]
    
# Retourne la distance euclidienne entre le centre de l'image et le centre de la boite englobante.
    
def distance(distances):
    return math.sqrt(distances[0]**2 + distances[1]**2)

# Deplace le drone de haut en bas et le fait tourner de maniere a l'enligner sur la detection.  

def align(differences):
    x_diff = differences[0]
    y_diff = differences[1]
    
    if x_diff < 0:
        drone.ccw(math.floor(abs(x_diff) *0.07))
    else:
        drone.cw(math.floor(abs(x_diff) *0.07))
        
    if abs(y_diff) > 30:
        if y_diff < 0:
            drone.up(20)
        else:
            drone.down(20)

# Fait faire une pirouette au drone et imprime un message a l'ecran 
        
def action():
    my_drone.flip("left")
    print("Cible identifiee!")

# Ramene le drone a la base, mettre fin au stream, fermer la fenetre OpenCV. 
    
def endMission():
    my_drone.streamoff()
    cv2.DestroyAllWindows()

######## MISSION 

label = "person"

# Debut de la mission

beginMission()

# Objet capture 

cap = VideoCapture(my_drone.video_source)

# Boucle principale 
i = 0 

while my_drone.stream_state:
    frame = cap.read()
    
    predictions = yolo.return_predict(frame)
    bounding_boxes(predictions, label)
    
    cv2.imshow("Tello Stream", frame)
    
    # Execute si le bon label est detecte. Sinon, appeler patrol() pour le mouvement par defaut. 
    
    if detected(predictions, label):
        
        distances = distances(predictions, label)
        
        # Si le drone est bien aligne a l'objet, executer action() et sortir de la boucle. Sinon, appeler align() pour l'enligner. 
        
        if distance(distances) < distance_min:
            action()
            break 
        else:
            align(distances)
        
    else: 
        patrol(command[i])
        i = (i+1)%nb_steps 
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break 

# Fin de la mission 
        
endMission()

