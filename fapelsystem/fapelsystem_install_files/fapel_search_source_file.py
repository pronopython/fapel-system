#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fapel_search_source_file.py searches a matching hardlink of a tagged fapel within your
# media library.
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
#
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import shutil
from datetime import datetime
import configparser
import subprocess

##############################################################################################
#Load Config
##############################################################################################


sys.path.insert(0, INSTALLDIR)
from fapelsystemlib import fapelSystemConfig
from fapelsystemlib import dirHelper


configParser = fapelSystemConfig.FapelSystemConfig()
homedir = dirHelper.getHomeDir()




##############################################################################################
#Init Vars
##############################################################################################

#rootpath = configParser.getDir('dirs','tagDir')
#print("tagDir",rootpath)

searchResultRoot = configParser.getDir('dirs','searchResultDir')
print("searchResultDir",searchResultRoot)

inodeSearchRootDir = configParser.getDir('dirs','inodeSearchRootDir')


root = tkinter.Tk()
root.withdraw()
answer = messagebox.askquestion ('Start search?','Search may take a long time and you will get no progress info in between. Start the search?',icon = 'warning')
if answer != 'yes':
	exit()
	
	
inodeSearchRootDir = filedialog.askdirectory(initialdir=inodeSearchRootDir, title = "Choose search root folder")

if inodeSearchRootDir == ():
	exit()

print("inodeSearchRootDir",inodeSearchRootDir)

fileToSearch = os.path.abspath(sys.argv[1])
inodeToSearch = os.stat(fileToSearch).st_ino

print("File to search for:", fileToSearch)
print("iNode to search for:", inodeToSearch)


# create search result dir
searchId = datetime.now().strftime("%Y%m%d%H%M%S")
searchResultPath = searchResultRoot + "/" + searchId
os.mkdir(searchResultPath)

 
# Set up find command
findCMD = 'find "'+inodeSearchRootDir+'" -inum ' + str(inodeToSearch)

print(findCMD)

out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)


lines = out.stdout.readlines()


foundFiles = []


for line in lines:
	foundFiles.append(line.rstrip())

print(foundFiles)


# link source file
path, filename = os.path.split(fileToSearch)
#f_name, f_ext = os.path.splitext(filename)
linkFilename = "0_" + filename
os.symlink(fileToSearch,os.path.join(searchResultPath,linkFilename))


# link found files
occurance = 1
for foundFile in foundFiles:
	path, filename = os.path.split(foundFile)
	linkFilename = str(occurance) + "_" + filename
	os.symlink(foundFile,os.path.join(searchResultPath,linkFilename))
	occurance = occurance + 1


subprocess.Popen(["xdg-open", searchResultPath])


