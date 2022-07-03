#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_fap_set enables you to hardlink media to a current date based dir.
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.1.0" #TODO
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



import tkinter
from tkinter import messagebox
import os
import sys
import shutil
from datetime import datetime,timedelta
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

# first arg is name of script
# second is file
fapel_fullpath = sys.argv[1]


fapsetDirRoot = configParser.getDir('dirs','fapsetDir')
print("fapsetDirRoot",fapsetDirRoot)

dateMidnightHoursOffset = int(configParser.get('dateAndTime','dateMidnightHoursOffset'))
fapsetId = (datetime.today() - timedelta(hours=dateMidnightHoursOffset, minutes=0)).strftime("%Y%m%d")
print("Using fapset ID",fapsetId)


##############################################################################################
#Main
##############################################################################################

fapsetDir = fapsetDirRoot + "/" + fapsetId

if not os.path.isdir(fapsetDir):
    os.mkdir(fapsetDir)



head, tail = os.path.split(fapel_fullpath)
fapel_filename = tail


# TODO what if same name? Find collision free name (as def?)
os.link(fapel_fullpath, os.path.join(fapsetDir, fapel_filename))



