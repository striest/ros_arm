import rospy
import numpy as np

from simulator.msg import Link_msg

class BaseLink:
	"""
	Class for parameterizing links in an arm. Handles prismatic/revolute joints via DH params and computes the link's homogeneous transform matrix
	"""
	def __init__(self, a, alpha, d, theta):
		self.a = a
		self.alpha = alpha
		self.d = d
		self.theta = theta

	def htm(self):
		"""
		Induces the HTM for this link (i.e. T(i-1, i)).
		"""
		htm = np.zeros((4, 4))
		htm[0, 0] = np.cos(self.theta)
		htm[0, 1] = -np.sin(self.theta) * np.cos(self.alpha)
		htm[0, 2] = np.sin(self.theta) * np.sin(self.alpha)
		htm[0, 3] = self.a * np.cos(self.theta)
		htm[1, 0] = np.sin(self.theta)
		htm[1, 1] = np.cos(self.theta) * np.cos(self.alpha)
		htm[1, 2] = -np.cos(self.theta) * np.sin(self.alpha)
		htm[1, 3] = self.a * np.sin(self.theta)
		htm[2, 1] = np.sin(self.alpha)
		htm[2, 2] = np.cos(self.alpha)
		htm[2, 3] = self.d
		htm[3, 3] = 1

		return htm

	def __repr__(self):
		return "a = {}, alpha = {}, d = {}, theta = {}".format(self.a, self.alpha, self.d, self.theta)

class RevoluteLink(BaseLink):
	"""
	Class for handling revolute joints (can adjust theta)
	"""
	def actuate(self, theta):
		self.theta = theta

class PrismaticLink(BaseLink):
	"""
	Class fotr handling prismatic joints (can adjust d)
	"""
	def actuate(self, d):
		self.d = d

def link_from_msg(msg):
	"""
	Construct the correct Link class from Link.msg
	"""
	if msg.link_type == 'fixed':
		return BaseLink(msg.a, msg.alpha, msg.d, msg.theta)
	elif msg.link_type == 'prismatic':
		return PrismaticLink(msg.a, msg.alpha, msg.d, msg.theta)
	elif msg.link_type == 'revolute':
		return RevoluteLink(msg.a, msg.alpha, msg.d, msg.theta)
	else:
		rospy.loginfo('Invalid link type')
