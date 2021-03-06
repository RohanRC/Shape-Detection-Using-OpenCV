# import the necessary packages
import cv2

import argparse
import imutils
import cv2
import numpy as np
import matplotlib.pyplot as plt
  
class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
 
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
		# if the shape is a pentagon, it will have 5 vertices
		#elif len(approx) == 5:
		#	shape = "pentagon"
 
		# otherwise, we assume the shape is a circle
		elif len(approx) >4:
			shape = "circle"
 
		# return the name of the shape
		return shape

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,help="a,jpg")
#args = vars(ap.parse_args())
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
cap= cv2.VideoCapture(0)
codec=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('outpu.avi',codec,80.0,(640,480))

while True:
    ret,image=cap.read()
    resized = imutils.resize(image, width=650)
    ratio = image.shape[1] / float(resized.shape[1])
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    s=15
    w=np.array([30-s,100,100])
    s=np.array([30+s,255,255])

    thresh=cv2.inRange(hsv,w,s) 

    
    kernel=np.ones((11,11),np.uint8)
    kernel2=np.ones((10,10),np.uint8)
    #thresh = cv2.GaussianBlur(thresh, (5, 5), 0)
    thresh=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
    thresh = cv2.GaussianBlur(thresh, (11, 11), 4)
    #thresh=cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel2)
    cv2.imshow('a',thresh)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        if M["m00"]>0:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            shape = sd.detect(c)
     
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
            #out.write(image)
        # show the output image
            cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

