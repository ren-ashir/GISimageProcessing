__author__ = 'Renat'
import math
import unittest
import numpy
def dist(p1,p2):
    return math.hypot(p1[0] - p2[0],p1[1] - p2[1])

def addEdgeToGraph (graph,pt,subtri):
    '''
    :param graph: Adjacency list
    :param pt: Geometry point
    :param subtri: Vertex id
    :return: empty
    Example:
    subtri = [3,1,2,0]
    In the Gragh will be added edge 3->1,1->2,2->0,0->3 with weight dist(pt[3],pt[1]) and so on
    '''
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

class TestAddEdgeToGraph(unittest.TestCase):
    def setUp(self): # Test initialization
        ds = dist([1,1],[2,2])
        self.test1_Graph = [[[1,ds]],[[0,ds]]]
    def test_1(self):
        print('TestAddEdgeToGraph1')
        graph = [[] for i in range(2)]
        addEdgeToGraph (graph,[[1,1],[2,2]],[0,1])
        self.assertEqual(self.test1_Graph,graph)
    def test_2(self):
        print('TestAddEdgeToGraph2')


def buildGraphFromTriMesh(pt,tri):
    '''
    :param pt:
    :param tri:
    :return:
    '''
    trilen = len(tri)
    if trilen == 0: return
    n = len(pt)
    graph = [[] for i in range(n)]
    for i in tri:
        if len(i) != 3:
           raise NameError('One cell of the tri should contain three elements')
        addEdgeToGraph(graph,pt,i) # add to the Graph all edges that
    return graph
class TestBuildGraphFromTriMesh(unittest.TestCase):
    def setUp(self):
        self.pt = [[2793,4273],
                   [2791,4275],
                   [2792,4274]]
        self.tri = [[0,1,2]]
        ds = [dist(self.pt[i], self.pt[(i + 1) % 3]) for i in range(3)]
        self.graph_result = [[[1,ds[0]],[2,ds[2]]],
                             [[0,ds[0]],[2,ds[1]]],
                             [[1,ds[1]],[0,ds[2]]]]
    def test_1(self):
       graph = buildGraphFromTriMesh (self.pt,self.tri)
       self.assertEqual(self.graph_result,graph)
       print ('TestBuildGraphFromTriMesh')
#print (dist([3,2],[1,1]))
#buildGraphFromTriMesh([[1,1],[2,2],[3,3]],[])
if __name__ == '__main__': # test only
    unittest.main()