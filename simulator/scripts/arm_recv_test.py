import rospy

from simulator.arm import Arm
from simulator.msg import Arm_msg

def callback(msg):
	a = Arm(msg)
	print(a.get_link_poses())
	rospy.loginfo('recieved:\n{}'.format(a))

def main():
	rospy.init_node('arm_recv')
	arm_sub = rospy.Subscriber('arm/arm_spec', Arm_msg, callback)
	rospy.spin()

if __name__ == '__main__':
	main()
