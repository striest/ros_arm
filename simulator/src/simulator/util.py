"""
Collection of util functions (mostly moving between DH, HTM, quaternion)
"""
import numpy as np

from geometry_msgs.msg import Pose

def HTM_to_pose(htm):
	"""
	Constructs a Pose message from an HTM (as a numpy matrix)
	"""
	pose_out = Pose()
	pose_out.position.x = htm[0, 3]	
	pose_out.position.y = htm[1, 3]	
	pose_out.position.z = htm[2, 3]	
	pose_out.orientation.w = 0.5 * np.sqrt(htm[0, 0] + htm[1, 1] + htm[2, 2] + 1)
	pose_out.orientation.x = 0.5 * np.sign(htm[2, 1] - htm[1, 2]) * np.sqrt(htm[0, 0] - (htm[1, 1] + htm[2, 2]) + 1)
	pose_out.orientation.y = 0.5 * np.sign(htm[0, 2] - htm[2, 0]) * np.sqrt(htm[1, 1] - (htm[0, 0] + htm[2, 2]) + 1)
	pose_out.orientation.z = 0.5 * np.sign(htm[1, 0] - htm[0, 1]) * np.sqrt(htm[2, 2] - (htm[1, 1] + htm[0, 0]) + 1)
	return pose_out
