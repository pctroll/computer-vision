# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		iris_detection.py

import cv
import math
import numpy as np
import os

centroid = (0,0)
radius = 0
#magnitude = 0
currentEye = 0
eyesList = []

def getNewEye(list):
	global currentEye
	if (currentEye >= len(list)):
		currentEye = 0
	newEye = list[currentEye]
	currentEye += 1
	return (newEye)

def getCircles(image):
	i = 80
	while i < 151:
		storage = cv.CreateMat(image.width, 1, cv.CV_32FC3)
		cv.HoughCircles(image, storage, cv.CV_HOUGH_GRADIENT, 2, 100.0, 30, i, 100, 140)
		circles = np.asarray(storage)
		if (len(circles) == 1):
			return circles
		i +=1
	return ([])

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
	circles = getCircles(grayImg)	
	for circle in circles:
		rad = int(circle[0][2])
		global radius
		radius = rad
		cv.Circle(mask, centroid, rad, cv.CV_RGB(255,255,255), cv.CV_FILLED)
		cv.Not(mask,mask)
		cv.Sub(frame,copyImg,resImg,mask)
	return (resImg)
	
def getPolar2CartImg(image, center, rad):
	c = (float(center[0]), float(center[1]))
	imgRes = cv.CreateImage((rad*2, int(360)), 8, 3)
	cv.LogPolar(image,imgRes,c,25.0)
	return (imgRes)

cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("normalized", cv.CV_WINDOW_AUTOSIZE)

eyesList = os.listdir('images/R')
key = 0
while True:
	eye = getNewEye(eyesList)
	frame = cv.LoadImage("images/eyes/"+eye)
	iris = cv.CloneImage(frame)
	output = getPupil(frame)
	iris = getIris(output)
	cv.ShowImage("input", frame)
	cv.ShowImage("output", iris)
	normImg = cv.CloneImage(iris)
	normImg = getPolar2CartImg(iris,centroid,radius)
	cv.ShowImage("normalized", normImg)
	key = cv.WaitKey(3000)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyAllWindows()

