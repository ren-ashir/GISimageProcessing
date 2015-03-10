__author__ = 'sovznd'
# find tree longest path based on the two DFS algorithm
# any cycle graph is not acceptable for this algo
import unittest
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

class TestbuildGraphFromMST(unittest.TestCase):
    def setUp(self):
        self.res = 40
        self.graph = [[[1,10]],
                      [[0,10],[2,30]],
                      [[1,30]]]
    def test_1(self):
       self.assertEqual(self.res,findTreeLngstPath(self.graph))

if __name__ == '__main__': # test only
    unittest.main()