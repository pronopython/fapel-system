#!/usr/bin/python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_tagger is a GUI based media tagging application.
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION = "0.1.0" #TODO
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
import os

def printModuleDir():
	print(os.path.dirname(os.path.realpath(__file__)))
