# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		iris_detection.py

import cv
import math


centroid = [-100,-100]
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
			point = [int(x),int(y)]
			cv.DrawContours(frame, pupil, (0,0,0), (0,0,0), 2, cv.CV_FILLED)
			#cv.Circle(frame, (int(x),int(y)), 2, (0,255,0), int(r)*2)
			break
		contours = contours.h_next()
		i += 1
	return (frame)

def getIris(frame):
	grayImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.CvtColor(frame,grayImg,cv.CV_BGR2GRAY)
	cv.Smooth(grayImg,grayImg,cv.CV_GAUSSIAN,9,9)
	cv.Canny(grayImg, grayImg, 32, 2)
	storage = cv.CreateMat(grayImg.width, 1, cv.CV_32FC3)
	minRad = int(getRadius(pupilArea))
	circles = cv.HoughCircles(grayImg, storage, cv.CV_HOUGH_GRADIENT, 2, 10,32,200,minRad, minRad*2)
	cv.ShowImage("output", grayImg)
	while circles:
		cv.DrawContours(frame, circles, (0,0,0), (0,0,0), 2)
		print "circle!"
		circles = circles.h_next()
	return (frame)


cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
key = 0
while True:
	frame = cv.LoadImageM("images/R/S1001R02.jpg")
	output = getPupil(frame)
	cv.ShowImage("input", frame)
	iris = getIris(output)
	#cv.ShowImage("output", iris)
	key = cv.WaitKey(500)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyWindow("input")

