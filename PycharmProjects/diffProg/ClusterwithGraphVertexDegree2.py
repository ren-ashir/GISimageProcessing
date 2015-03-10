import cv2
import numpy as np
import math
import time
from scipy.spatial import Delaunay

def getStrTime():
    L = time.asctime().split()
    return L[-1] + '_Time' + L[-2].replace(':','.') + L[-4] + L[-3]

def dist(p1,p2):
    return math.hypot(p1[0] - p2[0],p1[1] - p2[1])

def addEdgeToGraph (graph,pt,subtri):
    ln = len(subtri)
    for i in range(ln):
        fromPt = subtri[i]
        toPt = subtri[(i + 1) % ln]
        ds = dist(pt[fromPt],pt[toPt])
        # Since the [fromPt,ds],graph[toPt] element may already be stored in the graph we need if ...
        if [toPt,ds] not in graph[fromPt]: # O(n)
            graph[fromPt].append([toPt,ds])
        if [fromPt,ds] not in graph[toPt]: # O(n)
            graph[toPt].append([fromPt,ds])
    return graph

def buildGraphFromTriMesh(pt,tri):
    trilen = len(tri)
    if trilen == 0: return
    n = len(pt)
    graph = [[] for i in range(n)]
    for i in tri:
        if len(i) != 3:
           raise NameError('One cell of the tri should contain three elements')
        addEdgeToGraph(graph,pt,i) # add to the Graph all edges that
    return graph

import random

def dsuGet(p,v):
    if v != p[v]:
        p[v] = dsuGet(p,p[v])
    return p[v]

def dsuUnite (p,a,b):
    i = dsuGet(p,a)
    j = dsuGet(p,b)
    if random.choice((True,False)):
        i,j = j,i
    if i != j:
        p[i] = j

def Kruskal(graph):
    n = len(graph)
    edges = []
    for i in range(n): # edge extraction O(n + m) from the unordered graph with a double edge
        for j in range(len(graph[i])):
            to = graph[i][j][0]
            weight = graph[i][j][1]
            edges.append([weight,i,to])
    edges.sort() # O(m log m)
    m = len(edges)
    p = range(n)
    resMST = []
    for w,a,b in edges: # O (m)
        if dsuGet(p,a) != dsuGet(p,b): # If a and b in the different set ~ O(1)
            dsuUnite(p,a,b)  # union a and b vertex into the same set ~ O(1)
            resMST.append((a,b))
    # All Kruskal take O (m log m + n + m)
    # Simplification of O: since the m < n ^ 2 then  m log m < m log n^2 ( 2m log n)
    # and O (2 m log n + n + m) reduce to the O (m log n)
    return resMST

def buildGraphFromMST(pt,n,edges):
    m = len(edges)
    graph = [[] for i in range(n)]
    for a,b in edges:
        ds = dist(pt[a],pt[b])
        graph[a].append([b,ds])
        graph[b].append([a,ds])
    return graph

#geometry
# getDiameter funtion
from scipy.spatial import ConvexHull
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

def getDiameter (pts):
    hull = ConvexHull(pts)
    hull_pts = pts[hull.vertices,:] #clockwise order
    ptr2 = 2
    resdist = 0
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

        if distancePt2pt((x3,y3),(x2,y2)) > resdist:
            resdist = distancePt2pt((x3,y3),(x2,y2))
        ptr2 += 1
    return resdist
#graph lng
def findTreeLngstPath (graph):
    mx,v = dfsGo(graph,0)
    mx2,v2 = dfsGo(graph,v)
    return  max(mx,mx2)

def dfsGo(g,v,p=-1):
    mx = 0
    v1 = v
    for i in g[v]:
        to,w = i
        if to != p:
            mx2,v2 = dfsGo(g,to,v)
            if mx2 + w > mx:
                mx = mx2 + w
                v1 = v2
    return mx,v1


from scipy.spatial.distance import pdist, squareform
fileName = 'sample.png'
fileOutPutName = '1out' + fileName
img = cv2.imread(fileName)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,18,20,apertureSize = 3)
#cv2.imwrite('out3' + fileOutPutName,edges)
contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print (hierarchy)
print (len(contours))
C = 5
result = []
for i in contours:
   if len(i) > 2:
      #print (i)
      pt = [x[0] for x in i.tolist()]
      for x in i.tolist(): # check it
          if len(x) > 1:
              raise NameError('We get it len(x) > 1')
      ar = np.array([x[0] for x in i])
      diameterOfCntr = getDiameter(ar)
      #print diameterOfCntr
      tri = Delaunay(ar)
      Pt = tri.simplices
      #print (Pt.tolist())
      #cv2.line(img,(P[i][0], P[i][1]),(P[j][0], P[j][1]),(0,255,0),2)
      # if C == 0:
      #     break
      C -= 1
      graph = buildGraphFromTriMesh(pt,Pt.tolist())


      #print graph
      n = len(graph)
      countDeg = 0
      MST = Kruskal(graph)
      m = len(MST)
      graph = buildGraphFromMST (pt,n,MST)
      lngthPath = findTreeLngstPath(graph)
      #print diameterOfCntr,lngthPath

      countDeg = len([1 for i in graph if len(i) > 2])
      # for i in graph:
      #     if len(i) > 2:
      #         countDeg += 1
      #print (pt)
      if diameterOfCntr > lngthPath * 4.5 / 5.0: # < m / 15:
          for a,b in MST:
            cv2.line(img,(pt[a][0],pt[a][1]),(pt[b][0],pt[b][1]),(0,255,0),2)
      #result.append([pt,])
# for x in result: # Output
#     print x
cv2.imwrite(getStrTime() + fileOutPutName,img)