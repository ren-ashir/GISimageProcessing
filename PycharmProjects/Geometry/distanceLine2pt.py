__author__ = 'sovznd'
# the distance from a point to a line python
import unittest
import math
def distLine2Pt (line,pt):
    x1,y1,x2,y2 = line
    x0,y0 = pt
    return abs ((x2-x1)*(y0-y1)-(y2-y1)*(x0-x1)/math.sqrt((x2-x1) ** 2 + (y2 - y1) ** 2))

class TestDist(unittest.TestCase):
    def setUp(self):
        self.line = (0,0,0,10)
        self.pt = (10,10)
        self.res = 10
    def test_1(self):
       self.assertEqual(self.res,distLine2Pt(self.line,self.pt))
    def test_2(self):
        self.assertEqual(0,distLine2Pt(self.line,(0,0)))

if __name__ == '__main__': # test only
    unittest.main()