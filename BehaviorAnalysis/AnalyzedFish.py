#!/usr/bin/python

class AnalyzedFish:

	def __init__(self, idnumber, genotype, dpix, rho_array, theta_array, x_array, y_array, distances, displacements, all_bouts, secmintuple, dsecmintuple, min10mintuple, dmin10mintuple, boutpermintuple, boutper10mintuple, fishevents):
		self.idnumber = idnumber # string
		self.genotype = genotype # string
		self.dpix = dpix #list
		self.rho_array = rho_array
		self.theta_array = theta_array
		self.x_array = x_array
		self.y_array = y_array
		self.distances = distances #list
		self.displacements = displacements #list
		self.all_bouts = all_bouts #list
		self.secmintuple = secmintuple #tuple of three items: dmin10minintervalactivities,dmin10minintervalstarttimes,dmin10minintervalstartindices
		self.dsecmintuple = dsecmintuple #tuple of three items: dmin10minintervalactivities,dmin10minintervalstarttimes,dmin10minintervalstartindices
		self.min10mintuple = min10mintuple #tuple of three items: dmin10minintervalactivities,dmin10minintervalstarttimes,dmin10minintervalstartindices
		self.dmin10mintuple = dmin10mintuple #tuple of three items: dmin10minintervalactivities,dmin10minintervalstarttimes,dmin10minintervalstartindices
		self.boutpermintuple = boutpermintuple
		self.boutper10mintuple = boutper10mintuple # tuple has a lot of stuff in it#return (numberofbouts, np.nan_to_num(bouttimes), np.nan_to_num(boutcumdist), np.nan_to_num(boutdisp), np.nan_to_num(boutspeeds), np.nan_to_num(boutvelocities), np.nan_to_num(boutdispoverdist), np.nan_to_num(interboutinterval)) # should I eventually make these things into objects??
		self.fishevents = fishevents # This is a list that contains the EventSection object, which contains a dictionary with keys for the event type and then a tuple of three lists for freq, dist, and latency (in that order)
