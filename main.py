import pygame, sys
from math import *
from pygame.locals import *

pygame.init()

# set up the window

infoObject = pygame.display.Info()

screenWidth = 2**int(log(infoObject.current_w * 0.9, 2))
screenHeight = 2**int(log(infoObject.current_h * 0.9, 2))
screenCenter = (screenWidth / 2, screenHeight / 2)

DISPLAYSURF = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
pygame.display.set_caption('Drawing')

openingGap = 25.*pi/360.
levelSeparation = 100
gaps = [[x, pi/2 + x, pi + x, 3*pi/2 + x] for x in [0, pi*20./360, pi*40./360, pi*60./360]]

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

animIndex = 0
printed = False

fontObj = pygame.font.Font('freesansbold.ttf', 32)

def GetTextSurf(text):
    textSurfaceObj = fontObj.render(text, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screenWidth - textSurfaceObj.get_width(), screenHeight - textSurfaceObj.get_height())
    return textSurfaceObj, textRectObj

def ScreenToPolar(x, y):
    newX = x - screenWidth / 2.0
    newY = screenHeight / 2.0 - y
    r = sqrt(newX**2 + newY**2)
    th = atan2(newY, newX)

    if newY < 0:
        th += 2*pi

    return r, th

mousex, mousey = 0, 0

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos

    DISPLAYSURF.fill(WHITE)

    mouseRadius, mouseAngle = ScreenToPolar(mousex, mousey)
    mouseAngle *= 180./pi
    mousePosStr = 'Screen: (%d, %d)   Polar: (%f, %f)' % (mousex, mousey, mouseRadius, mouseAngle)
    #mousePosStr = 'Screen: (%d, %d)   Polar: (%f, %f)' % (mousex, mousey, mousex - , mouseAngle)

    DISPLAYSURF.blit(*GetTextSurf(mousePosStr))

    levelNum = 1
    for level in gaps:
        if not printed:
            print 'Level #%d' % levelNum
        for gapNum in range(len(level)):
            startAngle = level[gapNum] + (openingGap / levelNum)
            stopAngle = level[(gapNum + 1) % len(level)]

            if startAngle > stopAngle:
                stopAngle += 2*pi

            radius = levelNum * levelSeparation
            rect = (screenCenter[0] - radius, screenCenter[1] - radius, radius * 2, radius * 2)
            if not printed and gapNum + 1 == len(level):
                print 'Gap num: %d' % gapNum
                print 'Start Angle: %f deg, (%f)' % (startAngle * 180./pi, startAngle)
                print 'Stop Angle: %f deg, (%f)' % (stopAngle * 180./pi, stopAngle)
                print 'Radius: %d' % radius
                print 'Rect: %s' % repr(rect)
            pygame.draw.arc(DISPLAYSURF, BLUE, rect, startAngle, stopAngle, 10)
        levelNum += 1

    printed = True
    animIndex = (animIndex + 1) % 4
    pygame.display.update()
    fpsClock.tick(FPS)