#!/usr/bin/python

class Fish:

	def __init__(self, idnumber, genotype, dpix, rho_array, theta_array, x_array, y_array, hs_dict, hs_pos_x, hs_pos_y):

		self.idnumber = idnumber # string
		self.genotype = genotype # string
		self.dpix = dpix # numpy array
		self.rho_array = rho_array # numpy array
		self.theta_array = theta_array # numpy array
		self.x_array = x_array # numpy array
		self.y_array = y_array # numpy array
		self.hs_dict = hs_dict # numpy array
		self.hs_pos_x = hs_pos_x # numpy array
		self.hs_pos_y = hs_pos_y # numpy array
