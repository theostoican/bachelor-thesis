import numpy as np
from numpy.linalg import inv


class KalmanFilter:
	def __init__(self):
		# This is the interval between predictions
		dt = 1

		#Initialize state and covariance matrix
		self.x = np.zeros((4, 1))
		self.F = np.matrix([[1, 0, dt, 0],
						   [0, 1, 0, dt],
						   [0, 0, 1, 0],
						   [0, 0, 0, 1]])
		self.P = np.matrix([[1, 0, 0, 0],
						   [0, 1, 0, 0],
						   [0, 0, 1000, 0],
						   [0, 0, 0, 1000]])
		self.H = np.matrix([[1, 0, 0, 0],
						    [0, 1, 0, 0]])
		self.R = np.matrix([[0.0225, 0],
						    [0, 0.0225]])


	def predict(self):
		self.x = self.F * self.x
		self.P = self.F * self.P * np.transpose(self.F)

		return self.x, self.P

	def update(self, z):
		# z has the form: 2 x 1
		y = z - self.H * self.x
		H_t = np.transpose(self.H)
		S = self.H * self.P * H_t + self.R
		K = self.P * H_t * inv(S)

		# Update the state and covariance
		self.x = self.x + K * y
		self.P = self.P - K * self.H * self.P
