# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		iris_detection.py

import cv
import math
import numpy

centroid = (0,0)
pupilArea = 0
pupil = []

def getRadius(area):
	r = 1.0
	r = math.sqrt(area/3.14)
	return (r)

def getPupil(frame):
	pupilImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.InRangeS(frame, (30,30,30), (80,80,80), pupilImg)
	cv.ShowImage("output", pupilImg)
	contours = cv.FindContours(pupilImg, cv.CreateMemStorage(0), mode = cv.CV_RETR_EXTERNAL)
	del pupilImg
	x,y = -10, -10
	i = 0
	while contours:
		moments = cv.Moments(contours)
		area = cv.GetCentralMoment(moments,0,0)
		if (area > 50):
			pupilArea = area
			x = cv.GetSpatialMoment(moments,1,0)/area
			y = cv.GetSpatialMoment(moments,0,1)/area
			pupil = contours
			point = (int(x),int(y))
			global centroid
			centroid = point
			cv.DrawContours(frame, pupil, (0,0,0), (0,0,0), 2, cv.CV_FILLED)
			#cv.Circle(frame, (int(x),int(y)), 2, (0,255,0), int(r)*2)
			break
		contours = contours.h_next()
		i += 1
	return (frame)

def getIris(frame):
	grayImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	storage = cv.CreateMat(frame.width, 1, cv.CV_32FC3)
	cv.CvtColor(frame,grayImg,cv.CV_BGR2GRAY)
	cv.Canny(grayImg, grayImg, 5, 70, 3)
	cv.Smooth(grayImg,grayImg,cv.CV_GAUSSIAN, 7, 7)
	minRad = int(getRadius(pupilArea))
	cv.HoughCircles(grayImg, storage, cv.CV_HOUGH_GRADIENT, 2, 100.0, 30, 150, 100, 140)
	#cv.ShowImage("output", grayImg)
	circles = numpy.asarray(storage)
	for circle in circles:
		rad = int(circle[0][2])
		cv.Circle(frame, centroid, rad, cv.CV_RGB(255,0,0), 1, 8, 0)
		#cv.DrawContours(frame, circles, (0,0,0), (0,0,0), 2)
		#print "circle!"
	return (frame)


cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
key = 0
while True:
	frame = cv.LoadImageM("images/R/S1001R02.jpg")
	output = getPupil(frame)
	cv.ShowImage("input", frame)
	iris = getIris(output)
	cv.ShowImage("output", iris)
	key = cv.WaitKey(500)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyWindow("input")

