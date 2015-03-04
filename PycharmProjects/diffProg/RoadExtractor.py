__author__ = 'sovznd'
import cv2
import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform
# Test some idea for the read extraction problem based on the graph theory
# Slow method for finding a minimum spanning tree is implemented
# sources: http://peekaboo-vision.blogspot.ru/2012/02/simplistic-minimum-spanning-tree-in.html
def minimum_spanning_tree(X, copy_X=True):
    """X are edge weights of fully connected graph"""
    if copy_X:
        X = X.copy()

    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix of edge weights")
    n_vertices = X.shape[0]
    spanning_edges = []

    # initialize with node 0:
    visited_vertices = [0]
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    X[diag_indices, diag_indices] = np.inf

    while num_visited != n_vertices:
        new_edge = np.argmin(X[visited_vertices], axis=None)
        # 2d encoding of new_edge from flat, get correct indices
        new_edge = divmod(new_edge, n_vertices)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = np.inf
        X[new_edge[1], visited_vertices] = np.inf
        num_visited += 1
    return np.vstack(spanning_edges)

fileName = '1987165_masked.tif'
fileOutPutName = '1out' + fileName
img = cv2.imread(fileName)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,30,30,apertureSize = 3)
contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

print (len(contours))
for i in contours:
   L = []
   [L.append(x[0]) for x in i.tolist() if x[0] not in L] # not efficient an unique operation
   if len(i) > 2:
      # tri = Delaunay(i)
      # Pt = i[tri.simplices].tolist()[0]
      # print (Pt)
      # #print (,i,tri.simplices)
      P = L
      #print (P)
      X = squareform(pdist(P))
      edge_list = minimum_spanning_tree(X)
      #print (edge_list)
      #print (P)
      for edge in edge_list:
        i, j = edge
       # print (i,j)
      #  print ((P[i][0], P[j][0]),(P[i][1], P[j][1]))
        cv2.line(img,(P[i][0], P[i][1]),(P[j][0], P[j][1]),(0,255,0),2)
cv2.imwrite('out2' + fileOutPutName,img)
#cv2.cv.SaveImage('canny'+ fileOutPutName, cv2.cv.fromarray(edges))

