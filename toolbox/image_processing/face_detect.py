import numpy as np
import cv2


def draw_face(frame):
	shape = frame.shape


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/home/thuc/SoftDesSp15/toolbox/image_processing/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
# Capture frame-by-frame
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
		cv2.rectangle(frame,(x+w/6,y+h/4),(x+w/4, y+h*2/4),(0,255,255))
		cv2.rectangle(frame,(x+w*5/6,y+h/4),(x+w*3/4, y+h*2/4),(0,255,255))
	 	cv2.ellipse(frame, (x+w/2, y+h*3/4) , (w/4,h/4), 0,0,180,(0,255,0),2) 
	 	cv2.ellipse(frame, (x+w/2, y+h*2/4) , (w/16,h/16), 0,0,360,(0,255,0),2) 
	 
	 # Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()