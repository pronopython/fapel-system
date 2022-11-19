#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# tagPackExport can be used to export a Tag Directory Structure to a tagPack CSV file
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.1.0"
INSTALLDIR="/opt/fapelsystem"
#
##############################################################################################
#
# Copyright (C) 2022 PronoPython
#
# Contact me at pronopython@proton.me
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################################
# TODO Bug: .ts , . , .recycled etc will be exported, too

import os
import sys
import csv
import getopt
import codecs
import configparser
import codecs


print("TagPack Exporter")



##############################################################################################
#Import lib
##############################################################################################

sys.path.insert(0, INSTALLDIR)
from fapelsystemlib import fapelSystemConfig
from fapelsystemlib import dirHelper


configParser = fapelSystemConfig.FapelSystemConfig()


##############################################################################################
#Vars
##############################################################################################


tagPackFilename = None
rot13enabled = True
NSFWenabled = False
info = ""

##############################################################################################
#Args
##############################################################################################



if len(sys.argv) == 1:
	# TODO print a help
	sys.exit(2)

try:
	opts, args = getopt.getopt(sys.argv[1:],"?hcni:",[])
except getopt.GetoptError:
	# TODO print a help
	sys.exit(2)


for opt, arg in opts:
	if (opt == '-h') or (opt == '-?'):
		# TODO print a help
		sys.exit(2)
	elif (opt == '-c'): # clear text instead of rot13
		rot13enabled = False
	elif (opt == '-n'):
		NSFWenabled = True
	elif (opt == '-i'):
		info = arg


if (len(args) == 1):
	tagPackFilename = args[0]
else:
	pass
	# TODO error, no tagpack...





rootpath = configParser.getDir('dirs','tagDir')

print("Exporting tags from", rootpath)


file = open(tagPackFilename, mode ='w')
csvFile = csv.writer(file, delimiter=";")


#csvFile.writerow(["REM",";","\"",""])


csvFile.writerow(["REM","Parameter A","Parameter B","Parameter C"])
csvFile.writerow(["VERSION","1","",""])
csvFile.writerow(["REM","Exported with tagPackExport","",""])


if info != "":
	csvFile.writerow(["INFO",info,"",""])


if NSFWenabled:	
	csvFile.writerow(["NSFW","","",""])





csvFile.writerow(["REM","#####################################################################################","",""])

if rot13enabled:
	csvFile.writerow(["ROT","on","on","off"])



excludedSubDirs = []


for counterEntry in configParser.items("countersDirs"):
	cdir = counterEntry[1]
	cdir = dirHelper.expandHomeDir(cdir)

	if (cdir.startswith(rootpath)):
		excludedSubDirs.append(cdir)
		print("Counter",cdir,"will be excluded")




for root,d_names,f_names in os.walk(rootpath):
	#print (root, d_names, f_names)

	tagproperties = ""
	
	traverseSubDirs = True
	excludeTag = False
	for f_name in f_names:
		if (f_name == ".exclude_subdirs"):
			traverseSubDirs = False
			excludedSubDirs.append(root)
			if tagproperties != "":
				tagproperties = tagproperties + ","
			tagproperties = tagproperties + "exclude_subdirs"

		if (f_name == ".hide_button"):
			if tagproperties != "":
				tagproperties = tagproperties + ","
			tagproperties = tagproperties + "hide_button"
		if (f_name == ".hide_child_buttons"):
			if tagproperties != "":
				tagproperties = tagproperties + ","
			tagproperties = tagproperties + "hide_child_buttons"

	for excludedSubDir in excludedSubDirs:
		if (root.find(excludedSubDir) != -1):
			traverseSubDirs = False
			excludeTag = True

	if not excludeTag:

		tooltip = ""
		if (os.path.isfile(os.path.join(root,".taginfo"))):
			configParserTT = configparser.RawConfigParser()
			configParserTT.read(os.path.join(root,".taginfo"))
			tooltip = configParserTT.get('general','tooltip')
		



		tagname = os.path.relpath(root, rootpath)
		if not rot13enabled:
			csvFile.writerow(["TAG",tagname,tooltip,tagproperties])
		else:
			csvFile.writerow(["TAG",codecs.encode(tagname, 'rot_13'),codecs.encode(tooltip, 'rot_13'),tagproperties])



