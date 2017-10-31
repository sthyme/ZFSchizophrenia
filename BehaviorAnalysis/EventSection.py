#!/usr/bin/python
import datetime
import time
from datetime import timedelta

class EventSection:

	def __init__(self, namestring, startdate):
		self.starttime = datetime.datetime.strptime(startdate + " " + namestring.split('=')[1].split('-')[0].split('_')[1], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=int(namestring.split('=')[1].split('-')[0].split('_')[0])) # datetime #df_timestart = datetime.datetime.strptime(startdate + " 13:00:15", "%Y-%m-%d %H:%M:%S") #lf_timestart = lf_timestart + datetime.timedelta(days=1)
		self.endtime = datetime.datetime.strptime(startdate + " " + namestring.split('=')[1].split('-')[1].split('_')[1], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=int(namestring.split('=')[1].split('-')[1].split('_')[0])) # datetime #df_timestart = datetime.datetime.strptime(startdate + " 13:00:15", "%Y-%m-%d %H:%M:%S") #lf_timestart = lf_timestart + datetime.timedelta(days=1)
	#	self.endtime = endtime # datetime
		self.name = namestring.split('=')[0].split('_')[1] # string #habituation_daytaps=1_15:25:30-1_16:59:00
		self.type = namestring.split('=')[0].split('_')[0] # string #habituation_daytaps=1_15:25:30-1_16:59:00
		self.events = {}
		self.boutdatadpix = {}
		self.boutdatadist = {}
		self.boutdatatotaldist = {}
		self.boutdataspeed = {}
		self.boutdatadisp = {}
		self.boutdatavel = {}
		#self.approximate_frames = self.populate_approximate_frames()
		#self.approximate_frames_slow = self.populate_approximate_frames_slow()

#	def populate_approximate_frames(self):
#		if self.type == "habituation" and "tap" in self.name:
#			return [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
#		elif self.type == "ppi":
#			return [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
#		elif "flash" in self.name:
#			return []
#		else:
#			return []

#	def populate_approximate_frames_slow(self):
#		if self.type == "habituation" and "tap" in self.name:
#			return [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#		elif "flash" in self.name:
#			return [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
#		else:
#			return []

	def add_bout_data_dpix(self, bout_data):
		self.boutdatadpix = bout_data.copy()

	def add_bout_data_dist(self, bout_data):
		self.boutdatadist = bout_data.copy()

	def add_bout_data_totaldist(self, bout_data):
		self.boutdatatotaldist = bout_data.copy()

	def add_bout_data_speed(self, bout_data):
		self.boutdataspeed = bout_data.copy()

	def add_bout_data_disp(self, bout_data):
		self.boutdatadisp = bout_data.copy()

	def add_bout_data_vel(self, bout_data):
		self.boutdatavel = bout_data.copy()

	def add_event(self, eventtype, eventvoltage, eventtime):
		if self.type != "time":
			if self.name[-9:] == "darkflash":
				if eventtype == "0" and eventvoltage == "5":
					if eventtype in self.events.keys():
						self.events[eventtype].append(eventtime)
					else:
						self.events[eventtype] = [eventtime]
				if eventtype == "103":
					if eventtype in self.events.keys():
						#print self.events[eventtype]
				##		for et in self.events[eventtype]:
						#	print "times: ", eventtime, et, eventtime.hour, et.hour, eventtime.minute, et.minute
				##			if eventtime.hour == et.hour and eventtime.minute == et.minute:
						#		print "skipping adding 103 because it's already there - september data only"
					##			continue
							self.events[eventtype].append(eventtime)
							self.events["0"].append(eventtime)
					else:
						#print "in else statement"
						self.events[eventtype] = [eventtime]
						self.events["0"] = [eventtime]
			#elif self.name == "lightflash":
			#	if (eventtype == "0" and eventvoltage == "0") or eventtype == "104":
			#		if eventtype in self.events.keys():
			#			self.events[eventtype].append(eventtime)
			#		else:
			#			self.events[eventtype] = [eventtime]
			elif self.name[-9:] == "ightflash":
				if eventtype == "0" and eventvoltage == "0":
					if eventtype in self.events.keys():
						self.events[eventtype].append(eventtime)
					else:
						self.events[eventtype] = [eventtime]
				if eventtype == "104":
					if eventtype in self.events.keys():
							self.events[eventtype].append(eventtime)
							self.events["0"].append(eventtime)
					else:
						#print "in else statement"
						self.events[eventtype] = [eventtime]
						self.events["0"] = [eventtime]
			elif self.type == "habituation" and eventtype =="102":
				if eventtype in self.events.keys():
					self.events[eventtype].append(eventtime)
					self.events["1"].append(eventtime)
				else:
					self.events[eventtype] = [eventtime]
					self.events["1"] = [eventtime]
			elif self.type == "ppi" and eventtype == "100":
				if eventtype + "a" in self.events.keys():
					self.events[eventtype + "a"].append(eventtime)
					self.events[eventtype + "b"].append(eventtime)
					self.events[eventtype + "c"].append(eventtime)
					self.events[eventtype + "d"].append(eventtime)
				else:
					self.events[eventtype + "a"] = [eventtime]
					self.events[eventtype + "b"] = [eventtime]
					self.events[eventtype + "c"] = [eventtime]
					self.events[eventtype + "d"] = [eventtime]
			elif self.type == "voltthreshold":
				if eventtype + "_" + str(''.join(eventvoltage.split("."))) in self.events.keys():
					self.events[eventtype + "_" + str(''.join(eventvoltage.split(".")))].append(eventtime)
				else:
					self.events[eventtype + "_" + str(''.join(eventvoltage.split(".")))] = [eventtime]
			else:
				if eventtype in self.events.keys():
					self.events[eventtype].append(eventtime)
				else:
					self.events[eventtype] = [eventtime]
#types = ppi, habituation, slowspeedtime, doubleevent (ie, light + tap or dark + tap), lightchange ??
