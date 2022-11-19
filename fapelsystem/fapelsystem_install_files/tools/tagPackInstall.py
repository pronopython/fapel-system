#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# tagPackInstall creates Dirs from a tagPack CSV file within the Tag folder
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.1.1" #TODO
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
#
# TODO: uninstaller, remove all which was not used (= no fapels present)
#       therefore a "Play" must run in positive (down) direction
#       then play that backwards, which thenn removes /Models/A and then /Models


import os
import sys
import csv
import getopt
import codecs






print("TagPack Installer")



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

simulation = False
tagPackFilename = None

##############################################################################################
#Args
##############################################################################################



if len(sys.argv) == 1:
	# TODO print a help
	sys.exit(2)

try:
	opts, args = getopt.getopt(sys.argv[1:],"?hs",[])
except getopt.GetoptError:
	# TODO print a help
	sys.exit(2)


for opt, arg in opts:
	if (opt == '-h') or (opt == '-?'):
		# TODO print a help
		sys.exit(2)
	elif opt == '-s':
		print("Simulation on")
		simulation = True

if (len(args) == 1):
	tagPackFilename = args[0]
else:
	pass
	# TODO error, no tagpack...



rootpath = configParser.getDir('dirs','tagDir')

print("Installing tags to", rootpath)


counterEmojis = None
 
file = open(tagPackFilename, mode ='r')
csvFile = csv.reader(file, delimiter=";")
linenumber = 0
rot13on = None
for line in csvFile:
	if rot13on == None:
		rot13on = [False]*len(line)

	if line[0] != "ROT":
		for position,item in enumerate(line):
			if rot13on[position]:
				line[position] = codecs.encode(item, 'rot_13')

	linenumber = linenumber + 1

	if line[0] == "INFO":
		print(line[1])
	elif line[0] == "VERSION":
		print("Version of file:",line[1])
		if line[1] != "1":
			print("Wrong TagPack version, check for updates of this program! Giving up!")
			sys.exit(1)

	elif line[0] == "NSFW":
		answer = input("TagPack contains NSFW content. Do you want to proceed? (y/n)")
		if not ((answer == "y") or (answer == "Y")):
			sys.exit(0)

	elif line[0] == "ROT":
		for position,item in enumerate(line):
			if item.lower() == "on":
				rot13on[position] = True
			else:
				rot13on[position] = False

	elif line[0] == "TAG":


		if line[1].find("../") != -1:
			print("Malicious relative path found in tagPack file tag dir:")
			print(line[1])
			print("aborting")
			sys.exit(1)

		if line[3].find("../") != -1:
			print("Malicious relative path found in tagPack file dot filename:")
			print(line[3])
			print("aborting")
			sys.exit(1)



		tagpath = os.path.join(rootpath, line[1])
		if not os.path.isdir(tagpath):
			print("Creating tag",line[1])
			if not simulation:
				#os.mkdir(tagpath)
				os.makedirs(tagpath , exist_ok=True )

				# create tool tip?
				if line[2] != "":
					tooltipfilename = os.path.join(tagpath,".taginfo")
					if not os.path.isfile(tooltipfilename):
						with open(tooltipfilename, 'w') as f:
							f.write('[general]')
							f.write(os.linesep)
							f.write('tooltip='+line[2])
							f.write(os.linesep)
				# create . dot files
				if line[3] != "":
					dotFilenames = line[3].split(",")
					for dotFilename in dotFilenames:
						dotFilename = os.path.join(tagpath,"."+dotFilename)
						if not os.path.isfile(dotFilename):
							with open(dotFilename, 'w') as f:
								pass




	elif line[0] == "COUNTER":


		counterDestinationPath = os.path.join(rootpath, line[1])
		
		scriptPath = configParser.getDir('dirs','filemanagerScriptDir')
		
		linkName = line[2]
		linkNameEmojis = line[3].encode('UTF-8').decode('unicode-escape')

		print("Counter:")
		print("   Tag:",counterDestinationPath)
		print("   Rightclick script:", linkName," / ",linkNameEmojis)
		

		answer = input("Install this counter? (y/n)")
		
		if ((answer == "y") or (answer == "Y")):
		
			if (counterEmojis == None):
				answer = input("Install nautilus scripts with emojis? (y/n)")
				counterEmojis = (answer == "y") or (answer == "Y")

			if counterEmojis:
				linkFilename = os.path.join(scriptPath,linkNameEmojis)
			else:
				linkFilename = os.path.join(scriptPath,linkName)

			if not os.path.isfile(linkFilename):
				print("Creating counter",linkName)
				if not simulation:

					os.symlink(os.path.join(INSTALLDIR,"fapel_counter.py"),linkFilename)

					counterKey = dirHelper.getLastPartOfFilename(linkFilename)
					print("Counter Name:", counterKey)


					counterPath = os.path.join(configParser.getDir('dirs','tagDir'),line[1])
					configParser.changeConfig()['countersDirs'][counterKey] = counterPath


					print("Installed counter",counterKey)


	elif line[0] == "REM":
		# it's just a remark, so just pass on
		pass

	else:
		print("Unknown command",line[0],"in line",linenumber)
		

configParser.writeChangedConfig()
