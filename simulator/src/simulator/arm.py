import rospy
import numpy as np

from simulator.link import *
from simulator.util import HTM_to_pose
from geometry_msgs.msg import Pose, PoseArray

class Arm:
	"""
	Arm class for forward kinematics
	"""
	def __init__(self, msg):
		links = [link_from_msg(l) for l in msg.links]
		self.links = []
		self.control_links = []
		for link in links:
			self.links.append(link)
			if isinstance(link, (PrismaticLink, RevoluteLink)):
				self.control_links.append(link)

	def get_controls(self):
		controls = []
		for link in self.control_links:
			if isinstance(link, PrismaticLink):
				controls.append(link.d)
			elif isinstance(link, RevoluteLink):
				controls.append(link.theta)

		return controls

	def control_dim(self):
		return len(self.control_links)

	def update_controls(self, controls):
		assert len(controls) == len(self.control_links), 'Expected {}-d control signal, got {}'.format(len(self.control_links), len(controls))
		for link, val in zip(self.control_links, controls):
			link.actuate(val)

	def get_link_poses(self):
		htms = [np.eye(4)]
		for link in self.links:
			htms.append(np.dot(htms[-1], link.htm()))

		poses = [HTM_to_pose(htm) for htm in htms]
		return poses
		
	def get_ee_pose(self):
		ee_pose = self.get_link_poses()[-1]
		return ee_pose


	def __repr__(self):
		out = 'ARM:\n'
		for i, link in enumerate(self.links):
			out += '\t LINK {}: {}\n'.format(i+1, link.__repr__())
		return out
