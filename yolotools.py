import cv2 
import math
import queue
import time
import threading 

# Class for threading and queuing video capture 

class VideoCapture:
	def __init__(self, name):
		self.cap = cv2.VideoCapture(name)
		self.q = queue.Queue()
		t = threading.Thread(target=self._reader)
		t.daemon = True
		t.start()

	def _reader(self):
		while True:
			ret, frame = self.cap.read()
			if not ret:
				break
			if not self.q.empty():
				try:
					self.q.get_nowait()
				except Queue.Empty:
					pass
			self.q.put(frame)
            
	def release(self):
		self.cap.release()
	
	def read(self):
		return self.q.get() 
    
# Function that returns True if a target label is in the detections 

def detected(detections, target):
    detected = False 
    
    for detection in detections:
        label = detection["label"]
        
        if label == target:
            detected = True
            break
    
    return detected  

# Function for drawing bounding boxes 

def bounding_boxes(results, img):
	for result in results:
		# Parse detector output
		label = result["label"]
		confidence = result["confidence"]

		xtopleft = result["topleft"]["x"]
		ytopleft = result["topleft"]["y"]
		
		xbottomright = result["bottomright"]["x"]
		ybottomright = result["bottomright"]["y"]

		length = xbottomright - xtopleft
		height = ybottomright - ytopleft

		# Draw and write on frame		
		cv2.rectangle(img, (xtopleft, ytopleft), (xbottomright, ybottomright), (255, 0, 0), 2)
		cv2.putText(img, "Label: " + label, (xtopleft, ytopleft - math.floor(0.05*height)), cv2.FONT_HERSHEY_SIMPLEX, 0.005*length, (255, 0, 0))
		cv2.putText(img, "Confidence:" + str(confidence), (xtopleft, ytopleft + math.floor(0.12*height)), cv2.FONT_HERSHEY_SIMPLEX, 0.005*length, (255, 0, 0))

# Function that return matches with highest confidence 
    
def match(detections, targets):	
	centers = []
	model_output = []
	max_confidence = []
	for target in targets:
		centers.append([])
		model_output.append({})
		max_confidence.append(0)

	targeting = False

	for detection in detections:
		label = detection["label"]

		if label in targets:
			targeting = True
	
			index = targets.index(label)
			confidence = detection["confidence"]

			if confidence > max_confidence[index]:
				max_confidence[index] = confidence

				xtopleft = detection["topleft"]["x"]
				ytopleft = detection["topleft"]["y"]
				xbottomright = detection["bottomright"]["x"]
				ybottomright = detection["bottomright"]["y"]

				width = xbottomright - xtopleft
				length = ybottomright - ytopleft

				center = [int(xtopleft + width/2), int(ytopleft + length/4)] 

				centers[index] = center	
				model_output[index] = detection

	return targeting, centers, model_output 

# Retourne la difference en x et y entre le centre de l'image et le centre de la meilleure boite englobante. 

def distances(predictions, label):
    
    max_confidence = 0
    index = 0
    
    iterations = len(predictions)
    
    for i in range(iterations):
        if predictions[i]["label"] == label and predictions[i]["confidence"] > max_confidence:
            index = i
            max_confidence = predictions[i]["confidence"]
            
        target = predictions[index]
        
        x_centerbox = target["topleft"]["x"] + (target["bottomright"]["x"] - target["topleft"]["x"])/2
        y_centerbox = target["topleft"]["y"] + (target["bottomright"]["y"] - target["topleft"]["y"])/2
        
        x_diff = x_centerbox - xcenter
        y_diff = y_centerbox - ycenter 
        
        return [x_diff, y_diff]

# Deplace le drone de haut en bas et le fait tourner de maniere a l'enligner sur la detection.  

def align(differences):
    x_diff = differences[0]
    y_diff = differences[1]
    
    if x_diff < 0:
        my_drone.ccw(math.floor(abs(x_diff) *0.07))
    else:
        my_drone.cw(math.floor(abs(x_diff) *0.07))
        
    if abs(y_diff) > 30:
        if y_diff < 0:
            my_drone.up(20)
        else:
            my_drone.down(20)
