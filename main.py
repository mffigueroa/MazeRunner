import pygame, sys
from pygame.locals import *
from math import *
import random

pygame.init()

# Set up the window 90% relative to the screen resolution
infoObject = pygame.display.Info()
screenWidth = 2**int(log(infoObject.current_w * 0.9, 2))
screenHeight = 2**int(log(infoObject.current_h * 0.9, 2))
smallestDimension = min(screenWidth, screenHeight)
screenCenter = (screenWidth / 2, screenHeight / 2)

print 'Dimensions: (%d, %d)' % (screenWidth, screenHeight)

DISPLAYSURF = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
pygame.display.set_caption('MazeRunner')

openingGap = 12.*pi/180.
gaps = [[x, pi/2 + x, pi + x, 3*pi/2 + x] for x in [0, pi*10./180, pi*20./180, pi*25./180, pi*30./180, pi*15./180, pi*25./180]]

levelSeparation = int(1024 * (153.1 - 13.3*len(gaps)) / smallestDimension) #85#int(smallestDimension*0.9 / len(gaps))
arcWidth = int((smallestDimension*0.9 - 2*(len(gaps) * levelSeparation)) / len(gaps))

print levelSeparation
print arcWidth
print (smallestDimension*0.9 - (len(gaps) * levelSeparation)) / len(gaps)

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

animIndex = 0
printed = True

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

def PolarToScreen(r, th):
    x = r*cos(th)
    y = r*sin(th)
    x += screenWidth / 2.0
    y = screenHeight / 2.0 - y
    return x, y

mousex, mousey = 0, 0
currGameLevel = 1

def ResetLevel():
    global currBotLevel
    global currBotGap
    global currBotRad
    global botSpeed
    global botRadius
    global currBlockingGapSelected
    global blockedGapsRenderInfo
    global blockedGaps

    currBotLevel = 0
    currBotGap = random.randint(0, len(gaps[0]) - 1)
    currBotRad = 0
    botSpeed = 0.5 + 0.1 * currGameLevel
    botRadius = 10
    currBlockingGapSelected = 0
    blockedGapsRenderInfo = set([])
    blockedGaps = set([])

blockedGapsRenderInfo = set([])
ResetLevel()

# run the game loop
while True:
    # check for any event updates
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                currBlockingGapSelected = (currBlockingGapSelected + 1) % len(gaps[currBotLevel])
            elif event.key == K_RIGHT:
                currBlockingGapSelected = (currBlockingGapSelected - 1) % len(gaps[currBotLevel])
            elif event.key == K_SPACE:
                blockedGapsRenderInfo.add(((currBotLevel + 1) * levelSeparation, gaps[currBotLevel][currBlockingGapSelected]))
                blockedGaps.add(currBlockingGapSelected)

                if currBlockingGapSelected == currBotGap:
                    print 'Blocked bot gap'
                    if len(blockedGaps) == len(gaps[currBotLevel]):
                        currGameLevel += 1
                        ResetLevel()
                    else:
                        print 'Still open gaps'
                        while currBotGap in blockedGaps:
                            currBotGap = random.randint(0, len(gaps[currBotLevel]) - 1)
                            print 'Trying gap #%d' % currBotGap
                        print 'Got new gap'

    DISPLAYSURF.fill(WHITE)

    # render the maze
    levelNum = 1
    for level in gaps:
        if not printed:
            print 'Level #%d' % levelNum
        for gapNum in range(len(level)):
            startAngle = level[gapNum] + openingGap#(openingGap / levelNum)
            stopAngle = level[(gapNum + 1) % len(level)]

            if startAngle > stopAngle:
                stopAngle += 2*pi

            radius = levelNum * levelSeparation
            rect = (screenCenter[0] - radius, screenCenter[1] - radius, radius * 2, radius * 2)
            if not printed:
                print 'Gap num: %d' % gapNum
                print 'Start Angle: %f deg, (%f)' % (startAngle * 180./pi, startAngle)
                print 'Stop Angle: %f deg, (%f)' % (stopAngle * 180./pi, stopAngle)
                print 'Radius: %d' % radius
                print 'Rect: %s' % repr(rect)
            pygame.draw.arc(DISPLAYSURF, BLUE, rect, startAngle, stopAngle, arcWidth)
        levelNum += 1

    # draw all the currently blocked off gaps
    for gap in blockedGapsRenderInfo:
        rect = (screenCenter[0] - gap[0], screenCenter[1] - gap[0], gap[0] * 2, gap[0] * 2)
        pygame.draw.arc(DISPLAYSURF, RED, rect, gap[1], gap[1] + openingGap, arcWidth)

    # draw the currently selected blocking gap
    currBlockingGapRadius = (currBotLevel + 1) * levelSeparation
    currBlockingGapSelectedRect = (screenCenter[0] - currBlockingGapRadius,
                                   screenCenter[1] - currBlockingGapRadius,
                                   currBlockingGapRadius * 2, currBlockingGapRadius * 2)
    currBlockingGapSelectedStartAngle = gaps[currBotLevel][currBlockingGapSelected]
    pygame.draw.arc(DISPLAYSURF, GREEN,
                    currBlockingGapSelectedRect, currBlockingGapSelectedStartAngle,
                    currBlockingGapSelectedStartAngle + openingGap, arcWidth)

    # draw the bot as it currently is
    botAngle = gaps[currBotLevel][currBotGap]
    botX, botY = PolarToScreen(currBotRad, botAngle)
    pygame.draw.circle(DISPLAYSURF, GREEN, (int(botX), int(botY)), botRadius)

    # update the bot's state
    currBotRad += botSpeed

    if currBotRad - botRadius > (currBotLevel + 1) * levelSeparation:
        blockedGaps = set([])
        if currBotLevel + 1 < len(gaps):
            currBotLevel += 1
            currBotGap = random.randint(0, len(gaps[currBotLevel]) - 1)
        else:
            botSpeed = 0

    # render the frame
    printed = True
    animIndex = (animIndex + 1) % 4
    pygame.display.update()
    fpsClock.tick(FPS)
