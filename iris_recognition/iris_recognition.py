# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		iris_detection.py

import cv
import math
import numpy as np

centroid = (0,0)
radius = 0
magnitude = 0

def getPupil(frame):
	pupilImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.InRangeS(frame, (30,30,30), (80,80,80), pupilImg)
	contours = cv.FindContours(pupilImg, cv.CreateMemStorage(0), mode = cv.CV_RETR_EXTERNAL)
	del pupilImg
	pupilImg = cv.CloneImage(frame)
	while contours:
		moments = cv.Moments(contours)
		area = cv.GetCentralMoment(moments,0,0)
		if (area > 50):
			pupilArea = area
			x = cv.GetSpatialMoment(moments,1,0)/area
			y = cv.GetSpatialMoment(moments,0,1)/area
			pupil = contours
			global centroid
			centroid = (int(x),int(y))
			cv.DrawContours(pupilImg, pupil, (0,0,0), (0,0,0), 2, cv.CV_FILLED)
			break
		contours = contours.h_next()
	return (pupilImg)

def getIris(frame):
	copyImg = cv.CloneImage(frame)
	resImg = cv.CloneImage(frame)
	grayImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	mask = cv.CreateImage(cv.GetSize(frame), 8, 1)
	storage = cv.CreateMat(frame.width, 1, cv.CV_32FC3)
	cv.CvtColor(frame,grayImg,cv.CV_BGR2GRAY)
	cv.Canny(grayImg, grayImg, 5, 70, 3)
	cv.Smooth(grayImg,grayImg,cv.CV_GAUSSIAN, 7, 7)
	cv.HoughCircles(grayImg, storage, cv.CV_HOUGH_GRADIENT, 2, 100.0, 30, 150, 100, 140)
	circles = np.asarray(storage)
	for circle in circles:
		rad = int(circle[0][2])
		global radius
		radius = rad
		cv.Circle(mask, centroid, rad, cv.CV_RGB(255,255,255), cv.CV_FILLED)
		cv.Not(mask,mask)
		cv.Sub(frame,copyImg,resImg,mask)
	return (resImg)
	


cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("normalized", cv.CV_WINDOW_AUTOSIZE)

key = 0
while True:
	frame = cv.LoadImage("images/R/S1001R02.jpg")
	iris = cv.CloneImage(frame)
	output = getPupil(frame)
	iris = getIris(output)
	x = float(centroid[0])
	y = float(centroid[1])
	cv.ShowImage("input", frame)
	cv.ShowImage("output", iris)
	size = cv.GetSize(frame)
	size = (int(size[0]), int(size[1]*3.14))
	normImg = cv.CreateImage(size, 8, 3)
	cv.LogPolar(iris, normImg, (x,y), 40)
	cv.ShowImage("normalized", normImg)
	key = cv.WaitKey(1000)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyAllWindows()

