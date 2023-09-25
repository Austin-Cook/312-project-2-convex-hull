from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
# elif PYQT_VER == 'PYQT4': 							# Commented out so error would go away
# 	from PyQt4.QtCore import QLineF, QPointF, QObject
# elif PYQT_VER == 'PYQT6':
# 	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import sys
from typing import Tuple

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25

# Constants for the program
FAILURE = -1
ABOVE = 1
ON = 0
BELOW = -1


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

	# This is the method that gets called by the GUI and actually executes
	# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert(type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()
		# DONE: SORT THE POINTS BY INCREASING X-VALUE
		sorted_points = sorted(points, key=get_x_value)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = [QLineF(points[i], points[(i + 1) % 3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		# TODO: After calling convex_hull_dc(), set polygon to convert_nodes_to_list(convex_hull_root)
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon, RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))


def get_x_value(point: QPointF) -> float:
	"""
	Retrieves the x value of a PyQt QPointF object\n
	NOTE - used as a key for sorted(unsorted_points)

	:param point: The point from which to retrieve the x-value
	:return: The x value, as a float (double)
	"""
	return point.x()


class PointNode:
	"""
	Represents a point in a convex hull

	clockwise: The following node in clockwise direction
	counter_clockwise: The following node in counter-clockwise direction
	"""
	point = None
	clockwise = None
	counter_clockwise = None

	def __init__(self, point: QPointF):
		self.point = point


def convert_nodes_to_list(point: PointNode) -> list:
	"""
	Returns a list of QPointF objects, given a point in a convex hull

	:param point: A point in a convex hull
	:return: A list of QPointF objects composing the convex hull TODO Response from TA and state if it is clockwise/cc where the list starts in the hull
	"""
	# TODO when the TA responds fill this function in


def convex_hull_dc(sorted_points: list) -> PointNode:
	"""
	A divide and conquer approach to finding a convex hull

	:param sorted_points: A list of QPointF objects from which to find the convex hull, sorted by x-value
	:return: The root node of the resulting convex hull
	"""
	# if size(x) < theta then
	# 	return adhoc(x)
	# decompose x into a subtasks x_1,x_2,...,x_a of size n/b
	# for i = 1 to a do
	# 	y_i <- convex_hull_dc(x_i_
	# y <- combine(left_hull_root, right_hull_root)
	# return y

	a = []
	return a


def find_upper_tangent(left_hull_root: PointNode, right_hull_root: PointNode) -> Tuple[PointNode, PointNode]:
	"""
	Finds the upper tangent of two convex hulls

	:param left_hull_root: The root node of the left convex hull (rightmost Node)
	:param right_hull_root: The root node of the right convex hull (leftmost Node)
	:return: A tuple of PointNode objects of the left and right points of the upper tangent
	"""
	# find rightmost point p in L and leftmost point q in R
	# temp = line(p, q)
	# done = 0
	# while not done do
	# 	done = 1
	# 	while temp is not upper tangent to L do
	# 		r <- p's counterclockwise neighbor
	# 		temp = line(r, q)
	# 		p = r
	# 		done = 0
	# 	while temp is not upper tangent to R do
	# 		r <-q's clockwise neighbor
	# 		temp = line(p, r)
	# 		q = r
	# 		done = 0
	# 	return temp
	# TODO


def find_lower_tangent(left_hull_root: PointNode, right_hull_root: PointNode) -> Tuple[PointNode, PointNode]:
	"""
	Finds the lower tangent of two convex hulls

	:param left_hull_root: The root node of the left convex hull (rightmost point)
	:param right_hull_root: The root node of the right convex hull (leftmost point)
	:return: A tuple of PointNode objects of the left and right points of the lower tangent
	"""
	# find rightmost point p in L and leftmost point q in R
	# temp = line(p, q)
	# done = 0
	# while not done do
	# 	done = 1
	# 	while temp is not lower tangent to L do
	# 		r <- p's clockwise neighbor
	# 		temp = line(r, q)
	# 		p = r
	# 		done = 0
	# 	while temp is not lower tangent to R do
	# 		r <-q's counter-clockwise neighbor
	# 		temp = line(p, r)
	# 		q = r
	# 		done = 0
	# 	return temp
	# TODO


def is_upper_tangent(points: list, tangent_left: QPointF, tangent_right: QPointF) -> bool:
	"""
	Finds if the tangent is above of all points on the list

	:param points: The points to compare against the tangent, as a list of QPointF
	:param tangent_left: The left point of the tangent, as a QPointF
	:param tangent_right: The right point of the tangent, as a QPointF
	:return: Whether the tangent is above all points on the list
	"""
	m = find_slope(tangent_left.point, tangent_right.point)
	b = find_y_intercept(m, tangent_left.point)

	for point in points:
		if above_or_below(m, b, point) == ABOVE:
			return False

	# all points were on or below
	return True


def is_lower_tangent(points: list, tangent_left: QPointF, tangent_right: QPointF) -> bool:
	"""
	Finds if the tangent is below of all points on the list

	:param points: The points to compare against the tangent, as a list of QPointF
	:param tangent_left: The left point of the tangent, as a QPointF
	:param tangent_right: The right point of the tangent, as a QPointF
	:return: Whether the tangent is below all points on the list
	"""
	m = find_slope(tangent_left.point, tangent_right.point)
	b = find_y_intercept(m, tangent_left.point)

	for point in points:
		if above_or_below(m, b, point) == BELOW:
			return False

	# all points were on or above
	return True


def above_or_below(m: float, b: float, point: QPointF) -> int:
	"""
	y_0 >/=/< m(x_0) + b

	:param m: The slope, as a float
	:param b: The y-intercept, as a float
	:param point: The point to compare to the tangent line, as a QPointF
	:return: ABOVE (1), ON (0), or BELOW (-1)
	"""
	y_0 = point.y()
	result = m * point.x() + b
	if y_0 > result:
		return ABOVE
	elif y_0 == result:
		return ON
	elif y_0 < result:
		return BELOW


def find_slope(tangent_left: QPointF, tangent_right: QPointF) -> float:
	"""
	m = (y_2 - Y_1) / (x_2 - x_1)
	
	:param tangent_left: The left point on the tangent, as a QPointF
	:param tangent_right: The right point on the tangent, as a QPointF
	:return: The slope, as a float
	"""
	return (tangent_right.y() - tangent_left.y()) / (tangent_right.x() - tangent_left.x())


def find_y_intercept(m: float, point_on_tangent: QPointF) -> float:
	"""
	b = y_1 - (m * x_1)

	:param m: The slope
	:param point_on_tangent: Either point on the tangent, as a QPointF
	:return: The y-intercept, as a float
	"""
	return point_on_tangent.y() - (m * point_on_tangent.x())

def combine(left_hull_root: PointNode, right_hull_root: PointNode) -> PointNode:
	"""
	Combines two hulls by finding upper and lower tangents and removing nodes
	that are no longer part of the combined hull

	:param left_hull_root: The root PointNode of the hull left hull to combine (rightmost point)
	:param right_hull_root: The root PointNode of the right hull to combine (leftmost point)
	:return: The root PointNode of the combined hull
	"""
	# TODO find upper tangent
	# TODO find lower tangent
	# TODO Create a new hull
		# start at left hull
			# Iterate counter-clockwise through nodes until upper_tangent_left node is found
				# Set its clockwise node to upper_tangent_right node
			# Continue iterate counter-clockwise until lower_tangent_left node is found
				# Set its counter-clockwise node to lower_tangent_right node
			# Iterate counter-clockwise 1 node (to lower_tangent_right node)
				# Set its clockwise node to lower_tangent_left node
			# Continue counter-clockwise until upper_tangent_right_node is found
				# Set its counter-clockwise node to upper-tangent-left-node


def to_leftmost_node(root_node: PointNode) -> PointNode:
	"""
	Rotates through the convex hull to the leftmost node\n
	NOTE - if surrounding nodes have same x, the hull has a size of 1

	:param root_node: A node in the convex hull
	:return: The leftmost node in the same convex hull as root_node
	"""
	curr_node = root_node
	curr_x = root_node.point.x()
	while (curr_node.clockwise is not None) and (curr_node.clockwise.point.x() < curr_x):
		# bottom of the hull - rotate clockwise
		curr_node = curr_node.clockwise
		curr_x = curr_node.point.x()
	while (curr_node.counter_clockwise is not None) and (curr_node.counter_clockwise.point.x() < curr_x):
		# top of the hull - rotate counter-clockwise
		curr_node = curr_node.counter_clockwise
		curr_x = curr_node.point.x()

	return curr_node


def to_rightmost_node(root_node: PointNode) -> PointNode:
	"""
	Rotates through the convex hull to the rightmost node\n
	NOTE - if surrounding nodes have same x, the hull has a size of 1

	:param root_node: A node in the convex hull
	:return: The rightmost node in the same convex hull as root_node
	"""
	curr_node = root_node
	curr_x = root_node.point.x()
	while (curr_node.clockwise is not None) and (curr_node.clockwise.point.x() > curr_x):
		# top of the hull - rotate clockwise
		curr_node = curr_node.clockwise
		curr_x = curr_node.point.x()
	while (curr_node.counter_clockwise is not None) and (curr_node.counter_clockwise.point.x() > curr_x):
		# bottom of the hull - rotate counter-clockwise
		curr_node = curr_node.counter_clockwise
		curr_x = curr_node.point.x()

	return curr_node


def iterate_clockwise(node: PointNode) -> PointNode:
	"""
	Returns the next clockwise PointNode, first checking for None

	:param node: A PointNode in the convex hull
	:return: The PointNode clockwise of node in the convex hull
	"""
	assert node.clockwise is not None
	return node.clockwise


def iterate_counter_clockwise(node: PointNode) -> PointNode:
	"""
	Returns the next counter-clockwise PointNode, first checking for None

	:param node: A PointNode in the convex hull
	:return: The PointNode counter-clockwise of node in the convex hull
	"""
	assert node.counter_clockwise is not None
	return node.counter_clockwise
