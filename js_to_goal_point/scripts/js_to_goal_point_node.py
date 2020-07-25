#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Pose, Twist

#TODO: Learn if this should be its own package

class JsToGoalPoint:
	"""
	Maps joystick controls to a point in 3D
	"""
	def __init__(self, rate, speed = 1e-2, axes = (0, 1, 3)):
		self.rate = rate
		self.speed = speed
		self.axes = axes
		self.pose = Pose()
		self.vel = Twist()

	def handle_event(self, data):
		self.handle_axes(data.axes)
		self.handle_buttons(data.buttons)

	def handle_axes(self, ax):
		vx = self.speed * ax[self.axes[0]]
		vy = self.speed * ax[self.axes[1]]
		vz = self.speed * ax[self.axes[2]]
		self.vel.linear.x = vx
		self.vel.linear.y = vy
		self.vel.linear.z = vz

		rospy.loginfo('VEL = {}'.format(self.vel))

	def handle_buttons(self, bu):
		if sum(bu) > 0:
			self.pose = Pose()
			self.vel = Twist()

	def update(self):
		self.pose.position.x -= self.rate * self.vel.linear.x
		self.pose.position.y += self.rate * self.vel.linear.y
		self.pose.position.z += self.rate * self.vel.linear.z
		

def main():
	freq = 10

	js2goal = JsToGoalPoint(rate = freq)
	sub = rospy.Subscriber('joy', Joy, js2goal.handle_event)
	pub = rospy.Publisher('goal_pose', Pose, queue_size = 1)
	rospy.init_node('js_to_goal_point')

	rate = rospy.Rate(freq)
	while not rospy.is_shutdown():
		js2goal.update()
		pub.publish(js2goal.pose)
		rate.sleep()

if __name__ == '__main__':
	main()
