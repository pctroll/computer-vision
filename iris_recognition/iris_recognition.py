# @author	pctroll a.k.a Jorge Palacios 10-87970
# @file		iris_detection.py

import cv



def getPupil(frame):
	pupilImg = cv.CreateImage(cv.GetSize(frame), 8, 1)
	cv.InRangeS(frame, (30,30,30), (80,80,80), pupilImg)
	contours = cv.FindContours(pupilImg, cv.CreateMemStorage(0), mode = cv.CV_RETR_EXTERNAL)
	del pupilImg
	pupil = []
	x,y = -10, -10
	i = 0
	while contours:
		moments = cv.Moments(contours)
		area = cv.GetCentralMoment(moments,0,0)
		if (area > 50):
			x = cv.GetSpatialMoment(moments,1,0)/area
			y = cv.GetSpatialMoment(moments,0,1)/area
			pupil = contours
			point = [int(x),int(y)]
			cv.DrawContours(frame, pupil, (0,0,0), (0,0,0), 2, cv.CV_FILLED)
			cv.Circle(frame, (int(x),int(y)), 2, (0,255,0), 5)
			break
		contours = contours.h_next()
		i += 1
	return (frame)


cv.NamedWindow("input", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("output", cv.CV_WINDOW_AUTOSIZE)
key = 0
while True:
	frame = cv.LoadImageM("images/R/S1001R02.jpg")
	cv.ShowImage("input", frame)
	output = getPupil(frame)
	cv.ShowImage("output", output)
	key = cv.WaitKey(500)
	# seems like Esc with NumLck equals 1048603
	if (key == 27 or key == 1048603):
		break

cv.DestroyWindow("input")

