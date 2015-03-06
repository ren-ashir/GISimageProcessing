__author__ = 'Renat'
# kruskal's algorithm in Python with DSU data structure optimization
# PAY ATTENTION: It's implementation was not properly tested
import random
import unittest
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
'''
Test Kruskal's code
'''
import math
def dist(p1,p2):
    return math.hypot(p1[0] - p2[0],p1[1] - p2[1])
class TestKruskal(unittest.TestCase):
    def setUp(self):
        self.pt = [[2793,4273],
                   [2791,4275],
                   [2792,4274]]
        ds = [dist(self.pt[i], self.pt[(i + 1) % 3]) for i in range(3)]
        print (ds)
        self.graph = [[[1,ds[0]],[2,ds[2]]],
                      [[0,ds[0]],[2,ds[1]]],
                      [[1,ds[1]],[0,ds[2]]]]
        self.MSTgraph = [(0,2),(1,2)]
    def test_1(self):
        pass
        self.assertEqual(self.MSTgraph,Kruskal(self.graph))

if __name__ == '__main__': # test only
    unittest.main()