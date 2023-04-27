#!/bin/bash
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# openLink.sh opens a file manager window of the directory a sym-linked has its source.
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
VERSION="0.1.0"
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
targetFile=$(readlink "$1")
targetDir=$(dirname "$targetFile")
#nautilus --no-desktop "$targetDir"
xdg-open "$targetDir"
