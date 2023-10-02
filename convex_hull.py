import random

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
		sorted_points = sorted(points, key=lambda point: point.x())
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		# polygon = [QLineF(points[i], points[(i + 1) % 3]) for i in range(3)]
		convex_hull_node = convex_hull_dc(sorted_points)
		convex_hull_list = convert_nodes_to_list(convex_hull_node)
		polygon = [QLineF(convex_hull_list[i], convex_hull_list[(i + 1) % len(convex_hull_list)]) for i in range(len(convex_hull_list))]
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon, RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))


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


def convert_nodes_to_list(start_node: PointNode) -> list:
	"""
	Returns a list of QPointF objects, given a point in a convex hull

	:param start_node: Any point in a convex hull
	:return: A list of QPointF objects composing the convex hull
	"""
	points = []

	curr_node = start_node
	while True:
		points.append(curr_node.point)

		# increment and check if tried every point
		curr_node = curr_node.clockwise
		if curr_node is start_node:
			break

	return points


def convex_hull_dc(sorted_points_list: list) -> PointNode:
	"""
	A divide and conquer approach to finding a convex hull

	:param sorted_points_list: A list of QPointF objects from which to find the convex hull, sorted by x-value
	:return: The root node of the resulting convex hull
	"""
	# base case - a hull of 1 point
	if len(sorted_points_list) == 1:
		one_node_hull = PointNode(sorted_points_list[0])
		one_node_hull.clockwise = one_node_hull
		one_node_hull.counter_clockwise = one_node_hull
		return one_node_hull

	# divide into two hulls and solve
	middle_index = len(sorted_points_list) // 2
	left_hull = convex_hull_dc(sorted_points_list[0:middle_index])
	right_hull = convex_hull_dc(sorted_points_list[middle_index:len(sorted_points_list)])

	# combine the hulls together
	return combine(left_hull, right_hull)


def find_upper_tangent(left_hull_root: PointNode, right_hull_root: PointNode) -> Tuple[PointNode, PointNode]:
	"""
	Finds the upper tangent of two convex hulls

	:param left_hull_root: The root node of the left convex hull (rightmost Node)
	:param right_hull_root: The root node of the right convex hull (leftmost Node)
	:return: A tuple of PointNode objects of the left and right points of the upper tangent
	"""
	# find rightmost point p in L (left_hull) and leftmost point q in R (right_hull)
	left_node = to_rightmost_node(left_hull_root)
	right_node = to_leftmost_node(right_hull_root)

	# starting line from innermost nodes of the hulls
	curr_line = QLineF(left_node.point, right_node.point)
	curr_slope = (curr_line.y2() - curr_line.y1()) / (curr_line.x2() - curr_line.x1())

	done = 0
	while not done:
		done = 1
		# while temp is not upper tangent to L
		while True:
			# r <- p's counterclockwise neighbor
			new_left = left_node.counter_clockwise

			new_slope = (curr_line.p2().y() - new_left.point.y()) / (curr_line.p2().x() - new_left.point.x())
			if new_slope < curr_slope:
				# new slope is closer to being the tangent
				# temp = line(r, q)
				curr_line.setP1(new_left.point)
				# p = r
				left_node = new_left
				curr_slope = new_slope
				done = 0
			else:
				break
		# while temp is not upper tangent to R do
		while True:
			# r <-q's clockwise neighbor
			new_right = right_node.clockwise

			new_slope = (new_right.point.y() - curr_line.p1().y()) / (new_right.point.x() - curr_line.p1().x())
			if new_slope > curr_slope:
				# new_slope is closer to being the tangent
				# temp = line(p, r)
				curr_line.setP2(new_right.point)
				# q = r
				right_node = new_right
				curr_slope = new_slope
				done = 0
			else:
				break
	return left_node, right_node


def find_lower_tangent(left_hull_root: PointNode, right_hull_root: PointNode) -> Tuple[PointNode, PointNode]:
	"""
	Finds the lower tangent of two convex hulls

	:param left_hull_root: The root node of the left convex hull (rightmost point)
	:param right_hull_root: The root node of the right convex hull (leftmost point)
	:return: A tuple of PointNode objects of the left and right points of the lower tangent
	"""
	# find rightmost point p in L and leftmost point q in R
	left_node = to_rightmost_node(left_hull_root)
	right_node = to_leftmost_node(right_hull_root)

	# starting line from innermost nodes of the hulls
	curr_line = QLineF(left_node.point, right_node.point)
	curr_slope = (curr_line.y2() - curr_line.y1()) / (curr_line.x2() - curr_line.x1())

	done = 0
	while not done:
		done = 1
		# while temp is not lower tangent to L do
		while True:
			# r <- p's clockwise neighbor
			new_left = left_node.clockwise

			new_slope = (curr_line.p2().y() - new_left.point.y()) / (curr_line.p2().x() - new_left.point.x())
			if new_slope > curr_slope:
				# new_slope is closer to being the tangent
				# temp = line(r, q)
				curr_line.setP1(new_left.point)
				# p = r
				left_node = new_left
				curr_slope = new_slope
				done = 0
			else:
				break
		# while temp is not lower tangent to R do
		while True:
			# r <-q's counter-clockwise neighbor
			new_right = right_node.counter_clockwise

			new_slope = (new_right.point.y() - curr_line.p1().y()) / (new_right.point.x() - curr_line.p1().x())
			if new_slope < curr_slope:
				# new_slope is closer to being the tangent
				# temp = line(p, r)
				curr_line.setP2(new_right.point)
				# q = r
				right_node = new_right
				curr_slope = new_slope
				done = 0
			else:
				break
	return left_node, right_node


# def is_upper_tangent(point_in_hull: PointNode, tangent_left: QPointF, tangent_right: QPointF) -> bool:
# 	"""
# 	Finds if the tangent is above of all points on the list
#
# 	:param point_in_hull: Any point of the hull which will be compared to tangent line, as a PointNode
# 	:param tangent_left: The left point of the tangent, as a QPointF
# 	:param tangent_right: The right point of the tangent, as a QPointF
# 	:return: Whether the tangent is above all points on the list
# 	"""
# 	m = find_slope(tangent_left, tangent_right)
# 	b = find_y_intercept(m, tangent_left)
#
# 	# check if each point in the hull is below the tangent
# 	curr_point = point_in_hull
# 	while True:
# 		if above_or_below(m, b, curr_point.point) == ABOVE:
# 			# not an upper tangent for at least this point
# 			return False
#
# 		# increment and check if tried every point
# 		curr_point = curr_point.clockwise
# 		if curr_point is point_in_hull:
# 			break
#
# 	# all points were on or below
# 	return True
#
#
# def is_lower_tangent(point_in_hull: PointNode, tangent_left: QPointF, tangent_right: QPointF) -> bool:
# 	"""
# 	Finds if the tangent is below of all points on the list
#
# 	:param point_in_hull: Any point of the hull which will be compared to tangent line, as a PointNode
# 	:param tangent_left: The left point of the tangent, as a QPointF
# 	:param tangent_right: The right point of the tangent, as a QPointF
# 	:return: Whether the tangent is below all points on the list
# 	"""
#
# 	m = find_slope(tangent_left, tangent_right)
# 	b = find_y_intercept(m, tangent_left)
#
# 	# check if each point in the hull is above the tangent
# 	curr_point = point_in_hull
# 	while True:
# 		if above_or_below(m, b, curr_point.point) == BELOW:
# 			# not a lower tangent for at least this point
# 			return False
#
# 		# increment and check if tried every point
# 		curr_point = curr_point.clockwise
# 		if curr_point is point_in_hull:
# 			break
#
# 	# all points were on or above
# 	return True
#
#
# def above_or_below(m: float, b: float, point: QPointF) -> int:
# 	"""
# 	y_0 >/=/< m(x_0) + b
#
# 	:param m: The slope, as a float
# 	:param b: The y-intercept, as a float
# 	:param point: The point to compare to the tangent line, as a QPointF
# 	:return: ABOVE (1), ON (0), or BELOW (-1)
# 	"""
# 	y_0 = point.y()
# 	result = m * point.x() + b
# 	# print(f"y_0: {y_0}, result: {result}")
# 	if abs(y_0 - result) < 0.0000001: # 0.0000000001
# 		# print("   ON")
# 		return ON
# 	elif y_0 > result:
# 		# print("   ABOVE")
# 		return ABOVE
# 	elif y_0 < result:
# 		# print("   BELOW")
# 		return BELOW


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
	# find tangents
	upper_left, upper_right = find_upper_tangent(left_hull_root, right_hull_root)
	lower_left, lower_right = find_lower_tangent(left_hull_root, right_hull_root)

	# create a new hull
	upper_left.clockwise = upper_right
	upper_right.counter_clockwise = upper_left
	lower_left.counter_clockwise = lower_right
	lower_right.clockwise = lower_left

	return upper_left


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


if __name__ == "__main__":
	# sorted_points = [QPointF(1.0, 1.0), QPointF(2.0, 2.0), QPointF(3.0, 1.0), QPointF(5, 3)]
	# sorted_points = [QPointF(1.000001, 2.000001), QPointF(2.000001, 3.000001), QPointF(2.500004, 2.000001), QPointF(3.000005, 1.000001), QPointF(3.500005, 3.000001), QPointF(4.00002, 4.000001), QPointF(5.002, 2.000001), QPointF(6.0005, 3.000001)]
	# sorted_points = [QPointF(-0.8346014684451692, 0.11172643811141669), QPointF(-0.8040451631412548,-0.2748520657076059), QPointF(-0.1248416717398606, -0.3760631777812582), QPointF(0.03115216321399039, 0.9751813280210595), QPointF(0.4523649013590423, 0.1558272297975385)]
	# sorted_points = [QPointF(-0.6726141353934931, -0.021656509885807473), QPointF(-0.3588946762474199, -0.48025045570101055), QPointF(-0.20384115482678244, -0.3015934861352687), QPointF(0.20213023654773443, -0.09789206232693326)]
	sorted_points = []
	for i in range(100000):
		sorted_points.append(QPointF(i, random.randrange(300)))
	print("done generating")
	print(len(sorted_points))
	t1 = time.time()
	node = convex_hull_dc(sorted_points)
	t2 = time.time()
	print("done finding convex_hull: time: ", str(t2 - t1))
	hull_points = convert_nodes_to_list(node)
	print(hull_points)

