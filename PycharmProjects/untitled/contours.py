import cv2,numpy
import ImageColor

inputFile = '1987165_masked.tif'
outputImg = 'out' + inputFile
im = cv2.imread(inputFile)
edged = cv2.Canny(im, 30, 30)
cv2.cv.SaveImage('canny'+ outputImg, cv2.cv.fromarray(edged))
contours, hierarchy = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
#cv2.fastNlMeansDenoising(edged,edged,3, 5, 50)
#cv2.cv.SaveImage(outputImg, cv2.cv.fromarray(edged))
#cntrs = contours
cntrs = []
print (len(contours))
#cntrs.append(contours[9])
for i in contours:
    #epsilon = 0.1*cv2.arcLength(i,False)
    #cntrs.append(cv2.approxPolyDP(i,epsilon,False))
    rect = cv2.minAreaRect(i)
    box = cv2.cv.BoxPoints(rect)
    box = numpy.int0(box)
    if cv2.contourArea(box) < 1:
        continue
    r_x, r_y, r_w, r_h = cv2.boundingRect(i)
    # print (box)
    # print (r_w,r_h)
    mx = max (r_w,r_h)
    mn = min (r_w,r_h)
    # print (float(mn) / mx )
    #print (type(box))
    if mn / float(mx) < 0.5:
        cntrs.append([box])
        #print (box)
        #cntrs.append(i)
#cntrs = cntrs[1:]
#print (cntrs)
#row,cols = im.shape[:2]
#[vx,vy,x,y] = cv2.fitLine(cntrs,cv2.cv.CV_DIST_L2,0,0.01,0.01)
cn = 0
print (len(cntrs))
for i in cntrs:
   #print (i)
   cv2.drawContours(im,i,-1,(0,255,100),-1)
   cn += 1
cv2.cv.SaveImage('sqfilter' + outputImg, cv2.cv.fromarray(im))
# cv2.drawContours(im,cntrs,-1,(0,255,0),-1)
# cv2.cv.SaveImage('2OUT' + outputImg, cv2.cv.fromarray(im))



