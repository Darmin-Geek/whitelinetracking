# Alejandro's general color filtering code
# Can be converted into a function and used like an API for the actual vision code

# 2018-09-12 update: refilters same image but this doesn't actually help. it just closes the bounds
#           the original image needs to be overlaid and the filtered version needs to be applied to the end product
# 2018-09-13 - filters original image multiple times but adds all of the filtered images together to display
#           python mamacita.py -i C:/Users/alejandro/Desktop/elmo.jpg -b 220 150 150 255 255 255 -b 210 100 40 255 210 140 -b 235 45 50 255 100 120 -b 0 0 0 190 30 30
#               use with the elmo jpg

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, nargs=1, help = "path to image")
ap.add_argument("-b", "--bounds", action="append", type=int, nargs=6, help = "R G B R G B (0-255)")
#ap.add_argument("-l", "--lower", type=int, nargs=3, help = "R G B (0-255)")
#ap.add_argument("-u", "--upper", type=int, nargs=3, help = "R G B (0-255)")
args = vars(ap.parse_args())

def filter(image, bounds):
    lower = np.array([bounds[2], bounds[1], bounds[0]], dtype = "uint8")
    upper = np.array([bounds[5], bounds[4], bounds[3]], dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.bitwise_not(mask)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output

def main():
    originalImage = cv2.imread(args["image"][0])
    finalImage = cv2.bitwise_not(originalImage)

    for i in range(len(args["bounds"])):
        if i == 0:
            finalImage = filter(originalImage, args["bounds"][i])
        else:
            finalImage = finalImage + filter(originalImage, args["bounds"][i])

    kernel = np.ones((2,2),np.uint8)
    filteredImage = cv2.erode(finalImage, kernel, iterations = 1)
    filteredImage = cv2.dilate(finalImage, np.ones((3,3),np.uint8), iterations = 3)
    invertedimage = cv2.bitwise_not(filteredImage)
    imhsv = cv2.cvtColor(filteredImage,cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(ixmgray,127,255,0)
    ret,thresh = cv2.threshold(imhsv,150,255,cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(invertedimage, contours, -1, (0,255,0), 3)
   

    for c in contours:
        epsilon = 0.1* cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

    cv2.drawContours(filteredImage, [approx], -1, (0, 255, 0), 4)
    cv2.drawContours(invertedimage, [approx], -1, (0,255,0), 3)
    cv2.drawContours(imhsv, [approx], -1, (0,255,0), 3)
    cv2.imshow("hsv", imhsv)
    cv2.imshow("mamacita", filteredImage)
    
    cv2.imshow("end result", invertedimage)
    
    cv2.waitKey(0)
main()
