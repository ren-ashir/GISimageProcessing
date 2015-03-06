__author__ = 'Renat'


import math
import unittest
import numpy

def buildGraphFromMST(n,edges):
    m = len(edges)
    graph = [[] for i in range(n)]
    for a,b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph

class TestbuildGraphFromMST(unittest.TestCase):
    def setUp(self):
        self.edges = [(0,1),(1,2)]
        self.graph = [[1],
                      [0,2],
                      [1]]
    def test_1(self):
       self.assertEqual(self.graph,buildGraphFromMST(3,self.edges))
       print ('TestbuildGraphFromMST')

if __name__ == '__main__': # test only
    unittest.main()