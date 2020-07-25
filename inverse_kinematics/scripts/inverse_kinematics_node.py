import rospy
import numpy as np

from simulator.msg import PositionControl, Arm_msg
from geometry_msgs.msg import Pose

from inverse_kinematics.inverse_kinematics import PositionInverseKinematicsSolver

def main():
	rospy.init_node('inverse_kinematics_node')
	ik_solver = PositionInverseKinematicsSolver(lr=1e-1)
	arm_spec_sub = rospy.Subscriber('arm/arm_spec', Arm_msg, ik_solver.update_arm)
	goal_sub = rospy.Subscriber('goal_pose', Pose, ik_solver.update_goal)
	control_sub = rospy.Subscriber('arm/control', PositionControl, ik_solver.update_controls)
	control_pub = rospy.Publisher('arm/control', PositionControl, queue_size = 1)

	rate = rospy.Rate(50)

	for i in range(100):
		rate.sleep()

	while not rospy.is_shutdown():
		rospy.loginfo(ik_solver.numeric_jacobian())

		u = ik_solver.step()
		rospy.loginfo(u)
		control_pub.publish(u)

		rate.sleep()

if __name__ == '__main__':
	main()
