"""
Implementation of the line finding algorithm based on the 
paper 'AN EFFICIENT ALGORITHM FOR LINE RECOGNITION BASED ON 
INTEGER ARITHMETIC' of Khalid Daghameen and Nabil Arman
 -- http://staff.ppu.edu/narman/cp11.pdf

# Filename: linefinding.py
# Author: Thomas Osterland
# Date created: 10/30/2015
# Python version: 2.7
"""

import numpy
import math

class VisitedMatrix(object):
    """
    Keeps track of the visited pixels in the image
    """
    _visited_matrix = None

    def __init__(self, image=None):
        """
        Creates a matrix that tracks the visited pixels of an
        underlying image.
        """
        if None == image:
            raise ValueError("Image must be set" )

        self._visited_matrix = numpy.zeros(image.shape)

    def isValidIndice(self, x, y):
        """
        Checks if the pixel (x,y) is addressable
        """
        if y < 0 or y > self._visited_matrix.shape[0]:
            return False

        if x < 0 or x > self._visited_matrix.shape[1]:
            return False

        return True

    def isVisited(self, x, y):
        """
        Checks if the pixel (x,y) was already visited
        """
        if not self.isValidIndice(x, y):
            raise ValueError("Invalid indices x=" + str(x) + ", y=" + str(y))

        return 1 == self._visited_matrix[y,x]

    def setVisited(self, x, y):
        """
        Set the pixel (i,j) as visited
        """
        if not self.isValidIndice(x, y):
            raise ValueError("Invalid indices x=" + str(x) + ", y=" + str(y))
  
        self._visited_matrix[y,x] = 1

    def setRowVisited(self, y, x1, x2):
        """
        Sets the pixels x1 - x2 in row y visited
        """
        if not (self.isValidIndice(x1, y) and self.isValidIndice(x2, y)):
            raise ValueError("Invalid indices")

        if x1 > x2:
            temp = x1
            x1 = x2
            x2 = temp

        for i in range(x1, x2 + 1):
            self.setVisited(i, y)

    def setColumnVisited(self, x, y1, y2):
        """
        Sets the pixels y1 - y2 in column x visited
        """
        if not (self.isValidIndice(x, y1) and self.isValidIndice(x, y2)):
            raise ValueError("Invalid indices")

        if y1 > y2:
            temp = y1
            y1 = y2
            y2 = temp

        for i in range(y1, y2 + 1):
            self.setVisited(x, i)

class LineSegment(object):
    """
    Class representing a detected line segment in the image
    """
    x_start = None
    y_start = None
    x_end = None
    y_end = None

    # true, if the line segment is vertically directed
    _vertical = False

    def __init__(self, x_start, y_start, x_end=None, y_end=None, vertical=None ):
        """
        Constructor
        x_start:
            x coordinate marking the beginning of the line in x direction
        y_start:
            y coordinate marking the beginning of the line in y direction
        """
        self.x_start = int(x_start)
        self.y_start = int(y_start)

        self._vertical = vertical

        if not None == x_end:
            self.x_end = int(x_end)

        if not None == y_end:
            self.y_end = int(y_end)

    def __str__(self):
        return "(" + str(self.x_start) + ", " + str(self.y_start) + ") -- (" + str(self.x_end) + ", " + str(self.y_end) + ")"

    def setVertical(self):
        """
        The property shows that the line segment directs into the fifth or sixth octant, so e.g.,
        
            x
            x
             x
             x
        """
        self._vertical = True

    def swapStartEnd(self):
        """
        Swaps the start and the end points of the line segment
        """
        temp_x = self.x_start
        temp_y = self.y_start
        self.x_start = self.x_end
        self.y_start = self.y_end

        self.x_end = temp_x
        self.y_end = temp_y

    def isPoint(self):
        """
        Returns 'True' if the linesegment is a point otherwise 'False'
        """
        return 0 == (self.x_end - self.x_start) and 0 == (self.y_end - self.y_start)

    def getAsNumpyArray(self):
        """
        Returns the line segment as numpy array of the form
        [x1, y1, x2, y2]
        """
        return numpy.array([int(self.x_start), int(self.y_start), int(self.x_end), int(self.y_end)])

    def getLineLength(self):
        """
        Returns the length of the line
        """
        a = self.getXLength() ** 2
        b = self.getYLength() ** 2

        return math.sqrt(a + b)

    def getXLength(self):
        """
        Returns the length in x direction 
        """
        return int(math.fabs(self.x_end - self.x_start) + 1)

    def getYLength(self):
        """
        Returns the length in y direction 
        """
        return int(math.fabs(self.y_end - self.y_start) + 1)

    def setEndCoordinate(self, x, y):
        self.x_end = x
        self.y_end = y

    def setStartCoordinate(self, x, y):
        self.x_start = x
        self.y_start = y

    def isValidIndice(self, image, x, y):
        """
        Checks if the pixel (x,y) is addressable
        """
        if y < 0 or y >= image.shape[0]:
            return False

        if x < 0 or x >= image.shape[1]:
            return False

        return True

    def isNextPixelBelow(self, image, isLineColor):
        """
        Tests if the current line segment is a
        vertical line segment.
        """
        temp_x = self.x_end
        temp_y = self.y_end + 1

        # check bounds
        if not self.isValidIndice(image, temp_x, temp_y):
            return False

        return isLineColor(image[temp_y, temp_x])

    def isNextPixelRightDown(self, image, isLineColor):
        """
        Tests if the current line segment belongs
        to a line that goes right down through the image.
        """
        temp_x = self.x_end + 1
        temp_y = self.y_end + 1

        # check bounds
        if not self.isValidIndice(image, temp_x, temp_y):
            return False

        return isLineColor(image[temp_y, temp_x])

    def isNextPixelLeftDown(self, image, isLineColor):
        """
        Tests if the current line segment belongs
        to a line that goes left down through the image.
        """
        temp_x = self.x_start - 1
        temp_y = self.y_start + 1

        if self._vertical: 
            temp_x = self.x_end - 1
            temp_y = self.y_end + 1

        # check bounds
        if not self.isValidIndice(image, temp_x, temp_y):
            return False

        return isLineColor(image[temp_y, temp_x])

def findVerticalSegment(image, x, y, isLineColor):
    """
    Travels to the end of the current line segment in positive y direction and returns
    the coordinates.
    """

    if None == image:
        raise ValueError("Image must be set" )

    l = y
    while l < image.shape[0] and isLineColor(image[l,x]):
        l += 1

    return (x, l-1)

def findHorizontalNegativeSegment(image, x, y, isLineColor):
    """
    Travels to the end of the current line segment in negative x direction and returns
    the coordinates.
    """
    if None == image:
        raise ValueError("Image must be set" )

    l = x
    while l >= 0 and isLineColor(image[y,l]):
        l -= 1

    return (l+1, y) 

def findHorizontalPositiveSegment(image, x, y, isLineColor):
    """
    Travels to the end of the current line segment in positive x direction and returns
    the coordinates.
    """

    if None == image:
        raise ValueError("Image must be set" )

    l = x
    while l < image.shape[1] and isLineColor(image[y,l]):
        l += 1

    return (l-1, y) 

def handleFourthOctant(image, lineSegment, visited_matrix, isLineColor):
    """
    Tracks line segments in negative x direction
    """
    length = lineSegment.getXLength()
    max_length = 2*length
    moreSeg = True
    while moreSeg:
        x_temp = lineSegment.x_start - 1
        y_temp = lineSegment.y_start + 1

        if lineSegment.isNextPixelLeftDown(image, isLineColor):
            (x_end, y_end) = findHorizontalNegativeSegment(image, x_temp, y_temp, isLineColor)

        else:
            moreSeg = False

        lengthX = x_temp - x_end + 1
        if lengthX >= length and lengthX <= max_length:
            lineSegment.setStartCoordinate(x_end, y_end)
            visited_matrix.setRowVisited(y_temp, x_temp, x_end)
        else:
            moreSeg = False
        
    return lineSegment

def handleSeventhOctant(image, lineSegment, visited_matrix, isLineColor):
    """
    Tracks line segments in positive x direction
    """
    length = lineSegment.getXLength()
    max_length = 2*length
    moreSeg = True
    while moreSeg:
        x_temp = lineSegment.x_end + 1
        y_temp = lineSegment.y_end + 1

        if lineSegment.isNextPixelRightDown(image, isLineColor):
            (x_end, y_end) = findHorizontalPositiveSegment(image, x_temp, y_temp, isLineColor)
        else:
            moreSeg = False

        lengthX = x_end - x_temp + 1

        if lengthX >= length and lengthX <= max_length:
            lineSegment.setEndCoordinate(x_end, y_end)
            visited_matrix.setRowVisited(y_temp, x_temp, x_end)
        else:
            moreSeg = False

        
    return lineSegment

def handleFourthAndSeventhOctant(image, lineSegment, visited_matrix, isLineColor):
    """
    Handle lines in the fourth and seventh octant.
    ------------------------
              / | \ 
             /  |  \ 
            /   |   \ 
      Oct 4/    |    \ Oct7
           Oct 5|Oct 6

    We do not need to check the octants 1 - 4, because we traverse upside-down from left to right through
    the image.

    Lines of the fourth and seventh octant have the characteristic that line segments are
    x-oriented
        xx
          xx
            xx
              xx

    """
    (x_end, y_end) = findHorizontalPositiveSegment(image, lineSegment.x_start, lineSegment.y_start, isLineColor)
    lineSegment.setEndCoordinate(x_end, y_end)
    visited_matrix.setRowVisited(y_end, lineSegment.x_start, x_end)

    if lineSegment.isNextPixelRightDown(image, isLineColor):
        lineSegment = handleSeventhOctant(image, lineSegment, visited_matrix, isLineColor)
    elif lineSegment.isNextPixelLeftDown(image, isLineColor):
        lineSegment = handleFourthOctant(image, lineSegment, visited_matrix, isLineColor)
        
    return lineSegment

def handleFifthAndSixthOctant(image, lineSegment, visited_matrix, isLineColor):
    """
    Handle lines in the fith and sixth octant.
    ------------------------
              / | \ 
             /  |  \ 
            /   |   \ 
      Oct 4/    |    \ Oct7
           Oct 5|Oct 6

    We do not need to check the octants 1 - 4, because we traverse upside-down from left to right through
    the image.

    Lines of the fith and sixth octant have the characteristic that line segments are
    y-oriented
        x
        x
         x
         x
          x
          x
           x
           x

    """
    (x_end, y_end) = findVerticalSegment(image, lineSegment.x_start, lineSegment.y_start, isLineColor)
    lineSegment.setEndCoordinate(x_end, y_end)
    visited_matrix.setColumnVisited(lineSegment.x_start, lineSegment.y_start, y_end)

    moreSeg = True
    x_temp = lineSegment.x_start

    length = lineSegment.getYLength()
    max_length = 2 * length

    while moreSeg:

        y_temp = lineSegment.y_end + 1

        if lineSegment.isNextPixelLeftDown(image, isLineColor):
            x_temp -= 1
            (x_end, y_end) = findVerticalSegment(image, x_temp, y_temp, isLineColor)
        elif lineSegment.isNextPixelRightDown(image, isLineColor):
            x_temp += 1
            (x_end, y_end) = findVerticalSegment(image, x_temp, y_temp, isLineColor)
        else:
            moreSeg = False

        lengthY = (y_end - y_temp) + 1
        if lengthY >= length and lengthY <= max_length:
            lineSegment.setEndCoordinate(x_end, y_end)
            visited_matrix.setColumnVisited(x_temp, y_temp, y_end)
        else:
            moreSeg = False

    return lineSegment

def _findLines(image, isLineColor=None):
    """
    Detects lines in the given image and returns them as a list
    image:
        Image that contains the lines as numpy array
    isLineColor(_color):
        A function that determines whether a given pixel color value '_color' is part of 
        a line, e.g.:

            mean = image.mean()
            isLineColor(_color):
                return _color > mean

    return:
        list of lines as LineSegment
    """

    if None == image:
        raise ValueError("Image must be set" )

    if None == isLineColor:
        raise ValueError("isLineColor(_color) not set")

    lines = []
    visited_matrix = VisitedMatrix(image)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if isLineColor(image[i,j]) and not visited_matrix.isVisited(j, i):
                lineSegment = LineSegment(j, i, j, i)

                if lineSegment.isNextPixelBelow(image, isLineColor):
                    lineSegment.setVertical()
                    lineSegment = handleFifthAndSixthOctant(image, lineSegment, visited_matrix, isLineColor=isLineColor)
                else:
                    lineSegment = handleFourthAndSeventhOctant(image, lineSegment, visited_matrix, isLineColor=isLineColor)

                lines.append(lineSegment)

    return lines 

def transformLineSegmentsIntoNumpyArray(lines):
    """
    Takes a list of linesegments and transforms them into a list of numpy arrays
    [linesegment1, ...] --> [[x1,y1,x2,y2],...]
    """
    lineparts = []

    for line in lines:
        lineparts.append(line.getAsNumpyArray())

    return lineparts


def findLines(image, isLineColor=None):
    """
    Detects lines in the given image and returns them as a list
    image:
        Image that contains the lines as numpy array
    isLineColor(_color):
        A function that determines whether a given pixel color value 'x' is part of 
        a line, e.g.:

            mean = image.mean()
            isLineColor(_color):
                return _color > mean

    return:
        list of lines as numpy array [x1,y1,x2,y2]
    """
    lines = _findLines(image, isLineColor=isLineColor)

    return transformLineSegmentsIntoNumpyArray(lines)
