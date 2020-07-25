import rospy
from numpy import pi

from simulator.arm import Arm
from simulator.msg import Arm_msg, PositionControl

def main():
	n_controls = 2

	rospy.init_node('simulator_rotate_node')
	control_pub = rospy.Publisher('arm/control', PositionControl, queue_size=1)
	rate = rospy.Rate(10)
	for i in range(20):
		rate.sleep()

	cnt = 0
	while not rospy.is_shutdown():
		val = (2*pi*(cnt/100)) % (2*pi)
		controls = [val] * n_controls
		msg = PositionControl(controls=controls)
		rospy.loginfo(msg)
		control_pub.publish(msg)
		cnt += 1
		rate.sleep()

if __name__ == '__main__':
	main()		
