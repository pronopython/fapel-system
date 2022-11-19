#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_exiles can dynamically hide media in the filemanager through updating the .hidden
# files.
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


from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font
import os
import sys
import configparser
import time


##############################################################################################
#Import lib
##############################################################################################

sys.path.insert(0, INSTALLDIR)
from fapelsystemlib import fapelSystemConfig
from fapelsystemlib import dirHelper


configParser = fapelSystemConfig.FapelSystemConfig()
homedir = dirHelper.getHomeDir()



##############################################################################################
#Init Vars
##############################################################################################

rootpath = configParser.getDir('dirs','tagDir')
print("tagDir",rootpath)


# load to be excluded tag names (=dirs)
excludedTagNames = []
for item in configParser.items('excludedTagNames'):
	excludedTagNames.append(item[0])
print("Excluded Tag names:",excludedTagNames)

# load colors
FT_COLORS = {}
for item in configParser.items('colors'):
	FT_COLORS[item[0]]=item[1]

##############################################################################################

class Fapel:
	def __init__(self, fullpath):
		self.tags = set()
		self.fullPath = fullpath
		head, tail = os.path.split(self.fullPath)
		self.filename = tail
		self.tagFilenames = {} # {tag,filename within tag} dictionary

		self.inode = os.stat(fullpath).st_ino
		
		self.exiled = False

class Tag:
	def __init__(self, name):
		self.name = name
		self.shortname = ""
		self.initialFapels = set()
		self.currentFapels = set()
		self.toBeRemovedFapels = set()
		self.allFapels = set()
		self.dir = ""
		self.button = None
		self.tooltip = ""
		# Tree Stuff
		self.parent = None
		self.children = []
		self.depth = 0
		# Finder Stuff
		self.listbox = None
		self.fg = "#FFFFFF"  # TODO remove
		self.bg = "#000000"   # TODO remove
		self.hideButton = False
		self.hideChildButtons = False


		self.hideFor = []
		self.hideFapelsFor = []
		self.hidesubFapelsFor = []
		self.excludedSubTags = []

		self.hidden = []



	def addChild(self, child):
		self.children.append(child)
		self.children = sorted(self.children, key=Tag.getTagShortName)
		child.parent = self
		child.depth = self.depth + 1

	# used as a comparator / key for sorting
	@staticmethod
	def getTagShortName(tag):
		return tag.shortname



class FapxileStatusFile:
	def __init__(self, filename):
		self.filename = filename

		self.configParserTT = configparser.RawConfigParser(allow_no_value=True, strict=False)
		self.configParserTT.optionxform = str # do *not* make everything lowercase
		self.hiddenFapxiles = []
		try:
			self.configParserTT.read(self.filename)
			self.hiddenFapxiles = self.getEntries('hiddenFapxiles')

		except:
			print("Error loading fapxile status file, continue without it")

	def writeStatusFile(self):

		print("Writing changes to status file",self.filename)
		configfile = open(self.filename, 'w')

		self.configParserTT['hiddenFapxiles'] = {}
		for hiddenFapxile in self.hiddenFapxiles:
			self.configParserTT['hiddenFapxiles'][hiddenFapxile] = None

		self.configParserTT.write(configfile)



	def getEntries(self, groupname):
		items = self.configParserTT.items(groupname)
		names = []
		for item in items:
			names.append(item[0])
		return names

class FapxileFile:
	def __init__(self, filename):
		self.filename = filename

		self.configParserTT = configparser.RawConfigParser(allow_no_value=True, strict=False)
		self.configParserTT.optionxform = str # do *not* make everything lowercase
		self.configParserTT.read(self.filename)

		self.fapxileForThisTag = self.getFapxileNames('fapxileForThisTag')
		self.fapxileForFapelsOfThisTag = self.getFapxileNames('fapxileForFapelsOfThisTag')
		self.fapxileForSubTagsAndSubFapels = self.getFapxileNames('fapxileForSubTagsAndSubFapels')

		self.excludedSubTags = self.getFapxileNames('excludedSubTags')


		#print(self.getAllFapxiles())
	
	def getFapxileForThisTag(self):
		return self.fapxileForThisTag
	def getFapxileForFapelsOfThisTag(self):
		return self.fapxileForFapelsOfThisTag
	def getFapxileForSubTagsAndSubFapels(self):
		return self.fapxileForSubTagsAndSubFapels
	def getAllFapxiles(self):
		return list(set(self.fapxileForThisTag) | set(self.fapxileForFapelsOfThisTag) | set(self.fapxileForSubTagsAndSubFapels))

	
	
	def getFapxileNames(self, groupname):
		items = self.configParserTT.items(groupname)
		names = []
		for item in items:
			names.append(item[0])
		return names



class FapxileButton(Button):
	global FT_COLORS
	status: int

	def __init__(self, window, fapxile):
		self.fapxile = fapxile
		self.status = 0
		super().__init__(window, text="visible")
		self.configure(command=self.clicked)
		#self.updatestatus()
		self.updatecolor()


	def clicked(self):
		self.status = 1 - self.status
		self.updatetext()
		self.updatecolor()

	def updatetext(self):
		if self.status == 0:
			self.config(text='visible')
		else:
			self.config(text='hidden')



	def updatecolor(self):
		if self.status == 0:
			self['bg'] = FT_COLORS["button_tag_unselected"]
		elif self.status == 2:
			self['bg'] = FT_COLORS["button_tag_partially"]
		elif self.status == 1:
			self['bg'] = FT_COLORS["button_tag_selected"]


def clickShowAllButton():
	for button in allButtons:
		button.status = 0
		button.updatetext()
		button.updatecolor()


def clickHideAllButton():
	for button in allButtons:
		button.status = 1
		button.updatetext()
		button.updatecolor()



def clickCancel():
	window.destroy()

def clickApply():

	# gather all fapxiles to hide (read out button selection)
	hiddenFapxiles = set()
	for button in allButtons:
		if button.status != 0:
			hiddenFapxiles.add(button.fapxile)

	# go through every tag and check it's exile definition
	for tag in tags:
		#print(tag.dir)
	
	
		# [1] Hide all Tags with hideFor directly
		hideFor = (list(set(tag.hideFor) & hiddenFapxiles))
		#print(hideFor)
		if len(hideFor) > 0:
			tag.parent.hidden.append(tag.shortname)
			print("Hiding Tag",tag.name)



		# [2] hideFapelsFor
		# check if to hide
		# for every fapel, go to every tag, add fapel there

		hideFapelsFor = (list(set(tag.hideFapelsFor) & hiddenFapxiles))
		#print(hideFapelsFor)
		if len(hideFapelsFor) > 0:
			print("Hiding all Fapel of Tag",tag.name)
			for fapel in tag.allFapels:
				#print("for Fapel:",fapel.fullPath)
	

				for ftag in fapel.tags:
					#print("--has Tag -> ",ftag.name)

					path, filename = os.path.split(fapel.tagFilenames[ftag])
					#print(filename)
					ftag.hidden.append(filename)



		# [3] hidesubFapelsFor
		# check if to hide
		# for every sub tag recursive, all fapels, all their tags add hidden there
	
		hidesubFapelsFor = (list(set(tag.hidesubFapelsFor) & hiddenFapxiles))
		#print(hidesubFapelsFor)
		if len(hidesubFapelsFor) > 0:
			print("Recursivly hiding everything within tag", tag.name)
			tagstack = []
			tagstack.extend(tag.children) # only use the child tags, not this tag
			while len(tagstack) > 0:
				ctag = tagstack.pop()

				if ctag.name in tag.excludedSubTags:
					print(" - ignoring SubTag",ctag.name)
					continue

				tagstack.extend(ctag.children)
				#print("visiting",ctag.shortname)

				print(" + Hiding all Fapel of sub Tag",ctag.name)
				# hide subtag itself
				if ctag.shortname not in ctag.parent.hidden:
					ctag.parent.hidden.append(ctag.shortname)	
				# hide all fapels of the subtag everywhere
				for fapel in ctag.allFapels:
					#print("for Fapel:",fapel.fullPath)
		
					#print("Hiding Fapel",fapel.fullPath)

					for ftag in fapel.tags:
						#print("--has Tag -> ",ftag.name)

						path, filename = os.path.split(fapel.tagFilenames[ftag])
						#print(filename)
						if filename not in ftag.hidden:
							ftag.hidden.append(filename)

	hiddenFileCounter = 0
	hiddenFileLines = 0
	# write .hidden files
	for tag in tags:
		with open(os.path.join(tag.dir, ".hidden"), 'w',encoding='utf-8') as f:
			if len(tag.hidden) > 0:
				for name in tag.hidden:
					f.write(name)
					f.write("\n")
					hiddenFileLines += 1
			else:
					f.write("\n") # deletes previous content
			hiddenFileCounter += 1

	print("Wrote",hiddenFileCounter,".hidden file(s)")
	print(hiddenFileLines,"files and folders are now hidden")

	fapxileStatusFile.hiddenFapxiles = []
	for button in allButtons:
		if button.status == 1:
			fapxileStatusFile.hiddenFapxiles.append(button.fapxile)
			

	fapxileStatusFile.writeStatusFile()


	#for tag in tags:
	#	if len(tag.hidden) > 0:
	#		print("#############################################")
	#		print(tag.dir)
	#		print(tag.hidden)

	window.destroy()



##############################################################################################
#Main
##############################################################################################





# Build main Window
#-------------------

window = Tk()

window.title("fapel exiles manager")

window.minsize(400,400)
#window.maxsize(400,700)

window.configure(bg=FT_COLORS["window_background"])

#switchframe = Frame(window, bg=FT_COLORS["window_background"])
#myframe.pack(fill = BOTH)



myframe=Frame(window,relief=GROOVE)
myframe.pack(side = TOP, fill = BOTH, expand=YES)

canvas=Canvas(myframe,highlightthickness=0) 
canvas.configure(bg=FT_COLORS["window_background"])
switchframe = Frame(canvas, bg=FT_COLORS["window_background"])
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myframe.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all"),height=e.height))

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left", fill=BOTH, expand=YES)
canvas.create_window((0,0),window=switchframe,anchor='nw')








bottomframe = Frame(window, bg=FT_COLORS["window_background"])

saveButton = Button(bottomframe, text="Apply", command=clickApply, bg = FT_COLORS["button_apply"])
cancelButton = Button(bottomframe, text="Cancel", command=clickCancel, bg = FT_COLORS["button_cancel"])
saveButton.pack( side = RIGHT,padx=20,pady=3)
cancelButton.pack( side = RIGHT)

hideAllButton = Button(bottomframe, text="Hide all", command=clickHideAllButton, bg = FT_COLORS["button_showallbuttons"])
showAllButton = Button(bottomframe, text="Show all", command=clickShowAllButton, bg = FT_COLORS["button_showallbuttons"])
showAllButton.pack( side = LEFT)
hideAllButton.pack( side = LEFT)


bottomframe.pack(side = BOTTOM, fill = X)


# search all .exile files
# 1) all tags that result in an exile
# 2) all tags that themself will be hidden/exiled


tags = set()
tagnameTag = {}
parentTags = {}
ROOTTAG_KEY = "."
rootTag = Tag(ROOTTAG_KEY) 
rootTag.dir = rootpath
rootTag.shortname = "."
tags.add(rootTag)
parentTags[ROOTTAG_KEY] = rootTag

excludedSubDirs = []

fapxileFiles = []

for root,d_names,f_names in os.walk(rootpath):
	#print (root, d_names, f_names)

	traverseSubDirs = True
	for f_name in f_names:
		if (f_name == ".exclude_subdirs"):
			traverseSubDirs = False
			excludedSubDirs.append(root)
		if (f_name == ".fapxile"):
			fapxileFiles.append(os.path.join(root, f_name))




	for excludedSubDir in excludedSubDirs:
		if (root.find(excludedSubDir) != -1):
			traverseSubDirs = False

	if (traverseSubDirs):
		for d_name in d_names:
			if d_name not in excludedTagNames:
				# rootpath/GrandParenttag/Parenttag/Tag
				# '---------root-----------------'  d_name
				# rootpath '---tagname-------------------'
				#		  '---dir-----------------------'
				#		  '------parenttag------'
				tagname = os.path.relpath(os.path.join(root, d_name), rootpath)
				tag = Tag(tagname)
				tagnameTag[tagname] = tag
				tag.shortname = d_name
				tag.dir = os.path.join(root, d_name)
				tags.add(tag)
				# Tree setup
				parenttag = os.path.relpath(root, rootpath)
				parentTags[tagname] = tag
				#   add as child
				parentTags[parenttag].addChild(tag)
				tag.hideChildButtons = parentTags[parenttag].hideChildButtons
				tag.hideButton = parentTags[parenttag].hideChildButtons

print("Found",len(tags),"Tag(s)")
print("Found",len(fapxileFiles),"fapxile file(s)")

allFapels = []
inodeFapels = {}


for tag in tags:
	

	for root, d_names, filenames in os.walk(tag.dir):
		#print (filenames)
		break

	#print(filenames)

	for filename in filenames:
		if filename.startswith("."):
			continue
		fapel = Fapel(os.path.join(tag.dir, filename))
		
		if fapel.inode not in inodeFapels:
			allFapels.append(fapel)
			inodeFapels[fapel.inode] = fapel

		inodeFapels[fapel.inode].tagFilenames[tag] = os.path.join(tag.dir, filename)
		inodeFapels[fapel.inode].tags.add(tag)
		#print("Fapel",inodeFapels[fapel.inode].inode,"now has",len(inodeFapels[fapel.inode].tags),"Tags")
		tag.allFapels.add(inodeFapels[fapel.inode])



print("Found",len(allFapels),"fapel(s)")



fapxileStatusFile = FapxileStatusFile(os.path.join(rootpath,"fapxile_status"))

print("hidden Fapxiles:",fapxileStatusFile.hiddenFapxiles)



fapxiles = []


for ff in fapxileFiles:
	fapxileFile = FapxileFile(ff)

	head, tail = os.path.split(ff)
	tagname = os.path.relpath(head, rootpath)
	#print(tagname)

	tag = tagnameTag[tagname]
	
	tag.hideFor = (list(set(tag.hideFor) | set(fapxileFile.fapxileForThisTag)))
	tag.hideFapelsFor = (list(set(tag.hideFapelsFor) | set(fapxileFile.fapxileForFapelsOfThisTag)))
	tag.hidesubFapelsFor = (list(set(tag.hidesubFapelsFor) | set(fapxileFile.fapxileForSubTagsAndSubFapels)))
	tag.excludedSubTags = fapxileFile.excludedSubTags

	fapxiles = (list(set(fapxiles) | set(fapxileFile.getAllFapxiles())))
	

fapxiles.sort()
print("Found Fapxiles:",fapxiles)



switchframe.columnconfigure(0, weight=3)
switchframe.columnconfigure(1, weight=1)

allButtons = []

row = 0
for fapxile in fapxiles:
	username_label = ttk.Label(switchframe, text=fapxile)
	username_label.grid(column=0, row=row, sticky=tk.W, padx=5, pady=5)

	toggle_button = FapxileButton(switchframe, fapxile)
	toggle_button.grid(column=1, row=row, sticky=tk.W, padx=5, pady=5)
	allButtons.append(toggle_button)

	if fapxile in fapxileStatusFile.hiddenFapxiles:
		toggle_button.clicked()

	row = row + 1

window.mainloop()

