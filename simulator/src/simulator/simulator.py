import rospy

from simulator.arm import Arm

from geometry_msgs.msg import Pose, PoseArray

class Simulator:
	"""
	Class that handles all the ROS wiring for the simulator
	Recieves: Arm_spec, joint angles
	Outputs: joint poses, ee_pose
	"""
	def __init__(self):
		self.arm = None

	def handle_arm_spec(self, msg):
		if self.arm is None:
			self.arm = Arm(msg)

	def handle_arm_control(self, msg):
		self.arm.update_controls(msg.controls)

	def link_poses_msg(self):
		poses = self.arm.get_link_poses()
		out = PoseArray()
		out.poses = poses
		return out

	def ee_pose_msg(self):
		return self.arm.get_ee_pose()
