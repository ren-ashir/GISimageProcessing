import cv2
import numpy as np
import math
from scipy.spatial import Delaunay

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

def buildGraphFromMST(n,edges):
    m = len(edges)
    graph = [[] for i in range(n)]
    for a,b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph

from scipy.spatial.distance import pdist, squareform
fileName = 'sample.png'
fileOutPutName = '1out' + fileName
img = cv2.imread(fileName)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,30,30,apertureSize = 3)
cv2.imwrite('out3' + fileOutPutName,edges)
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
      tri = Delaunay(ar)
      Pt = tri.simplices
      #print (Pt.tolist())
      #cv2.line(img,(P[i][0], P[i][1]),(P[j][0], P[j][1]),(0,255,0),2)
      # if C == 0:
      #     break
      C -= 1
      graph = buildGraphFromTriMesh(pt,Pt.tolist())
      n = len(graph)
      countDeg = 0
      MST = Kruskal(graph)
      m = len(MST)
      graph = buildGraphFromMST (n,MST)
      for i in graph:
          if len(i) > 2:
              countDeg += 1
      #print (pt)
      for a,b in MST:
          cv2.line(img,(pt[a][0],pt[a][1]),(pt[b][0],pt[b][1]),(0,255,0),2)
      #result.append([pt,])
# for x in result: # Output
#     print x
cv2.imwrite('out2' + fileOutPutName,img)