#!/usr/bin/python

import os,sys,glob,re
import subprocess

#subprocess.call(['./cleanup.sh'])
for file in glob.glob("fastqc_script*"):
	lfile = open(file, 'r')
	lines = lfile.readlines()
	for line in range(0, len(lines)):
		if lines[line].startswith("cd"):
			dir = lines[line].split()[1]
			os.mkdir(dir)
			#outputfulldata_bag5homfxhetmOct18_het_vs_bag5homfxhetmOct18_hom
for files in glob.glob("oldfiles_2017-07-28/sectionsfile"):
	lfiles = open(files, 'r')
	liness = lfiles.readlines()
	for sline in range(0,len(liness)):
		if liness[sline].startswith("time_day2heatshock"):
			hstime = liness[sline].strip()
		if liness[sline].startswith("time_combo"):
			ctimeend = liness[sline].split("-")[1]
#Only lines specific to a gene because they depend on end time
# start time should be good now that I'm doing 11:59 for everything
# I don't need that first hour on day 1
#time_day2heatshock=2_17:01:00-2_18:12:00
#time_combo=0_23:10:00-2_18:12:00
ffile = open('sectionsfile', 'w')
ffile.write("habituation_darkflash=2_10:00:00-2_17:00:00\n")
ffile.write("habituation_a0darkflash=2_10:00:00-2_10:10:30\n")
ffile.write("habituation_adarkflash=2_10:00:00-2_10:10:30\n")
ffile.write("habituation_a2darkflash=2_10:50:00-2_11:00:00\n")
ffile.write("habituation_bdarkflash=2_12:00:00-2_12:10:30\n")
ffile.write("habituation_b2darkflash=2_12:50:00-2_13:00:00\n")
ffile.write("habituation_cdarkflash=2_14:00:00-2_14:10:30\n")
ffile.write("habituation_c2darkflash=2_14:50:00-2_15:00:00\n")
ffile.write("habituation_ddarkflash=2_16:00:00-2_16:10:30\n")
ffile.write("habituation_d2darkflash=2_16:50:00-2_17:00:00\n")
ffile.write("habituation_d0darkflash=2_16:00:00-2_16:10:30\n")
ffile.write("response_lightflash=1_09:10:00-1_09:31:00\n")
ffile.write("response_nightlightflash=2_04:24:59-2_04:55:00\n")
ffile.write("response_night106=2_05:44:00-2_06:15:00\n")
ffile.write("response_106=1_10:10:00-1_10:31:00\n")
ffile.write("ppi_dayprepulseinhibition=1_14:00:01-1_17:00:00\n")
ffile.write("ppi_shortdayprepulseinhibition=1_14:00:01-1_14:20:00\n")
ffile.write("ppi_nightprepulseinhibition=2_01:00:01-2_02:00:01\n")
ffile.write("ppi_shortnightprepulseinhibition=2_01:00:01-2_01:20:01\n")
ffile.write("habituation_adaytap=1_17:30:00-1_17:55:00\n")
ffile.write("habituation_adaytaphab=1_17:45:00-1_17:47:00\n")
ffile.write("habituation_adaytappre=1_17:30:00-1_17:36:00\n")
ffile.write("habituation_adaytappostbdaytappre=1_17:49:00-1_17:55:00\n")
ffile.write("habituation_bdaytap=1_17:49:00-1_18:14:00\n")
ffile.write("habituation_bdaytaphab=1_18:04:00-1_18:06:00\n")
ffile.write("habituation_bdaytappostcdaytappre=1_18:08:00-1_18:14:00\n")
ffile.write("habituation_cdaytap=1_18:08:00-1_18:33:00\n")
ffile.write("habituation_cdaytaphab=1_18:23:00-1_18:25:00\n")
ffile.write("habituation_cdaytappost=1_18:27:00-1_18:33:00\n")
ffile.write("habituation_ddaytappost=1_19:02:00-1_19:07:00\n")
ffile.write("habituation_nighttap=2_03:00:00-2_03:25:00\n")
ffile.write("habituation_nighttappre=2_03:00:00-2_03:06:00\n")
ffile.write("habituation_nighttaphab=2_03:15:00-2_03:17:00\n")
ffile.write("habituation_nighttappost=2_03:19:00-2_03:25:00\n")
ffile.write("time_day1night=0_23:59:00-1_08:59:01\n")
ffile.write("time_day1morntrans=1_09:00:05-1_09:10:06\n")
ffile.write("time_day1mornstim=1_09:10:00-1_11:15:01\n")
ffile.write("time_day1day=1_11:15:00-1_14:00:01\n")
ffile.write("time_day1taps=1_14:00:00-1_19:22:01\n")
ffile.write("time_day1evening=1_19:22:00-1_22:59:01\n")
ffile.write("time_day2nighttrans=1_23:00:05-1_23:10:06\n")
ffile.write("time_day2night1=1_23:10:00-2_01:00:01\n")
ffile.write("time_day2nightstim=2_01:00:00-2_07:00:01\n")
ffile.write("time_day2night2=2_07:00:00-2_08:59:01\n")
ffile.write("time_day2morntrans=2_09:00:05-2_09:10:06\n")
ffile.write("time_day2morning=2_09:10:00-2_10:00:01\n")
ffile.write("time_day2darkflashes=2_10:00:00-2_17:00:01\n")
ffile.write(hstime + "\n")
ffile.write("time_combo=0_23:59:00-" + ctimeend)
