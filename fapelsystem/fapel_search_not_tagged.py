#!/usr/bin/python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_search_not_tagged.py is TODO
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.2.0" #TODO
#
##############################################################################################
#
# Copyright (C) 2022-2023 PronoPython
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
# TODO this is almost the same code as the _not_ not py file... put it into a lib or so!

import tkinter
from tkinter import messagebox
import os
import sys
import shutil
from datetime import datetime
import configparser
import subprocess

##############################################################################################
#Load Config
##############################################################################################



from fapelsystem import config_file_handler as config_file_handler
from fapelsystem import dir_helper as dir_helper


configDir = dir_helper.getConfigDir("Fapelsystem")
#print(configDir)
configParser = config_file_handler.FapelSystemConfigFile(os.path.join(configDir,"fapel_system.conf"))
homedir = dir_helper.getHomeDir()




##############################################################################################
#Init Vars
##############################################################################################

rootpath = configParser.getDir('dirs','tagDir')
print("tagDir",rootpath)

searchResultRoot = configParser.getDir('dirs','searchResultDir')
print("searchResultDir",searchResultRoot)

# load to be excluded tag names (=dirs)
excludedSubDirs = []
for item in configParser.items('excludedTagNames'):
	excludedSubDirs.append(item[0])
print("Excluded Tag names:", excludedSubDirs)







searchDir_fullpath = os.path.abspath(sys.argv[1])



searchId = datetime.now().strftime("%Y%m%d%H%M%S")

searchResultPath = searchResultRoot + "/" + searchId

os.mkdir(searchResultPath)


fapelsInodes = set()


#excludedSubDirs = [".ts",".recycled"]

for root,d_names,f_names in os.walk(rootpath):

	traverseDir = True

	for excludedSubDir in excludedSubDirs:
		if (root.find(excludedSubDir) != -1):
			traverseDir = False

	if (traverseDir):
		for f_name in f_names:
			fapelsInodes.add(os.stat(os.path.join(root,f_name)).st_ino)

	for f_name in f_names:
		if (f_name == ".exclude_subdirs"):
			excludedSubDirs.append(root)

print("Found ", len(fapelsInodes), " Fapels")


for root,d_names,f_names in os.walk(searchDir_fullpath):

	for f_name in f_names:
		inspectedFapelFullPath = os.path.join(root,f_name)
		inode = os.stat(inspectedFapelFullPath).st_ino
		if (inode not in fapelsInodes):	# TODO the only code difference...
			print("New Found", f_name)
			os.link(inspectedFapelFullPath, os.path.join(searchResultPath, f_name))

	break

subprocess.Popen(["xdg-open", searchResultPath])


