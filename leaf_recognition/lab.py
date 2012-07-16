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

import cv2
import cv
import os
import math
import numpy as np

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

R_low = 0
G_low = 100
B_low = 0
R_high = 104
G_high = 255
B_high = 76
corner = 1


imgSliderHSV = cv.CreateImage((300,200), 8, 3)
imgSliderRGB = cv.CreateImage((300,200), 8, 3)
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
def onSliderChangeHSV(n):
	global H_low
	global S_low
	global V_low
	global H_high
	global S_high
	global V_high
	global imgSliderHSV
	H_low = cv.GetTrackbarPos("H_low", "HSV module")
	S_low = cv.GetTrackbarPos("S_low", "HSV module")
	V_low = cv.GetTrackbarPos("V_low", "HSV module")
	H_high = cv.GetTrackbarPos("H_high", "HSV module")
	S_high = cv.GetTrackbarPos("S_high", "HSV module")
	V_high = cv.GetTrackbarPos("V_high", "HSV module")
	bgrColorLow = hsvToRgb((H_low, S_low, V_low))
	bgrColorHigh = hsvToRgb((H_high, S_high, V_high))
	cv.Rectangle(imgSliderHSV, (0,0), (150,200), bgrColorLow, cv.CV_FILLED)
	cv.Rectangle(imgSliderHSV, (151,0), (300, 200), bgrColorHigh, cv.CV_FILLED)
	cv.ShowImage("HSV module", imgSliderHSV)

##
# Sets the min and max RGB values
#
# Ajusta los valores minimos y maximos de RGB
#
# @param int		Some number
# @return void
def onSliderChangeRGB(n):
	global R_low
	global G_low
	global B_low
	global R_high
	global G_high
	global B_high
	global imgSliderRGB
	global corner
	R_low = cv.GetTrackbarPos("R_low", "RGB module")
	G_low = cv.GetTrackbarPos("G_low", "RGB module")
	B_low = cv.GetTrackbarPos("B_low", "RGB module")
	R_high = cv.GetTrackbarPos("R_high", "RGB module")
	G_high = cv.GetTrackbarPos("G_high", "RGB module")
	B_high = cv.GetTrackbarPos("B_high", "RGB module")
	corner = cv.GetTrackbarPos("corner", "RGB module")
	bgrColorLow = (B_low, G_low, R_low)
	bgrColorHigh = (B_high, G_high, R_high)
	cv.Rectangle(imgSliderRGB, (0,0), (150,200), bgrColorLow, cv.CV_FILLED)
	cv.Rectangle(imgSliderRGB, (151,0), (300, 200), bgrColorHigh, cv.CV_FILLED)
	cv.ShowImage("RGB module", imgSliderRGB)
	
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
def getBinaryImageHSV(frame, hsvMin, hsvMax):
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	hsvImg = cv.CreateImage(cv.GetSize(frame), 8, 3)
	cv.CvtColor(frame, hsvImg, cv.CV_BGR2HSV)
	cv.InRangeS(frame, hsvMin, hsvMax, resImg)
	del hsvImg
	return (resImg)


##
# Returns binary image according to the specified RGB range
#
# Regresa imagein binaria segun lo especificado por el rango
# RGB de entrada
#
# @param image		input image
# @param tuple		RGB min value
# @param tuple		RGB max value
# @returns image	binary image
def getBinaryImageRGB(frame, rgbMin, rgbMax):
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.InRangeS(frame, rgbMin, rgbMax, resImg)
	cv.Not(resImg, resImg)
	return (resImg)


##
# DEPRECATED
# Tried to be an optimized version of the getBinary function
# by drawing only contours bigger than a given size
#
# Intento de optimizacion de la funcion getBinary
# pintando solo los contornos mas grandes que un tamano dado
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
	
	return (b*255, g*255, r*255)

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

	hsvImg = cv.CreateImage(cv.GetSize(frame), 8, 3)
	cv.CvtColor(frame, hsvImg, cv.CV_BGR2HSV)
	hueChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	satChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	valChannel = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.Split(hsvImg, hueChannel, satChannel, valChannel, None)

	for y in range (0, frame.height):
		for x in range (0, frame.width):
			redValue = cv.GetReal2D(redChannel, y, x)
			greenValue = cv.GetReal2D(greenChannel, y, x)
			blueValue = cv.GetReal2D(blueChannel, y, x)
			sum = redValue + greenValue + blueValue + 0.0
			if (sum < 1.0):
				sum = 1.0
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

##
# Increase the saturation of the image
#
# Aumenta la saturacion de la imagen
#
# @param IplImage	imagen RGB
# @return IplImage	imagen RGB
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


##
# Computes the corner map in the binary image
#
# Computa el mapa de esquinas en la imagen binaria de entrada
#
# @param IplImage	binary image
# @return Mat		corner map
def getCornerMap(frame):
	global corner
	cornerMap = cv.CreateMat(frame.height, frame.width, cv.CV_32FC1)
	if (corner < 1):
		corner = 1
		cv.SetTrackbarPos("corner", "RGB module", 1)
	cv.CornerHarris(frame, cornerMap, corner)
	return (cornerMap)

##
# Draws the corner map on the specified image and returns it
#
# Pinta el mapa de esquinas en la imagen especificada y la regresa
#
# @param Mat		corner map
# @return IplImage	image with corner map drawn
def drawCornerMap(cornerMap, frame):
	for y in range(frame.height):
		for x in range(frame.width):
			harris = cv.Get2D(cornerMap, y, x)
			if (harris[0] > 10e-06):
				cv.Circle(frame, (x,y), 2, cv.RGB(255, 0,0))

##
# Isolate a sector of an image using a given WHITE mask
#
# Aisla un sector de la imagen dada una mascara BLANCA
#
# @param IplImage	image RGB
# @param IplImage	image single channel
# @return IplImage	image RGB isolated
def getMaskedImage(frame, mask):
	#cv.Not(myMask, myMask)
	rgbImg = cv.CreateImage(cv.GetSize(frame), 8, 3)
	resImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.Sub(frame, frame, rgbImg, mask)
	cv.CvtColor(rgbImg, resImg, cv.CV_BGR2GRAY)
	return (resImg)

##
# Returns a map of descriptors and keypoints based on the SURF technique
#
# Regresa un mapa de descriptores y puntos clave basado en la tecnica SURF
# @param IplImage	image gray
# @return tuple		keypoints, descriptors
def getFeatures(frame):
	surfer = cv2.SURF()
	# this line gives and error and could not be fixed
	# in order to go further
	# esta linea da un error y no pudo ser solucionado
	# a fin de continuar la investigacion
	#kp, descriptors = surfer.detect(frame, None, False)
	return (kp, descriptors)


##
# Saves the current masked image into the /images/isolated directory
# in order to get the example images for the SURF detector
#
# Guarda la actual imagen enmascarada en el directorio /images/isolated
# a fin de tener las imagenes de ejemplo para el detector SURF
def saveMaskedImage(name, frame):
	cv.SaveImage("images/isolated/"+name, frame)
	


# Window creation for showing input, output, sliders, etc
cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("binary", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("normalized", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("masked", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("HSV module", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("RGB module", cv.CV_WINDOW_AUTOSIZE)
cv.MoveWindow("input", 0, 0)
cv.MoveWindow("binary", 0, 0)

cv.CreateTrackbar("H_low", "HSV module", H_low, 179, onSliderChangeHSV)
cv.CreateTrackbar("S_low", "HSV module", S_low, 255, onSliderChangeHSV)
cv.CreateTrackbar("V_low", "HSV module", V_low, 255, onSliderChangeHSV)
cv.CreateTrackbar("H_high", "HSV module", H_high, 179, onSliderChangeHSV)
cv.CreateTrackbar("S_high", "HSV module", S_high, 255, onSliderChangeHSV)
cv.CreateTrackbar("V_high", "HSV module", V_high, 255, onSliderChangeHSV)

cv.CreateTrackbar("R_low", "RGB module", R_low, 255, onSliderChangeRGB)
cv.CreateTrackbar("G_low", "RGB module", G_low, 255, onSliderChangeRGB)
cv.CreateTrackbar("B_low", "RGB module", B_low, 255, onSliderChangeRGB)
cv.CreateTrackbar("R_high", "RGB module", R_high, 255, onSliderChangeRGB)
cv.CreateTrackbar("G_high", "RGB module", G_high, 255, onSliderChangeRGB)
cv.CreateTrackbar("B_high", "RGB module", B_high, 255, onSliderChangeRGB)
cv.CreateTrackbar("corner", "RGB module", corner, 255, onSliderChangeRGB)


cv.ShowImage("HSV module", imgSliderHSV)
cv.ShowImage("RGB module", imgSliderRGB)
# leaves list initialization with images from directory
leavesList = os.listdir('images/leaves')
leaf = getNewLeaf(leavesList)
isUpdate = True


isNormalized = False
normalizedImg = None
showNormalized = False
maskedImg = None
isPressedC = False
#onSliderChangeHSV(0)
onSliderChangeRGB(0)
while True:
	frame = cv.LoadImage("images/leaves/"+leaf)
	size = cv.GetSize(frame)
	cv.MoveWindow("output", size[0]+3, 0)
	if (isNormalized is False):
		# Deprecated because it's not suitable for the project
		# Abandonada porque no sirve para el proyecto
		# frame = saturate(frame)
		normalizedImg = normalizeImage(frame)
		isNormalized = True
		binImg = getBinaryImageRGB(normalizedImg, (B_low,G_low,R_low), (B_high,G_high,R_high))
	
	# Deprecated because it's not suitable for the project
	# Abandonadas porque no sirven para el proyecto
	# cornerMap = getCornerMap(binImg)
	# drawCornerMap(cornerMap, frame)

	maskedImg = getMaskedImage(frame, binImg)
	# gives error
	# keyPoints, descriptors = getFeatures(maskedImg)

	cv.ShowImage("input", frame)
	cv.ShowImage("normalized", normalizedImg)
	cv.ShowImage("binary", binImg)
	cv.ShowImage("masked", maskedImg)

	key = cv.WaitKey(30)
	if (key is 27 or key is 1048603):
		break
	elif (key is 32):
		leaf = getNewLeaf(leavesList)
		isNormalized = False
	elif (key is 67 or key is 99):
		isPressedC = True
	elif (key is 83 or key is 115):
		saveMaskedImage(leaf, maskedImg)
		

cv.DestroyAllWindows()

