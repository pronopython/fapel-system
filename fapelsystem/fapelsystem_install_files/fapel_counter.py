#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_counter tags media with an upward counting tag
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
# TODO collision untested (filenames are present AND matched instead of inode)



import tkinter
from tkinter import messagebox
import os
import sys
import shutil




##############################################################################################
#Import lib
##############################################################################################

sys.path.insert(0, INSTALLDIR)
from fapelsystemlib import fapelSystemConfig
from fapelsystemlib import dirHelper


configParser = fapelSystemConfig.FapelSystemConfig()



##############################################################################################
#Init Vars
##############################################################################################


# first arg is name of script
# second is file

rootPathKey = None


if (len(sys.argv) != 2):
	print("You must start this with one file as the one to be counted")
	sys.exit()


noticeableFapel_fullpath = os.path.abspath(sys.argv[1])


# counter name is derived from the last part after - or _ of this script's name
# this can also be from a soft link to this script (which is the main way to
# start this script
# so softlink what_else_counts_cucumber.py -> fapel_counter.py will look for the
# key "cucumber" in the conf file
rootPathKey = dirHelper.getLastPartOfFilename(os.path.abspath(sys.argv[0]))
print("Counter Name:",rootPathKey)



rootpath = configParser.getDir('countersDirs',rootPathKey)
print(rootPathKey,rootpath)


##############################################################################################
#Main
##############################################################################################






head, tail = os.path.split(noticeableFapel_fullpath)
noticeableFapel_filename = tail
twin_current_dir = ""



print("looking for file ",noticeableFapel_filename)
for root,d_names,f_names in os.walk(rootpath):
    #print (root, d_names, f_names)
    for f_name in f_names:
        #tagname = os.path.relpath(os.path.join(root, d_name), rootpath)
        #tag = Tag(tagname)
        #tag.dir = os.path.join(root, d_name)
        #tags.add(tag)
        print (noticeableFapel_filename,f_name)
        if noticeableFapel_filename == f_name:
            # match
            twin_current_dir = root
            twin_current_fullpath = os.path.join(root, f_name)
            twin_filename = f_name


if twin_current_dir != "":
    # found in one of the dirs, move one further
    currentNoticeNumber = int(os.path.relpath(twin_current_dir, rootpath))
    nextNoticeNumber = currentNoticeNumber + 1

    nextNoticePath = os.path.join(rootpath, f"{nextNoticeNumber:04d}")

    if not os.path.isdir(nextNoticePath):
        # notice number does not exist
        os.mkdir(nextNoticePath)

    # rename till it fits
    new_twin_name = twin_filename
    destinationFilename = os.path.join(nextNoticePath, new_twin_name)
    while os.path.isfile(destinationFilename):
        #change filename
        f_name, f_ext = os.path.splitext(new_twin_name)
        new_twin_name = f_name + "_A" + f_ext
        destinationFilename = os.path.join(nextNoticePath, new_twin_name)

    os.rename(twin_current_fullpath, destinationFilename)

    # if old twin dir is empty delete it
    if len(os.listdir(twin_current_dir)) == 0:
        #os.remove(twin_current_dir)
        pass # TODO old twin dir is empty delete it .. or not??

    # message
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo(noticeableFapel_filename, ""+str(currentNoticeNumber)+u" \u2192 "+str(nextNoticeNumber))

else:
    # must be hardlinked into 0001 dir
    print ("new, mv to 0001")
    nextNoticeNumber = 1

    nextNoticePath = os.path.join(rootpath, f"{nextNoticeNumber:04d}")

    if not os.path.isdir(nextNoticePath):
        # notice number does not exist
        os.mkdir(nextNoticePath)

    # rename till it fits
    new_twin_name = noticeableFapel_filename
    destinationFilename = os.path.join(nextNoticePath, new_twin_name)
    while os.path.isfile(destinationFilename):
        # change filename
        f_name, f_ext = os.path.splitext(new_twin_name)
        new_twin_name = f_name + "_A" + f_ext
        destinationFilename = os.path.join(nextNoticePath, new_twin_name)

    os.link(noticeableFapel_fullpath, destinationFilename)
    # message
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo(noticeableFapel_filename, u"new \u2192 1")
