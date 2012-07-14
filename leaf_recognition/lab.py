#!/usr/bin/python
# @author	pctroll a.k.a. Jorge Palacios 10-87970
# @file		lab.py
#
# This program is the tool for analizing the characteristics
# of each leaf and make annotations about them in order to
# get them into the main program and compare results with
# the input provided.
#
# Este programa es la herramienta para analizar las caracteristicas
# de cada hoja y hacer anotaciones de las mismas a fin de
# colocarlas como entrada en el programa principal y comparar
# resultados con la entrada provista.

import cv
import os
import math

WIDTH = 0
HEIGHT = 1
AREA = 3

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


H_low = 0
S_low = 0
V_low = 0
H_high = 0
S_high = 0
V_high = 0
imgSlider = cv.CreateImage((300,200), 8, 3)
#####################################


# Returns a different image filename on each call. If there are no more
# elements in the list of images, the function resets.
#
# Retorna un archivo de imagen distinto en cada llamada. Si quedan
# elementos en la lista de imagen, la funcion reinicia.
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

# Sets the min and max HSV values
#
# Ajusta los valores minimos y maximos de HSV
#
# @param int		Some number
# @return void
def onSliderChange(n):
	global H_low
	global S_low
	global V_low
	global H_high
	global S_high
	global V_high
	global imgSlider
	H_low = cv.GetTrackbarPos("H_low", "HSV module")
	S_low = cv.GetTrackbarPos("S_low", "HSV module")
	V_low = cv.GetTrackbarPos("V_low", "HSV module")
	H_high = cv.GetTrackbarPos("H_high", "HSV module")
	S_high = cv.GetTrackbarPos("S_high", "HSV module")
	V_high = cv.GetTrackbarPos("V_high", "HSV module")
	bgrColorLow = hsvToRgb((H_low, S_low, V_low))
	bgrColorHigh = hsvToRgb((H_high, S_high, V_high))
	cv.Rectangle(imgSlider, (0,0), (150,200), bgrColorLow, cv.CV_FILLED)
	cv.Rectangle(imgSlider, (151,0), (300, 200), bgrColorHigh, cv.CV_FILLED)
	cv.ShowImage("HSV module", imgSlider)
	
##
# Returns binary image according to the specified HSV range
#
# Regresa imagein binaria segun lo especificado por el rango
# HSV de entrada
#
# @param image		input image
# @param tuple		HSV min value
# @param tuple		HSV max value
# @returns image	binary image
def getBinaryImage(frame, hsvMin, hsvMax):
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	hsvImg = cv.CreateImage(cv.GetSize(frame), 8, 3)
	cv.CvtColor(frame, hsvImg, cv.CV_BGR2HSV)
	cv.InRangeS(frame, hsvMin, hsvMax, resImg)
	del hsvImg
	return (resImg)

def getBinaryClean(frame):
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	copy = cv.CloneImage(frame)
	contours = cv.FindContours(copy, cv.CreateMemStorage(0), mode = cv.CV_RETR_EXTERNAL)
	while contours:
		moments = cv.Moments(contours)
		area = cv.GetCentralMoment(moments,0,0)
		if (area > 20):
			cv.DrawContours(resImg,contours,(255,255,255), (255,255,255), 2, cv.CV_FILLED)
		contours = contours.h_next()
	return (resImg)

##
# Returns a list of properties (area, width, height) from the input binary image
#
# Regresa una lista de caracteristicas (area, ancho, alto) a partir de la imagen binaria
# de entrada
#
# @param image		binary image
# @return list		properties
def getLeafProps(frame):
	area = -1
	centroid = (-1,-1)
	width = -1
	height = -1
	contours = cv.FindContours(frame, cv.CreateMemStorage(0), mode = cv.CV_RETR_EXTERNAL)
	while contours:
		moments = cv.Moments(contours)
		area = cv.GetCentralMoment(moments,0,0)
		if (area > 50):
			x = int(cv.GetSpatialMoment(moments,1,0)/area)
			y = int(cv.GetSpatialMoment(moments,0,1)/area)
			centroid = (x,y)
		contours = contours.h_next()
	properties = []
	properties.append(area)
	properties.append(centroid)
	# TODO: Finish the method in order to find the 
	#	width and height.
	return (properties)

##
# Transform HSV values to RGB values
#
# Tranforma valores HSV a RGB
#
# @param Scalar		HSV color structure
# @return Scalar	RGB color structure
def hsvToRgb(hsvColor):
	h = hsvColor[0]
	s = hsvColor[1]
	v = hsvColor[2]
	#normalize values range [0.0, 1.0]
	h /= 179.0
	s /= 255.0
	v /= 255.0
	
	i = math.floor(h*60)
	f = h * 60 - i
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	i = i % 6
	if (i is 0):
		r,g,b = v,t,p
	elif (i is 1):
		r,g,b = q,v,p
	elif (i is 2):
		r,g,b = p,v,t
	elif (i is 3):
		r,g,b = p,q,v
	elif (i is 4):
		r,g,b = t,p,v
	else:
		r,g,b = v,p,q
	
	return (r*255, g*255, b*255)

##
# Returns the normalized RGB image based on the implementation
# by Utkarsh Sinha
# http://www.aishack.in/2010/01/normalized-rgb/ 
#
# Regresa la imagen normalizada en RGB basado en la implementacion
# de Utkarsh Sinha
# http://www.aishack.in/2010/01/normalized-rgb/
#
# @param IplImage
# @return IplImage
def normalizeImage(frame):
	redChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	greenChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	blueChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	redAvg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	greenAvg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	blueAvg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 3)
	cv.Split(frame, blueChannel, greenChannel, redChannel, None)
	for y in range (0, frame.height):
		for x in range (0, frame.width):
			redValue = cv.GetReal2D(redChannel, y, x)
			greenValue = cv.GetReal2D(greenChannel, y, x)
			blueValue = cv.GetReal2D(blueChannel, y, x)
			sum = redValue + greenValue + blueValue + 0.0
			cv.SetReal2D(redAvg, y, x, redValue/sum*255)
			cv.SetReal2D(greenAvg, y, x, greenValue/sum*255)
			cv.SetReal2D(blueAvg, y, x, blueValue/sum*255)
	cv.Merge(blueAvg, greenAvg, redAvg, None, resImg)
	del redChannel
	del greenChannel
	del blueChannel
	del redAvg
	del greenAvg
	del blueAvg
	return (resImg)

def saturate(frame):
	cv.CvtColor(frame, frame, cv.CV_BGR2HSV)
	hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
	sat = cv.CreateImage(cv.GetSize(frame), 8, 1)
	val = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.Split(frame, hue, sat, val, None)
	for y in range(0, frame.height):
		for x in range(0, frame.width):
			saturation = cv.GetReal2D(sat, y, x)
			if (saturation < 200):
				saturation = saturation + 50
				cv.SetReal2D(sat, y, x, saturation)
	cv.Merge(hue, sat, val, None, frame)
	del hue
	del sat
	del val
	cv.CvtColor(frame, frame, cv.CV_HSV2BGR)
	return (frame)

#	
# Returns the number of corners on the image
#
# Regresa el numero de esquinas en la imagen
#
# @param image		binary image
# @returns int		number of corners 
def getLeafNumCorners(frame):
	corners = 0
	# TODO: Find the 
	return (corners)

# Window creation for showing input, output, sliders, etc
cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("clean", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("HSV module", cv.CV_WINDOW_AUTOSIZE)
cv.MoveWindow("input", 0, 0)
cv.MoveWindow("output", 0, 0)
cv.CreateTrackbar("H_low", "HSV module", H_low, 179, onSliderChange)
cv.CreateTrackbar("S_low", "HSV module", S_low, 255, onSliderChange)
cv.CreateTrackbar("V_low", "HSV module", V_low, 255, onSliderChange)
cv.CreateTrackbar("H_high", "HSV module", H_high, 179, onSliderChange)
cv.CreateTrackbar("S_high", "HSV module", S_high, 255, onSliderChange)
cv.CreateTrackbar("V_high", "HSV module", V_high, 255, onSliderChange)
cv.ShowImage("HSV module", imgSlider)
# leaves list initialization with images from directory
leavesList = os.listdir('images/leaves')
leaf = getNewLeaf(leavesList)
isUpdate = True
while True:
	frame = cv.LoadImage("images/leaves/"+leaf)
	size = cv.GetSize(frame)
	cv.MoveWindow("output", size[0]+3, 0)
	cv.ShowImage("input", frame)
	#clean = getBinaryClean(output)
	frame = saturate(frame)
	normalized = normalizeImage(frame)
	output = getBinaryImage(normalized, (H_low,S_low,V_low), (H_high,S_high,V_high))
	cv.ShowImage("output", output)
	#cv.ShowImage("clean", clean)
	props = getLeafProps(output)
	key = cv.WaitKey(30)
	#print "Properties"
	#print "\tarea: %f" % props[0]
	#print  "\tcentroid (%d, %d)" % (props[1][0], props[1][1])
	if (key == 27 or key == 1048603):
		break
	elif (key == 32):
		leaf = getNewLeaf(leavesList)

cv.DestroyAllWindows()

