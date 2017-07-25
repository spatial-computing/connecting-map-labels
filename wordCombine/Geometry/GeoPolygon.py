
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString
import numpy as np


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

class GeoPolygon:
    def __init__(self, points,word):

        self.polygon = Polygon(points)
        self.word = word
        self.center = self.polygon.centroid.coords[0]

        self.points = points
        self.lines = []
        for i in range(0,len(points)-1,1):
            line =LineString([points[i],points[i+1]])
            self.lines.append(line)





    def __str__(self):
        string = "The text is : " +self.word + "\n"
        coordinates = self.polygon.exterior.coords
        string  += ",".join("(%s,%s)" % tup for tup in coordinates)

        return string


    def is_the_same_polygon(self, poly2):
        if self.word != poly2.word:
            return False

        # todo need coordinates


        return True

    def get_area(self):
        #print self.polygon.area
        return self.polygon.area


    def get_overlap_polygon(self, polygon2):

        overlap = self.polygon.intersection(polygon2.polygon)
        return overlap.area

    def get_center_location(self):
        return self.center[0]* self.center[0]+self.center[1]* self.center[1]




    def find_orientation(self,polygon2):
        max = -1
        for line in self.lines:

            if max < line.length:
                l1 = line
                max = line.length
        max = -1


        for line in polygon2.lines:
            if max < line.length:
                l2= line
                max = line.length
        x1 =list(l1.coords)[0][0]-list(l1.coords)[1][0]
        y1 = list(l1.coords)[0][1] - list(l1.coords)[1][1]

        x2 =list(l2.coords)[0][0]-list(l2.coords)[1][0]
        y2 = list(l2.coords)[0][1] - list(l2.coords)[1][1]

        #print l1,l2
        #print x1,y1,x2,y2
        angle =angle_between((x1,y1),(x2,y2))

        if np.degrees(angle) >180:
            return 360-np.degrees(angle)
        else:
            return np.degrees(angle)

    def find_longest_line(self):
        max = -1
        for line in self.lines:

            if max < line.length:
                l1 = line
                max = line.length
        return l1

    def calculate_polygon_distabce(self,polygon2):
        len1= len(self.points)
        len2 = len(polygon2.points)
        minDis = 100000.00
        if len1 < len2:
            for p in self.points:
                point = Point(p)
                if point.distance(polygon2.polygon) <= minDis:
                    minDis = point.distance(polygon2.polygon)
        else:
            for p in polygon2.points:
                point = Point(p)
                if point.distance(self.polygon) <= minDis:
                    minDis = point.distance(self.polygon)
        #print "the min distance is %f" %(minDis)
        return minDis



if __name__ == '__main__':

    p1 = GeoPolygon([(0, 0), (1, 1), (1, 0),(0,0)],'ok')
    p2 = GeoPolygon([(0, 0), (0,1),(1, 1), (1, 0)], '2')
    #print p1
    #print p1.get_area()
    #p1.get_overlap_polygon(p2)