import numpy as np

def position_error(p1, p2):
	"""
	Returns the position difference of two Pose messages as a 3x1 numpy array
	"""
	return np.array([p1.position.x - p2.position.x, p1.position.y - p2.position.y, p1.position.z - p2.position.z]).T

def pose_to_np(p):
	"""
	Constructs a 3x1 numpy array from the position of a Pose message
	"""
	return np.array([p.position.x, p.position.y, p.position.z]).T

def pseudo_inverse(J):
	"""
	Take the pseudo-inverse of the matrix
	J_inv = ((J_T*J)^-1) * J_T
	"""
	return np.dot(np.linalg.inv(np.dot(J.T, J)), J.T)
