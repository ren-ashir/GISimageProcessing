import cv2,numpy
import gdal
import gdalconst
threshold = 99
shadow = True
history = 0
MOG = cv2.BackgroundSubtractorMOG2() #history,threshold,shadow)
# nmixtures = 5
# backgroundratio = 0.9
# noisesigma = 10
# MOG = cv2.BackgroundSubtractorMOG(history,nmixtures,backgroundratio,noisesigma)
# print dir(MOG)
#MOG2 = cv2.BackgroundSubtractorMOG2()
img = '2010189_masked.tif'
img2 = '1987165_masked.tif'
frame = cv2.imread(img)
frame2 = cv2.imread(img2)
#cv2.imshow('Img1',frame)
#cv2.imshow('Img2',frame2)
fgmask1 = MOG.apply(frame)
fgmask2 = MOG.apply(frame2)
#cv2.imshow('Mask',fgmask2)
#print len(fgmask1)
cv2.waitKey(0)
outputFile = 'Output_do.tif'
cv2.cv.SaveImage(outputFile ,  cv2.cv.fromarray(fgmask2))
# transform
filepath = img
ds = gdal.Open(filepath, gdalconst.GA_ReadOnly)
gt = ds.GetGeoTransform()
proj = ds.GetProjection()


filepath2 = outputFile
dsnew = gdal.Open(filepath2, gdalconst.GA_Update)
dsnew.SetGeoTransform(gt)
dsnew.SetProjection(proj)
dsnew=None
ds=None