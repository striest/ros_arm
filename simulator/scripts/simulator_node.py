#! /usr/bin/env/ python
import rospy
from simulator.simulator import Simulator

from geometry_msgs.msg import PoseArray, Pose
from simulator.msg import Arm_msg, PositionControl

def main():
	rospy.init_node('simulator')
	simulator = Simulator()
	
	arm_spec_sub = rospy.Subscriber('arm/arm_spec', Arm_msg, simulator.handle_arm_spec)
	arm_control_sub = rospy.Subscriber('arm/control', PositionControl, simulator.handle_arm_control)
	joint_poses_pub = rospy.Publisher('arm/link_poses', PoseArray, queue_size=1)
	ee_pose_pub = rospy.Publisher('arm/ee_pose', Pose, queue_size=1)

	rate = rospy.Rate(10)
	for i in range(20):
		rate.sleep()

	while not rospy.is_shutdown():
		joint_poses_pub.publish(simulator.link_poses_msg())
		ee_pose_pub.publish(simulator.ee_pose_msg())
		rate.sleep()

if __name__ == '__main__':
	main()
