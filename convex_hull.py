from typing import List

from which_pyqt import PYQT_VER
import math

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # MY FUNCTIONS
    # Used to help the quick sort algorithm below, sortPointsByX()
    #
    def partition(self, array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j].x() > pivot.x():
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])

        (array[i + 1], array[high]) = (array[high], array[i + 1])
        return i + 1

    # A quick sort algorithm to sort the inital unsorted points by x value.
    # This is a O(n log n) tiem complexity (given from wikipedia).
    def sortPointsByX(self, array, low, high):
        if low < high:
            pi = self.partition(array, low, high)
            self.sortPointsByX(array, low, pi - 1)
            self.sortPointsByX(array, pi + 1, high)

    # This is used to get the slope - constant time
    def getSlope(self, p1, p2) -> int:
        return (p1.y() - p2.y())/(p1.x() - p2.x())

    # Get the left-most point - n time
    def findLeftMostPointIndex(self, points) -> int:
        leftMostIndex = 0
        while points[leftMostIndex + 1].x() < points[leftMostIndex].x():
            leftMostIndex += 1
            if leftMostIndex + 1 >= len(points):
                break
        return leftMostIndex

    # Get the next point - constant time
    def getNextPointIndex(self, points, index, clockwise: bool):
        if clockwise:
            if len(points) == index + 1:
                return 0
            else:
                return index + 1
        else:
            if index == 0:
                return len(points) - 1
            else:
                return index - 1

    # The main function to get the convex hull - it will run log(n) times
    # In this function there are two while loops, each with O(n) time complexity
    # Therefore, we get O(n log n) time for this algorithm. The tiem complexities of
    # each function can be found above the corresponding funciton.
    def getConvexHull(self, points) -> list:
        if len(points) <= 3:
            if len(points) == 3 and self.getSlope(points[0], points[1]) < self.getSlope(points[0], points[2]):
                (points[1], points[2]) = (points[2], points[1])
        else:
            # get hulls
            midIndex = math.floor(len(points) / 2)
            hull1 = self.getConvexHull(points[0: midIndex])
            hull2 = self.getConvexHull(points[midIndex:])

            # set up variables to get top and bottom lines
            indexTop1 = self.findLeftMostPointIndex(hull1)
            indexTop2 = 0

            indexBottom1 = indexTop1
            indexBottom2 = 0

            nextIndex1 = (indexTop1 + 1) if indexTop1 + 1 != len(hull1) else 0
            nextIndex2 = len(hull2) - 1

            slope = self.getSlope(hull1[indexTop1], hull2[indexTop2])
            slopeNew1 = self.getSlope(hull1[nextIndex1], hull2[indexTop2])
            slopeNew2 = self.getSlope(hull1[indexTop1], hull2[nextIndex2])

            # find top two points - linear time
            while slope < slopeNew1 or slope > slopeNew2:
                if slope < slopeNew1:
                    indexTop1 = nextIndex1
                    nextIndex1 = self.getNextPointIndex(hull1, nextIndex1, True)
                if slope > slopeNew2:
                    indexTop2 = nextIndex2
                    nextIndex2 = self.getNextPointIndex(hull2, nextIndex2, False)

                slope = self.getSlope(hull1[indexTop1], hull2[indexTop2])
                slopeNew1 = self.getSlope(hull1[nextIndex1], hull2[indexTop2])
                slopeNew2 = self.getSlope(hull1[indexTop1], hull2[nextIndex2])

            nextIndex1 = indexBottom1 - 1 if indexBottom1 != 0 else len(hull1) - 1
            nextIndex2 = 1

            slope = self.getSlope(hull1[indexBottom1], hull2[indexBottom2])
            slopeNew1 = self.getSlope(hull1[nextIndex1], hull2[indexBottom2])
            slopeNew2 = self.getSlope(hull1[indexBottom1], hull2[nextIndex2])

            # find bottom two points - linear time
            while slope > slopeNew1 or slope < slopeNew2:
                if slope > slopeNew1:
                    indexBottom1 = nextIndex1
                    nextIndex1 = self.getNextPointIndex(hull1, nextIndex1, False)
                if slope < slopeNew2:
                    indexBottom2 = nextIndex2
                    nextIndex2 = self.getNextPointIndex(hull2, nextIndex2, True)
                slope = self.getSlope(hull1[indexBottom1], hull2[indexBottom2])
                slopeNew1 = self.getSlope(hull1[nextIndex1], hull2[indexBottom2])
                slopeNew2 = self.getSlope(hull1[indexBottom1], hull2[nextIndex2])

            # concatenate the two arrays - linear time
            points = hull1[0:indexBottom1 + 1] + ((hull2[indexBottom2:] + hull2[0:1]) if indexTop2 == 0 else (hull2[indexBottom2:indexTop2 + 1])) + ([] if indexTop1 == 0 else hull1[indexTop1:])

        return points

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        self.sortPointsByX(points, 0, len(points) - 1)
        t2 = time.time()

        t3 = time.time()
        points = self.getConvexHull(points)
        polygon = [QLineF(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
