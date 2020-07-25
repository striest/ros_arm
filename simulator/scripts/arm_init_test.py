import rospy
from numpy import pi
from simulator.msg import Link_msg, Arm_msg

def main():
	a = Arm_msg()
	l1 = Link_msg(link_type = 'revolute', a = 0, alpha = 0, d = 2, theta = 0)
	l2 = Link_msg(link_type = 'fixed', a = 0, alpha = -pi/2, d = 0, theta = 0)
	l3 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l4 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l5 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l6 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l7 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l8 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l9 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l10 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l11 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l12 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l13 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	l14 = Link_msg(link_type = 'revolute', a = 1, alpha = 0, d = 0, theta = 0)
	a.links = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14]

	rospy.init_node('arm_spec_test')
	arm_spec_pub = rospy.Publisher('arm/arm_spec', Arm_msg, queue_size = 1)

	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		arm_spec_pub.publish(a)
		rate.sleep()

if __name__ == '__main__':
	main()
