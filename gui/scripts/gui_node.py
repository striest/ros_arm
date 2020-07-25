#! /usr/bin/env/ python

import rospy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from gui.gui import GUI
from geometry_msgs.msg import Pose, PoseArray


def main():
	gui = GUI(draw_orientation = False)
	rospy.init_node('gui_node')
	goal_sub = rospy.Subscriber('goal_pose', Pose, gui.handle_goal)
	arm_pose_sub = rospy.Subscriber('arm/link_poses', PoseArray, gui.handle_link_poses)
	rate = rospy.Rate(5)

	for i in range(5):
		rate.sleep()

	while not rospy.is_shutdown():
		gui.redraw()
		rate.sleep()	

if __name__ == '__main__':
	main()
