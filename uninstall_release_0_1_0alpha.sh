#!/bin/bash
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# install.sh is the installer script to copy all py files and create nautilus shortcuts
#
# For updates see git-repo at
#https://github.com/pronopython/fapel-system
#
##############################################################################################
#
INSTALLDIR=/opt/fapelsystem
CONFIGDIR=~/.config
NAUTILUSSCRIPTDIR=~/.local/share/nautilus/scripts
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

echo "This will uninstall all program files of the fapelsystem version 0.1.0-alpha"
echo "The following files will be deleted:"
echo "  - all files under /opt/fapelsystem (=all program files)"
echo "  - all script links under Nautilus right click menu"
echo ""
echo "Media files, Tags or config files will NOT be deleted, but use at your own risk."
echo "Sudo is needed to delete these files."
echo ""

while true; do

read -p "Delete fapelsystem program files and script links? (y/n) " yn

case $yn in 
	[yY] )  sudo rm -r /opt/fapelsystem;
			sudo rm $NAUTILUSSCRIPTDIR/*fapel*.py
			sudo rm $NAUTILUSSCRIPTDIR/*open-softlink*.sh
			break;;

	[nN] )  break;;

	* ) echo invalid response;;
esac

done

