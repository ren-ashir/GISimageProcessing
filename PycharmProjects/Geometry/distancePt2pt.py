__author__ = 'sovznd'

import math
# Y = pdist(X, 'euclidean')  in scipy.spatial.distance.pdist
def distancePt2pt (a,b):
    x1,y1 = a
    x2,y2 = b
    return math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)

print (distancePt2pt((1,1),(2,2)))