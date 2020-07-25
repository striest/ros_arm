import rospy

import numpy as np

from simulator.arm import Arm
from simulator.msg import PositionControl

from inverse_kinematics.util import position_error, pose_to_np, pseudo_inverse

class PositionInverseKinematicsSolver:
	"""
	Use inverse kinematics to move arm to a goal point.
	Note that the IK solver should basically just output new controls for the current state and let the other classes actually move the arm.
	"""
	def __init__(self, du = 0.01, dt_max = 0.01, lr=1e-2):
		self.arm = None
		self.goal = None
		self.du = du
		self.dt_max = dt_max
		self.lr = lr

	def update_arm(self, arm_msg):
		"""
		Note that you can only update the arm spec ONCE (controls as much as necessary though)
		"""
		if self.arm is None:
			self.arm = Arm(arm_msg)

	def update_goal(self, goal_msg):
		self.goal = goal_msg

	def update_controls(self, control_msg):
		self.arm.update_controls(control_msg.controls)

	def numeric_jacobian(self):
		"""
		Compute the numeric jacobian of the arm in its current configuration
		"""		
		base_pos = pose_to_np(self.arm.get_ee_pose())
		u = self.arm.get_controls()
		J_rows = []
		
		for i in range(self.arm.control_dim()):
			u[i] += self.du
			self.arm.update_controls(u)
			new_pos = pose_to_np(self.arm.get_ee_pose())
			J_rows.append((new_pos - base_pos) / self.du)

			#Reset the arm back
			u[i] -= self.du
			self.arm.update_controls(u)

		return np.stack(J_rows, axis=0)

	
	def step(self):
		"""
		Perform a step of inverse kinematics and return the updated control signal.
		J = de/dt
		de = J*dt
		dt = J_inv*de
		"""
		ji = pseudo_inverse(self.numeric_jacobian())
		de = position_error(self.goal, self.arm.get_ee_pose())
		dt = self.lr * np.dot(de, ji)

		scale = np.max(np.abs(dt) / self.dt_max)
		if scale > 1:
			dt /= scale

		rospy.loginfo('Dist to goal = {}'.format((de**2).sum() ** 0.5))

		c_new = [d + u for d, u in zip(self.arm.get_controls(), dt)]
		return PositionControl(controls = c_new)







