import numpy as np
import argparse
import cv2
import math
import sys

def getX(contour, index):
    return contour[index][0][0]

def getY(contour, index):
    return contour[index][0][1]

def main():
    originalImage = cv2.imread("C:/Users/alejandro/Desktop/80invertcrop.jpg")
    originalImage = cv2.bitwise_not(originalImage)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImage, 127, 255, 0)
    image2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image2, contours, -1, (100,255,0), 3)

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
    radians = top/float(bottom)
    print(abs(math.degrees(math.atan(radians))))

    cv2.drawContours(image2, [approx], -1, (100,255,0), 3)

    #cirlce points
    print(x2, y2)
    print(x1, y1)
    cv2.circle(image2,(x1,y1),10,(255,0,0))
    cv2.circle(image2,(x2,y2),10,(255,0,0))
    cv2.imshow("angle", image2) # highlights two points used to get angle
    cv2.waitKey()

    #get *top* left point
    xT = sys.maxsize
    yT = sys.maxsize
    for i in range(len(cnt)):
        if(getY(cnt, i) < yT or ((getY(cnt, i) == yT) and getX(cnt, i) < xT)):
            xT=getX(cnt,i)
            yT=getY(cnt,i)

    #get bottom *left* point
    xB = sys.maxsize
    yB = -1
    for i in range(len(cnt)):
        if(getX(cnt, i) < xB or ((getX(cnt, i) == xB) and getY(cnt, i) > yB)):
            xB=getX(cnt,i)
            yB=getY(cnt,i)
    #circle all points
    cv2.circle(image2,(xT,yT),10,(255,0,0))
    cv2.circle(image2,(xB,yB),10,(255,0,0))
    cv2.imshow("allPoints",image2) #highlights all four points
    cv2.waitKey()
main()
