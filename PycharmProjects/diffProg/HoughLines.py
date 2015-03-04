__author__ = 'sovznd'
import cv2
import numpy as np
fileName = '1987165_masked.tif'
fileOutPutName = 'out' + fileName
img = cv2.imread(fileName)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,30,30,apertureSize = 3)
cv2.cv.SaveImage('canny'+ fileOutPutName, cv2.cv.fromarray(edges))
minLineLength = 1000
maxLineGap = 2
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite(fileOutPutName,img)


lines = cv2.HoughLinesP(edges,1,np.pi/180,10,30,10)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('out2' + fileOutPutName,img)