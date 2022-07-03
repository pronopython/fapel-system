#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.1.0" #TODO
CONFIGFILE="~/.config/fapel_system.conf"
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
import os
from pathlib import Path
import configparser
from fapelsystemlib import dirHelper


##############################################################################################
#Load Config
##############################################################################################

class FapelSystemConfig:

	
	def __init__(self):
		global CONFIGFILE
		self.configFilePath = CONFIGFILE

		self.homedir = dirHelper.getHomeDir()
		self.configFilePath = dirHelper.expandHomeDir(CONFIGFILE)



		self.createConfigParserAndLoadConfig()
		self.configChanged = False

	def createConfigParserAndLoadConfig(self):
		self.configParser = None
		print("Opening config file",self.configFilePath)
		if (os.path.isfile(self.configFilePath)):
			self.configParser = configparser.RawConfigParser(allow_no_value=True)
			self.configParser.read(self.configFilePath)
			#print(self.configParser.get('dirs','tagDir'))
		else:
			print("Config file is missing, abort!")
			exit()
			
	def getConfigParser(self):
		return self.configParser



	def get(self, group, key):
		return self.configParser.get(group, key)


	def getInt(self, group, key):
		return int(self.configParser.get(group, key))
	
		
	def getDir(self, group, key):
		path = self.get(group, key)
		return path.replace("~", self.homedir)

	
	def items(self, group):
		return self.configParser.items(group)

	def changeConfig(self):
		self.configChanged = True
		return self.configParser		
		
	def writeChangedConfig(self):
		if self.configChanged:
			print("Writing changes to config file",self.configFilePath)
			configfile = open(self.configFilePath, 'w')
			self.configParser.write(configfile)		

