"""
Post processing functionalities:
	- group lines that are connected
	- join lines that have equal slope

# Filename: postProcessing.py
# Author: Thomas Osterland
# Date created: 10/30/2015
# Python version: 2.7
"""
import math
from lineFinding import LineSegment

class Structure(object):
	"""
	A structure is a set of connected lines.
	"""
	_lines = []

	def __init__(self):
		self._lines = []

	def __iter__(self):
		"""
		Overload iteration
		"""
		return self._lines.__iter__()

	def __len__(self):
		"""
		Overload len(...)
		"""
		return len(self._lines)

	def __getitem__(self, key):
		"""
		Overload structure[...]
		"""
		return self._lines[key]

	def __setitem__(self, key, value):
		"""
		Overload structure[...] = x
		"""
		if not isinstance(value, LineSegment):
			raise ValueError("A structure can only hold elements of type 'LineSegment'")

		self._lines[key] = value

	def __contains__(self, item):
		"""
		Overload contains
		"""
		return item in self._lines

	def __str__(self):
		"""
		Overload str(...)
		"""
		temp = "["
		for line in self._lines:
			temp += str(line) + ","

		if len(self._lines) > 0:
# remove successing ','
			temp = temp[0:len(temp) - 1]

		return temp + "]"

	def append(self, line):
		"""
		Append a line to the structure
		"""
		if not isinstance(line, LineSegment):
			raise ValueError("A structure can only hold elements of type 'LineSegment'")

		self._lines.append(line)

	def remove(self, line):
		"""
		Removes a line from the structure
		"""
		if not isinstance(line, LineSegment):
			raise ValueError("A structure can only hold elements of type 'LineSegment'")

		self._lines.remove(line)

	def transformIntoNumpyArray(self):
		"""
		Takes a list of linesegments and transforms them into a list of numpy arrays
		[linesegment1, ...] --> [[x1,y1,x2,y2],...]
		"""
		lines = []
		for line in self._lines:
			lines.append(line.getAsNumpyArray())

		return lines

def getAdjacentCoordinates(x, y, delta=1):
	"""
	Returns the coordinates of the points in the
	delta- neigbourhood around (x,y) (including x,y).
	"""
	if not isinstance(x, int) or not isinstance(y, int):
		raise ValueError("x, y must be of type 'int'")

	points = []

	for i in range(x-delta, x+delta+1):
		for j in range(y-delta, y+delta+1):
			points.append([i,j])

	return points

def isAdjacentPoint(x_1, y_1, x_2, y_2, delta=1):
	"""
	Checks if the coordinates (x_1, y_1) and
	(x_2, y_2) are adjacent within a delta- neighbourhood
	of (x_1, y_1)
	delta:
		size of the neigbourhood in pixels
	"""
	if not isinstance(x_1, int) or not isinstance(y_1, int) or not isinstance(x_2, int) or not isinstance(y_2, int):
		raise ValueError("x_1, y_1, x_2, y_2 must be of type 'int'")

	points = getAdjacentCoordinates(x_1, y_1, delta=delta)

	return [x_2, y_2] in points

def isAdjacentToEnd(line_1, line_2, delta=1):
	"""
	Checks if line_2 is adjacent to the end point
	of line_1.
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	if not isinstance(line_1, LineSegment) or not isinstance(line_2, LineSegment):
		raise ValueError("line_1, line_2 must be of type 'linefinding.LineSegment'")

	return isAdjacentPoint(line_1.x_end, line_1.y_end, line_2.x_start, line_2.y_start, delta=delta) or isAdjacentPoint(line_1.x_end, line_1.y_end, line_2.x_end, line_2.y_end, delta=delta)

def isAdjacentToStart(line_1, line_2, delta=1):
	"""
	Checks if line_2 is adjacent to the start point 
	of line_1.
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	if not isinstance(line_1, LineSegment) or not isinstance(line_2, LineSegment):
		raise ValueError("line_1, line_2 must be of type 'linefinding.LineSegment'")

	return isAdjacentPoint(line_1.x_start, line_1.y_start, line_2.x_start, line_2.y_start, delta=delta) or isAdjacentPoint(line_1.x_start, line_1.y_start, line_2.x_end, line_2.y_end, delta=delta)

def isAdjacent(line_1 , line_2, delta=1):
	"""
	Checks if two lines are adjacent.
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	if not isinstance(line_1, LineSegment) or not isinstance(line_2, LineSegment):
		raise ValueError("line_1, line_2 must be of type 'linefinding.LineSegment'")

	return isAdjacentToStart(line_1, line_2, delta=delta) or isAdjacentToEnd(line_1, line_2, delta=delta)

def collectAdjacentLines(currentLine, lines, structure, visitedLines, delta=1):
	"""
	Runs recursively (DFS) through the lines and finds connected lines
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""

	if not isinstance(structure, Structure):
		raise ValueError("'structure' must be of type 'postProcessing.Structure'")

	for line in lines:
		if line in structure or line in visitedLines:
			continue

		if isAdjacent(currentLine, line, delta=delta):
			structure.append(line)
			visitedLines.append(line)
			collectAdjacentLines(line, lines, structure, visitedLines, delta=delta)

def groupAdjacentLines(lines, delta=1):
	"""
	Returns a list of structures that contain lines that are connected.
	lines:
		Set of lines
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	return:
		A set of stuctures. Every structure hold lines that are connected to each other.
		That means you can always find a path from one line to every other by traversing 
		through the graph.
	"""

	structures = []
	visitedLines = []

	for line_1 in lines:

		if line_1 in visitedLines:
			continue

		structure = Structure()
		structure.append(line_1)
		visitedLines.append(line_1)
		collectAdjacentLines(line_1, lines, structure, visitedLines, delta=delta)
		structures.append(structure)


	return structures 

def computeSlope(line):
	"""
	Computes and returns the slope of a line
	"""
	if not isinstance(line, LineSegment): 
		raise ValueError("line must be of type 'linefinding.LineSegment'")

	# slope of a point is not defined
	if line.isPoint():
		return None

	delta_y = float(line.y_end - line.y_start)
	delta_x = float(line.x_end - line.x_start)

	if 0 == delta_y:
		return 0

	if 0 == delta_x:
		return None

	return delta_y / delta_x

def computeAngle(line_1, line_2):
	"""
	Computes the angle between two lines
	"""
	a_1 = line_1.x_start - line_1.x_end
	a_2 = line_1.y_start - line_1.y_end

	b_1 = line_2.x_start - line_2.x_end
	b_2 = line_2.y_start - line_2.y_end

	ab = a_1 * b_1 + a_2 * b_2

	if 0 == ab:
		return 90

	a_ = math.sqrt(a_1**2 + a_2**2)
	b_ = math.sqrt(b_1**2 + b_2**2)
	
	a_b_ = a_*b_

	r = float(ab) / a_b_

	#TODO !!! dangerous round to 5 digits
	acos = math.acos(round(r, 5))

	return math.degrees(acos)


def haveEqualSlope(line_1, line_2, angle_epsilon=None):
	"""
	Tests if two lines have equal (or similar) slope
	- angle_epsilon:
		Two lines will be joined if the angle is 180dg (+/- angle_epsilon)
	"""
	if not isinstance(line_1, LineSegment) or not isinstance(line_2, LineSegment):
		raise ValueError("line_1, line_2 must be of type 'linefinding.LineSegment'")

	if not None == angle_epsilon:
		angle = computeAngle(line_1, line_2)
		return -1 * angle_epsilon <= angle and angle <= angle_epsilon
	else:
		raise ValueError("angle_epsilon not set")

def combineLines(line_1, line_2, angle_epsilon=None, delta=1):
	"""
	Returns the combined line if a combination is possible. A combination is possible
	if the slope differs not too much and that is the case if the angles between the
	lines are not too different.
	It returns None if no such combination is possible.
	- angle_epsilon:
		Two lines will be joined if the angle is 180dg (+/- angle_epsilon)
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	if not isinstance(line_1, LineSegment) or not isinstance(line_2, LineSegment):
		raise ValueError("line_1, line_2 must be of type 'linefinding.LineSegment'")

	if not line_1.isPoint() and not line_2.isPoint() and not haveEqualSlope(line_1, line_2, angle_epsilon=angle_epsilon):
		return None

	if line_1.isPoint():

		if isAdjacentToStart(line_2, line_1, delta):
			line_1.setEndCoordinate(line_2.x_end, line_2.y_end)
			return line_1
		elif isAdjacentToEnd(line_2, line_1, delta):
			line_2.setEndCoordinate(line_1.x_end, line_1.y_end)
			return line_2
		else:
			return None

	elif line_2.isPoint():

		if isAdjacentToStart(line_1, line_2, delta):
			line_2.setEndCoordinate(line_1.x_end, line_1.y_end)
			return line_2
		elif isAdjacentToEnd(line_1, line_2, delta):
			line_1.setEndCoordinate(line_2.x_end, line_2.y_end)
			return line_1
		else:
			return None

	elif isAdjacentToStart(line_1, line_2, delta):

		line_2.setEndCoordinate(line_1.x_end, line_1.y_end)
		return line_2

	elif isAdjacentToEnd(line_1, line_2, delta):
		
		line_1.setEndCoordinate(line_2.x_end, line_2.y_end)
		return line_1

	else:
		return None

def combineLinesWithEqualSlope_Rec(i, structure, angle_epsilon=None, delta=1):
	"""
	Runs recursively through the set of adjacent lines (structures) and combines
	lines if possible.
	- angle_epsilon:
		Two lines will be joined if the angle is 180dg (+/- angle_epsilon)
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	if len(structure) > i:
		line_1 = structure[i]
		for j in range(i+1, len(structure)):
			line_2 = structure[j]

			combinedLine = combineLines(line_1, line_2, angle_epsilon=angle_epsilon, delta=delta)

			if not None == combinedLine:
				structure[i] = combinedLine
				structure.remove(line_2)
				combineLinesWithEqualSlope_Rec(i, structure, angle_epsilon=angle_epsilon, delta=delta)
				return

		combineLinesWithEqualSlope_Rec(i+1, structure, angle_epsilon=angle_epsilon, delta=delta)


def combineLinesWithEqualSlope(structures, angle_epsilon=None, delta=1):
	"""
	Combines lines that have equal or similar slope. Thus reduces the amount of lines
	in a structure for the price of reducing the detailedness.
	- angle_epsilon:
		Two lines will be joined if the angle is 180dg (+/- angle_epsilon)
	delta: 
		Range of the neighbour in which we consider a line as adjacent
	"""
	processedStructures = []

	for structure in structures:
		combineLinesWithEqualSlope_Rec(0, structure, angle_epsilon=angle_epsilon, delta=delta)
		processedStructures.append(structure)

	return processedStructures
