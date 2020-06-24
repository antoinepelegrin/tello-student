from darkflow.net.build import TFNet
import cv2
import numpy as np
import math

# Model parameters
options = {"model" : "cfg/yolo-lite.cfg", "load": "weights/yolo-lite.weights", "threshold" : 0.26}
# Model init
yolo = TFNet(options)

# Stream object
cap = cv2.VideoCapture(0)

# Stream/detection loop 
while(True):
	
	# Frame in variable	
	ret, frame = cap.read()

	# Apply model to frame
	results = yolo.return_predict(frame)
	
	# Draw bounding boxes on frame 
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
	
		cv2.rectangle(frame, (xtopleft, ytopleft), (xbottomright, ybottomright), (255, 0, 0), 2)
		cv2.putText(frame, "Label: " + label, (xtopleft, ytopleft - math.floor(0.05*height)), cv2.FONT_HERSHEY_SIMPLEX, 0.005*length, (255, 0, 0))
		cv2.putText(frame, "Confidence:" + str(confidence), (xtopleft, ytopleft + math.floor(0.12*height)), cv2.FONT_HERSHEY_SIMPLEX, 0.005*length, (255, 0, 0))

	# Display frame on screen
	cv2.imshow("frame", frame)

	# Break condition
	if cv2.waitKey(1) and 0xFF == ord("q"):
		break

# Release
cap.release()
cv2.destroyAllWindows()
