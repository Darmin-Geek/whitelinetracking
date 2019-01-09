import numpy as np
import argparse
import cv2

def main():
    originalImage = cv2.imread("/Users/hankinhomecomputer/Documents/newlinedarkthing.jpg")
    originalImage = cv2.bitwise_not(originalImage)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImage, 127, 255, 0)
    image2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image2, contours, -1, (100,255,0), 3)

    print(len(contours))

    cnt = contours[0]
    epsilon = 0.03*cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt,epsilon, True)
    maxx = 0
    maxy = 0
    for i in cnt:
       
        if(cnt[i][0][0][0][0] > maxx):
             if(cnt[i][0][0][0][1] > maxy):
                maxx=cnt[i][0][0][0][0]
                maxy=cnt[i][0][0][0][1]

    print(maxx)
    print(maxy)
    x2 = 0
    y2 = 1000000000
    maxy = 0
    for i in cnt:
       
        if(cnt[i][0][0][0][0] > x2):
             if(cnt[i][0][0][0][1] < y2):
                x2=cnt[i][0][0][0][0]
                y2=cnt[i][0][0][0][1]
    print(x2)
    print(y2)
    b = maxx-x2
    h=maxy-y2
    theta = np.arctan(b/h)
    print(b/h)
    print (theta)
    degrees=np.rad2deg(theta)
    print(degrees)

    cv2.drawContours(image2, [approx], -1, (100,255,0), 3)
    cv2.imshow("jackkk", image2)
    cv2.waitKey()
    

main()