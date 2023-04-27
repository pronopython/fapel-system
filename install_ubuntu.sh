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
VERSION=0.1.0
#
CONFIGDIR=~/.config
NAUTILUSSCRIPTDIR=~/.local/share/nautilus/scripts
INSTALLDIR=""
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
# TODO comment header
# TODO clean out comments



##################################################################################

##################################################################################

EMOJIUNICORN=$(echo -e "\U1F984")
EMOJIEGGPLANT=$(echo -e "\U1F346")
EMOJIWATER=$(echo -e "\U1F4A6")
#EMOJITAG=$(echo -e "\U1F3F7")
EMOJITAG=$(echo -e "\U2705")
#EMOJIHEARTS=$(echo -e "\U1F60D")
EMOJIHEARTS=$(echo -e "\U2764\UFE0F")
EMOJIMAGGLAS=$(echo -e "\U1F50D")
EMOJICALENDAR=$(echo -e "\U1F4C5")
EMOJIARROW=$(echo -e "\U27A1")
EMOJIISLAND=$(echo -e "\U1F3DD")
EMOJITROPHY=$(echo -e "\U1F3C6")

##################################################################################

link_module () {
	echo "installing $1"
	sudo ln -s $INSTALLDIR/$1 $NAUTILUSSCRIPTDIR/$2
	sudo chown $USER:$USER $NAUTILUSSCRIPTDIR/$2
}

##################################################################################


echo "fapelsystem installer v${VERSION}"
echo ""
echo "The installer now creates the program dirs and config files."
echo "Sudo is needed for some actions."
echo ""

#pip install .


if ! type "fapelsystem_printModuleDir" >/dev/null 2>&1; then
	echo "Installing fapel system module via pip"
	pip install .
	echo ""
fi


INSTALLDIR="$(fapelsystem_printModuleDir)"

echo "fapel system module installed in: ${INSTALLDIR}"
echo ""

echo "Copying config file..."
cp -i $INSTALLDIR/fapel_system_template.conf $CONFIGDIR/fapel_system.conf


echo ""
echo "The fapelsystem works with nautilus file manager through scripts in nautilus' script dir."
echo "These scripts can have emoji names for better visualization of their function."
echo "You can now choose if you want them with or without emojis in their names."
echo "Note that sudo is needed for that action."
echo ""

while true; do

read -p "Install nautilus scripts with emojis? (y/n) " yn

case $yn in 
	[yY] )  link_module fapel_tagger.py 1${EMOJITAG}--fapel-tagger.py;
		link_module fapel_counter.py 2${EMOJIHEARTS}--fapel-notice.py;
		link_module fapel_counter.py 6${EMOJIEGGPLANT}${EMOJIWATER}--fapel-ct.py;
		link_module fapel_search_not_tagged.py 5${EMOJIMAGGLAS}--fapel-search-not-tagged.py;
		link_module fapel_search_source_file.py 5${EMOJIMAGGLAS}--fapel-search-source-file.py;
		link_module fapel_search_tagged.py 4${EMOJIMAGGLAS}--fapel-search-tagged.py;
		link_module fapel_fap_set.py 3${EMOJICALENDAR}--fapel-fap-set.py;
		link_module openLink.sh 9${EMOJIARROW}--open-softlink-folder.sh;
		link_module fapel_exiles.py 9${EMOJIISLAND}--fapel-exiles.py;
		link_module fapel_elo.py 9${EMOJITROPHY}--fapel-elo.py;
		break;;

	[nN] )  link_module fapel_tagger.py 1-fapel-tagger.py;
		link_module fapel_counter.py 2-fapel-notice.py;
		link_module fapel_counter.py 6-fapel-ct.py;
		link_module fapel_search_not_tagged.py 5-fapel-search-not-tagged.py;
		link_module fapel_search_source_file.py 5-fapel-search-source-file.py;
		link_module fapel_search_tagged.py 4-fapel-search-tagged.py;
		link_module fapel_fap_set.py 3-fapel-fap-set.py;
		link_module openLink.sh 9-open-softlink-folder.sh;
		link_module fapel_exiles.py 9-fapel-exiles.py;
		link_module fapel_elo.py 9-fapel-elo.py;
		break;;
		
	* ) echo invalid response;;
esac

done

echo "Changing permissions on installed module files"
sudo chmod 0755 $INSTALLDIR/*.py
sudo chmod 0755 $INSTALLDIR/*.sh
sudo chmod 0644 $INSTALLDIR/*.conf
sudo chmod 0644 $INSTALLDIR/fapxile_file_template





echo ""
echo "The fapelsystem needs directories to place media and their tags (which are also directories)."
echo "You can edit the config file to point the fapelsystem to an existing directory structure"
echo "or this script can now create a basic, empty structure under your home dir"
echo "            ~/fapelsystem/"
echo "for you. This will then work out-of-the-box with the provided config file."
echo "It is also needed for the tag packs."
echo ""

while true; do

read -p "Install fapelsystem basic directories? (y/n) " yn

case $yn in 
	[yY] )  mkdir ~/fapelsystem;
		mkdir ~/fapelsystem/Tags;
		mkdir ~/fapelsystem/Tags/.recycled;
		mkdir ~/fapelsystem/Notice;
		mkdir ~/fapelsystem/Tags/Ct;
		mkdir ~/fapelsystem/Tags/Ct/Ct;
		touch ~/fapelsystem/Tags/Ct/Ct/.hide_button
		touch ~/fapelsystem/Tags/Ct/Ct/.hide_child_buttons

		echo "[fapxileForThisTag]" > ~/fapelsystem/Tags/Ct/Ct/.fapxile
		echo "[fapxileForFapelsOfThisTag]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
		echo "[fapxileForSubTagsAndSubFapels]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
		echo "ct" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
		echo "[excludedSubTags]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
		echo "Ct/Ct/0001" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile


		mkdir ~/fapelsystem/Tags/Hoover_over_me_for_a_tip

        echo "[general]" > ~/fapelsystem/Tags/Hoover_over_me_for_a_tip/.taginfo
        echo "tooltip='Create more Tags by simply creating directories under ~/fapelsystem/Tags'" >> ~/fapelsystem/Tags/Hoover_over_me_for_a_tip/.taginfo



		mkdir ~/fapelsystem/Elo;
		mkdir ~/fapelsystem/Search\ Results;
		mkdir ~/fapelsystem/Fapsets;
		break;;

	[nN] )  break;;

	* ) echo invalid response;;
esac

done


echo "done"

