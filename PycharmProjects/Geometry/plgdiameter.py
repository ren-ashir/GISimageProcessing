__author__ = 'sovznd'
#  The diameter of a set of points python
from scipy.spatial import ConvexHull
import numpy as np
import cv2

#create some points
np.random.seed(424242)
pts = np.random.rand(15, 2)
hull = ConvexHull(pts)
hull_pts = pts[hull.vertices,:] #clockwise order

#Create image
w = 1000
h = 1000
img = np.zeros((w,h,3), np.uint8)
img[:,0:w] = (255,255,255) # white colore

fileName = 'res.jpg'
hull_pts = [[int(j * h) for j in i] for i in hull_pts] # to pixel point
import math
def distLine2Pt (line,pt):
    x1,y1,x2,y2 = line
    x0,y0 = pt
    return abs (((x2-x1)*(y0-y1)-(y2-y1)*(x0-x1))/math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2))

def getPt(a,id):
    return a[id][0],a[id][1]

def distancePt2pt (a,b):
    x1,y1 = a
    x2,y2 = b
    return math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)
ptr2 = 2
resdist = 0
resline = 0,0
# two pointer method
for i in range(len(hull_pts)):
    ln = len(hull_pts)
    x1,y1 = getPt(hull_pts,i)
    x2,y2 = getPt(hull_pts,(i + 1) % ln)
    x3,y3 = getPt(hull_pts,ptr2 % ln)
    d1 = distLine2Pt((x1,y1,x2,y2),(x3,y3))
    while True: # shift a points position while the distance is increase
        d2 = distLine2Pt((x1,y1,x2,y2),getPt(hull_pts,(ptr2 + 1) % ln))
        if d2 > d1:
            ptr2 += 1
            d1 = d2
            x3,y3 = getPt(hull_pts,ptr2 % ln)
        else:
            break
    if distancePt2pt((x3,y3),(x1,y1)) > resdist:
        resdist = distancePt2pt((x3,y3),(x1,y1))
        resline = (x3,y3),(x1,y1)
    if distancePt2pt((x3,y3),(x2,y2)) > resdist:
        resdist = distancePt2pt((x3,y3),(x2,y2))
        resline = (x3,y3),(x2,y2)

    ptr2 += 1
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2) # green line
    cv2.circle(img,(x1,y1),10 + i * 10, ( 0, 0, 0 ), 4, 8 )

cv2.line(img,resline[0],resline[1],(255,0,0),2) # green line diameter
print resdist
cv2.imwrite(fileName,img)

