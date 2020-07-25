import rospy

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt4agg')
from mpl_toolkits.mplot3d import Axes3D

from geometry_msgs.msg import Pose, PoseArray

class GUI:
	"""
	GUI class for robot arm. Draws arm and goal point in 3D in real time
	"""
	def __init__(self, window = {'x':(-5, 5), 'y':(-5, 5), 'z':(-5, 5)}, figsize = (6, 6), draw_orientation = False):
		self.window = window
		self.goal = Pose()
		self.arm_poses = []

		self.draw_orientation = draw_orientation

		self.fig = plt.figure(figsize = figsize)
		self.ax = self.fig.add_subplot(111, projection='3d')

		plt.show(block = False)
		self.redraw()

	def handle_goal(self, data):
		self.goal = data

	def handle_link_poses(self, msg):
		self.arm_poses = msg.poses

	def draw_goal(self):
		self.ax.scatter(self.goal.position.x, self.goal.position.y, self.goal.position.z, c='g', marker='x', label = 'Goal: x={:.2f}, y={:.2f}, z={:.2f}'.format(self.goal.position.x, self.goal.position.y, self.goal.position.z))

	def draw_arm(self):
		xs = [pose.position.x for pose in self.arm_poses]
		ys = [pose.position.y for pose in self.arm_poses]
		zs = [pose.position.z for pose in self.arm_poses]
		
		if len(xs) < 1:
			return

		if self.draw_orientation:
			for pose in self.arm_poses:
				self.draw_orientations(pose)

		self.ax.plot(xs, ys, zs, color='k')

		self.ax.scatter(xs[-1], ys[-1], zs[-1], c='r', marker='x', label = 'EE: x={:.2f}, y={:.2f}, z={:.2f}'.format(xs[-1], ys[-1], zs[-1]))
		self.ax.scatter(xs[0], ys[0], zs[0], c='r', marker='.', label = 'Origin: x={:.2f}, y={:.2f}, z={:.2f}'.format(xs[0], ys[0], zs[0]))

	def draw_orientations(self, pose, scale=1.0):
		"""
		draws the coordinate frame for a pose
		"""
		x_o = pose.position.x
		y_o = pose.position.y
		z_o = pose.position.z
		qw = pose.orientation.w
		qx = pose.orientation.x
		qy = pose.orientation.y
		qz = pose.orientation.z
		vx = [2*(qw*qw+qx*qx)-1, 2*(qx*qy+qw*qz), 2*(qx*qz-qw*qy)]
		vy = [2*(qx*qy-qw*qz), 2*(qw*qw+qy*qy)-1, 2*(qy*qz+qw*qx)]
		vz = [2*(qx*qz+qw*qy), 2*(qy*qz-qw*qx), 2*(qw*qw+qz*qz)-1]

		self.ax.quiver(x_o, y_o, z_o, scale*vx[0], scale*vx[1], scale*vx[2], color='r')
		self.ax.quiver(x_o, y_o, z_o, scale*vy[0], scale*vy[1], scale*vy[2], color='g')
		self.ax.quiver(x_o, y_o, z_o, scale*vz[0], scale*vz[1], scale*vz[2], color='b')
		

	def redraw(self):
		self.ax.clear()
		self.ax.set_title('Arm GUI')
		self.ax.legend()
		self.ax.set_xlim(self.window['x'])
		self.ax.set_ylim(self.window['y'])
		self.ax.set_zlim(self.window['z'])
		self.ax.set_xlabel('X')
		self.ax.set_ylabel('Y')
		self.ax.set_zlabel('Z')

		self.draw_goal()
		self.draw_arm()
		
		self.ax.legend()
		self.fig.canvas.draw()
		plt.pause(1e-2)
