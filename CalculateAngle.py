import cv2
import numpy as np
import argparse
import cv2
import math
import sys
import time

def getX(contour, index):
    return contour[index][0][0]

def getY(contour, index):
    return contour[index][0][1]

def findCenter(img):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]
    return [width/2, height/2]

def findDistance(centerArray, xTopRight, xTopLeft, xBottomRight, angle):
    xLineCenter = .5 * (xTopLeft + xBottomRight)
    if (xTopRight - xTopLeft) == 0:
        return 0
    center = centerArray[0]
    if (angle == 0):
        return 0
    a = (2 / math.sin(angle))
    angledSideLength = xTopRight - xTopLeft
    distance = (a * (xLineCenter - center))/(xTopRight - xTopLeft)
    #if negative, line is on left side
    return distance

def findDistance2(xBottomRight, xBottomLeft, yBottomRight, yBottomLeft, image):
    x2Actual = xBottomRight - findCenter(image)[0]
    y2Actual = yBottomRight - findCenter(image)[1]
    x1Actual = xBottomRight - findCenter(image)[0]
    y1Actual = yBottomRight - findCenter(image)[1]

    yAvg = (y1Actual + y2Actual) * .5
    xAvg = (x1Actual + x2Actual) * .5
    #slope = (y1Actual - y2Actual)/(x1Actual - x2Actual)

    #offset = (yAvg * slope) + xAvg

    offset = yAvg * (x1Actual - x2Actual)/(y2Actual - y1Actual) + xAvg
    
    d = math.sqrt((xBottomLeft-xBottomRight)*(xBottomLeft-xBottomRight)+(yBottomLeft-yBottomRight)*(yBottomLeft-yBottomRight))

    theRealDistanceThatWeReallyNeed = 2*d/offset
    
    return theRealDistanceThatWeReallyNeed 

cap = cv2.VideoCapture(1)

def main():
    while(1):
        ret, frame = cap.read()
        originalImage=frame
        originalImage = cv2.bitwise_not(originalImage)
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grayImage, 175, 255, 0)
        image2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print("Must be 1: " + str(len(contours)))

        cnt = contours[0]
        epsilon = 0.03*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,epsilon, True)
        
        x2 = -1
        y2 = sys.maxsize
        #get top *right* point
        for i in range(len(cnt)):
            if(getX(cnt, i) > x2 or ((getX(cnt, i) == x2) and getY(cnt, i) < y2)):
                x2=getX(cnt,i)
                y2=getY(cnt,i)

        x1 = -1
        y1 = -1
        #get *bottom* right point
        for i in range(len(cnt)):
            if(getY(cnt, i) > y1 or ((getY(cnt, i) == y1) and getX(cnt, i) > x1)):
                x1=getX(cnt,i)
                y1=getY(cnt,i)

        top = y2-y1
        bottom = x2-x1
        radians = None
        if (top == 0 or bottom == 0):
            radians = 0
        else:
            radians = top/float(bottom)
        print(abs(math.degrees(math.atan(radians)))) # bottom right angle rotated (range 0-90 exclusive)

        cv2.drawContours(image2, [approx], -1, (100,255,0), 3)

        # plan:
        #   1. get bottommost point
        #   2. if there are other points on the same y value, it's cut off on the bottom
        #   3. get left and rightmost point with y value +- 2 of bottom y
        yBot = -1
        xBot = None
    
        #get the bottommost point
        for i in range(len(cnt)):
            if (getY(cnt, i) > yBot):
                xBot = getX(cnt, i)
                yBot = getY(cnt, i)

        # if the bottommost point is at the bottom of the image, it's probably cut off
        imageHeight, imageWidth = image2.shape
        cutoffBuffer = 3
        cutoff = (imageHeight - cutoffBuffer) <= yBot

        leftX = sys.maxsize
        leftY = None
        rightX = -1
        rightY = None
        if (cutoff):
            print ("cutoff")
            for i in range(len(cnt)):
                # look at points within +- 2 of the line
                if (getY(cnt, i) > yBot - 2 and getY(cnt, i) < yBot + 2):
                    if (getX(cnt, i) < leftX):
                        leftX = getX(cnt, i)
                        leftY = getY(cnt, i)
                    if (getX(cnt, i) > rightX):
                        rightX = getX(cnt, i)
                        rightY = getY(cnt, i)
        else:
            print ("not cutoff")
            for i in range(len(cnt)):
                if (getX(cnt, i) < leftX):
                    leftX = getX(cnt, i)
                    leftY = getY(cnt, i)
                if (getX(cnt, i) > rightX):
                    rightX = getX(cnt, i)
                    rightY = getY(cnt, i)
            # if the leftmost point is lower than the rightmost point
            if (leftY > rightY):
                # the bottommost point is the bottom right point
                rightX = xBot
                rightY = yBot
            else:
                # the bottommost point is the bottom left point
                leftX = xBot
                leftY = yBot
        print
        print (xBot, yBot)
        print (leftX, leftY)
        print (rightX, rightY)
        print
        cv2.circle(image2,(leftX,leftY),10,(255,0,0))
        cv2.circle(image2,(rightX,rightY),10,(255,0,0))        
        
        print("distance (inches): ",findDistance2(rightX, leftX, rightY, leftY, image2))
        cv2.imshow("allPoints",image2) #highlights all four points
        time.sleep(0.01)
        cv2.waitKey(1)  
main()
