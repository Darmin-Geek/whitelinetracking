import cv2
import numpy as np
imagine="Photo on 1-7-19 at 4.15 PM.jpg"

imagestart=cv2.imread(imagine)
imgray = cv2.cvtColor(imagestart,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(imagestart,cv2.COLOR_BGR2HSV)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imagestart, contours, -1, (0,255,0), 3)
lower_red = np.array([0,0,0])
upper_red = np.array([15,15,15])
mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(imagestart,imagestart, mask= mask)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.imshow("window title", imagestart)
cv2.waitKey()