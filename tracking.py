#! /usr/bin/env python

# remember to add this file or this folder to a directory that's available to bin!


############## Packages to be used ############
from collections import deque # deque is a module that creates list-like structures with versatile append functions
import numpy as np
import argparse # is a module to help manage the arguments for the command-line
import imutils
import cv2
###############################################



############## Arguments for the script ############
ap = argparse.ArgumentParser(description='Track an orange post-it quick and easy!')
ap.add_argument("-v", "--video",
	help="path to the (optional) video file") # 1st argument: this wil be the path to the video file. If left empty it will use the webcam.
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size") # 2nd argument:  will control the maximum size of the deque points (i.e. the frames that will be tracked; the history of the tracking). Default to 32
#ap.add_argument("-p", "--poem", action="store_true",
#	help="nice poem") # doesn't work right now
args = vars(ap.parse_args()) 
#if args.poem: #doesn't work as it is because poem is not part of the dictionary. If I delete vars then the poem works but not the rest.
#    print("\n\nWir sind durch Not und Freude\ngegangen Hand in Hand;\nvom Wandern ruhen wir beide\nnun ueberm stillen Land.\n\nRings sich die Taeler neigen,\nes dunkelt schon die Luft.\nZwei Lerchen nur noch steigen\nnachtraeumend in den Duft.\n\nTritt her und lass sie schwirren,\nbald ist es Schlafenszeit.\nDass wir uns nicht verirren\nin dieser Einsamkeit.\n\nO weiter, stiller Friede!\nSo tief im Abendrot.\nWie sind wir wandermuede--\nIst dies etwa der Tod?\n\nJoseph von Eichendorff\n\n")
###############################################

# v1_min, v1_max, v2_min, v2_max, v3_min, v3_max = 0, 21, 90, 171, 162, 255 works fine but not perfect
# (0, 15, 124, 255, 113, 255) works much better



orangeLower = (0, 124, 113) # will define the lower boundary in HSV color space of the orange post-it.
orangeUpper = (15, 255, 255)
pts = deque(maxlen=args["buffer"]) # pts will be a deque structure whose maximum length will be defined by the second argument of the script (i.e. the buffer)
 


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])


# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 

	frame = imutils.resize(frame, width=600) # to make the video smaller and easier to analyse
	blurred = cv2.GaussianBlur(frame, (11, 11), 0) # to blur image and wipe out any high frequency noise
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # change video to HSV color space (used to choose the lower- and upperOrange)
 
	
	mask = cv2.inRange(hsv, orangeLower, orangeUpper) # it will create a mask for every object in that falls into the HSV range defined
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2) #dilate and erode to get rid of small defects in the mask



	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2] # cnts is the ensemble of countours that are in the mask (the objects with defined contours that are orange). RETR_EXTERNAL will outline only the external contour. CHAIN_APPROX_SIMPLE will draw the contour with the least number of points.
	center = None
 
	
	if len(cnts) > 0: # len(list) is the number of items in list. It will proceed only if at least one (orange object) was found.

		c = max(cnts, key=cv2.contourArea) # max will look in cnts and find the largest object as defined by their contour area
		(x, y, w, h) = cv2.boundingRect(c) # of the largest object, it computes the 
		M = cv2.moments(c) 
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the width meets a minimum size
		if w > 10:
			# draw the rectangle and centroid on the frame,
			# then update the list of tracked points
			cv2.rectangle(frame, (int(x), int(y)), (x+w,y+h), (0, 255, 0), 3) # 1st arg: image, 2nd: upper-left corner, 3rd: lower-right, 4th: color, 5th: thickness
			cv2.rectangle(frame, center, center, (0, 255, 0), -1)
 
	# update the points queue
	pts.appendleft(center)




		# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)

	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
