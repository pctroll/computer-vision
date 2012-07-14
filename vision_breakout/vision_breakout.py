import pygame, cv, sys
from pygame.locals import *


# OpenCV 
capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 400)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 300)
def getCamFrame():
	global capture
	global src_rgb
	frame = cv.QueryFrame(capture)
	#src_rgb = cv.CreateMat(frame.width, frame.height, cv.CV_8UC3)
	src_rgb = cv.adaptors.Ipl2PIL(frame)
	pg_img = pygame.image.frombuffer(src_rgb.tostring(), cv.GetSize(src_rgb), "RGB")
	return pg_img

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300), 0, 32)
pygame.display.set_caption('Vision Breakout')

BLACK	= (0,0,0)
WHITE	= (255,255,255)
RED	= (255,0,0)
GREEN	= (0,255,0)
BLUE	= (0,0,255)

DISPLAYSURF.fill(WHITE)
running = True
mousepos = (0,0)
while running:
	camFrame = getCamFrame()
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == pygame.MOUSEMOTION:
			mousepos = event.pos
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(camFrame,(0,0))
	pygame.draw.circle(DISPLAYSURF, BLUE, (mousepos[0],280), 20, 0)
	pygame.display.update()

pygame.quit()
sys.exit()
