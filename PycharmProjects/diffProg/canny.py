__author__ = 'svzr'
import cv2,numpy
# Finding contours
fileName = '1987165_masked.tif'
img = cv2.imread(fileName)
outputImg = 'Canny_' + fileName
edges = cv2.Canny(img,50,50)
cv2.cv.SaveImage(outputImg, cv2.cv.fromarray(edges))