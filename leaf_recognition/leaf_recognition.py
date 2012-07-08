#!/usr/bin/python
# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		leaf_recognition.py

import cv
import math
import numpy as np
import os

# GLOBAL VARIABLES
#####################################
# Holds the pupil's center
centroid = (0,0)
# Holds the iris' radius
radius = 0
# Holds the current element of the image used by the getNewEye function
currentLeaf = 0
# Holds the list of leaves (filenames)
leavesList = []
#####################################


# Returns a different image filename on each call. If there are no more
# elements in the list of images, the function resets.
#
# @param list		List of images (filename)
# @return string	Next image (filename). Starts over when there are
#			no more elements in the list.
def getNewLeaf(list):
	global currentLeaf
	if (currentLeaf >= len(list)):
		currentLeaf = 0
	newLeaf = list[currentLeaf]
	currentLeaf += 1
	return (newLeaf)

# Returns the cropped image with the isolated iris and black-painted
# pupil. It uses the getCircles function in order to look for the best
# value for each image (eye) and then obtaining the iris radius in order
# to create the mask and crop.
#
# @param image		Image with black-painted pupil
# @returns image 	Image with isolated iris + black-painted pupil
def getIris(frame):
	iris = []
	copyImg = cv.CloneImage(frame)
	resImg = cv.CloneImage(frame)
	grayImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	mask = cv.CreateImage(cv.GetSize(frame), 8, 1)
	storage = cv.CreateMat(frame.width, 1, cv.CV_32FC3)
	cv.CvtColor(frame,grayImg,cv.CV_BGR2GRAY)
	cv.Canny(grayImg, grayImg, 5, 70, 3)
	cv.Smooth(grayImg,grayImg,cv.CV_GAUSSIAN, 7, 7)
	circles = getCircles(grayImg)
	iris.append(resImg)
	for circle in circles:
		rad = int(circle[0][2])
		global radius
		radius = rad
		cv.Circle(mask, centroid, rad, cv.CV_RGB(255,255,255), cv.CV_FILLED)
		cv.Not(mask,mask)
		cv.Sub(frame,copyImg,resImg,mask)
		x = int(centroid[0] - rad)
		y = int(centroid[1] - rad)
		w = int(rad * 2
		cv.SetImageROI(resImg, (x,y,w,h))
		cropImg = cv.CreateImage((w,h), 8, 3)
		cv.Copy(resImg,cropImg)
		cv.ResetImageROI(resImg)
		return(cropImg)
	return (resImg)

# Search middle to big circles using the Hough Transform function
# and loop for testing values in the range [80,150]. When a circle is found,
# it returns a list with the circles' data structure. Otherwise, returns an empty list.

# @param image
# @returns list
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

# Returns the same images with the pupil masked black and set the global
# variable centroid according to calculations. It uses the FindContours 
# function for finding the pupil, given a range of black tones.

# @param image		Original image for testing
# @returns image	Image with black-painted pupil
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


# Window creation for showing input, output
cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)

cv.MoveWindow("input", 0, 0)
cv.MoveWindow("output", 0, 0)

leavesList = os.listdir('images/leaves')
key = 0
while True:
	leaf = getNewLeaf(leavesList)
	frame = cv.LoadImage("images/leaves/"+leaf)
	size = cv.GetSize(frame)
	cv.MoveWindow("output", size[0]+3, 0)
	cv.ShowImage("input", frame)
	key = cv.WaitKey(3000)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyAllWindows()

