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
# TODO tkinter install: sudo apt-get install python3-tk
# TODO filename with "%" do not work (or is that a problem via nautilus UI parameter handling?)
# TODO you *can* select dirs directly and start the tagger with them... what happens next??? this is bad...
# TODO install tk:
# pip3 install tk
# sudo apt install python3.8-tk



from tkinter import *
from tkinter import ttk
import tkinter.font as font
import os
import sys
import configparser
import time




##############################################################################################
#Import lib
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
recycledPath = configParser.getDir('dirs','recycledDir')
print("recycledDir",recycledPath)

# load to be excluded tag names (=dirs)
excludedTagNames = []
for item in configParser.items('excludedTagNames'):
	excludedTagNames.append(item[0])
print("Excluded Tag names:",excludedTagNames)

# load colors
FT_COLORS = {}
for item in configParser.items('colors'):
	FT_COLORS[item[0]]=item[1]
#print(FT_COLORS)

# load tooltip stuff
TOOLTIP_WAITTIME = int(configParser.get('tooltip','waittime'))
TOOLTIP_WIDTH = int(configParser.get('tooltip','width'))



##############################################################################################
#Classes
##############################################################################################


class CreateToolTip(object):
	global FT_COLORS
	global TOOLTIP_WAITTIME
	global TOOLTIP_WIDTH
	
	# create a tooltip for a given widget
	def __init__(self, widget, text='widget info'):
		self.waittime = TOOLTIP_WAITTIME	 #miliseconds
		self.wraplength = TOOLTIP_WIDTH   #pixels
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.leave)
		self.widget.bind("<ButtonPress>", self.leave)
		self.id = None
		self.tw = None

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.widget.after(self.waittime, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.widget.after_cancel(id)

	def showtip(self, event=None):
		x = y = 0
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + 25
		y += self.widget.winfo_rooty() + 20
		# creates a toplevel window
		self.tw = Toplevel(self.widget)
		# Leaves only the label and removes the app window
		self.tw.wm_overrideredirect(True)
		self.tw.wm_geometry("+%d+%d" % (x, y))
		label = Label(self.tw, text=self.text, justify='left',
					   background=FT_COLORS["tooltip_background"], fg=FT_COLORS["tooltip_foreground"], relief='solid', borderwidth=1,
					   wraplength = self.wraplength)
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tw
		self.tw= None
		if tw:
			tw.destroy()




class Tag:
	def __init__(self, name):
		self.name = name
		self.shortname = ""
		self.initialFapels = set()
		self.currentFapels = set()
		self.toBeRemovedFapels = set()
		self.allFapels = None
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

	def addChild(self, child):
		self.children.append(child)
		self.children = sorted(self.children, key=Tag.getTagShortName)
		child.parent = self
		child.depth = self.depth + 1

	# used as a comparator / key for sorting
	@staticmethod
	def getTagShortName(tag):
		return tag.shortname


class TagButton(Button):
	global FT_COLORS
	status: int

	def __init__(self, window, tag):
		self.tag = tag
		self.status = 0
		#width=20
		numberText = ""
		if (len(tag.initialFapels) > 1):
				numberText = " (" + str(len(tag.initialFapels)) + ")"
		super().__init__(window, text=tag.name+numberText, height=1, font=buttonFont, pady=0, padx=0)
		self.configure(command=self.clicked)
		self.updatestatus()
		self.updatecolor()


	def clicked(self):
		#print (len(self.tag.initialFapels), " ", len(self.tag.allFapels))
		if self.status == 0:
			if len(self.tag.initialFapels) == len(self.tag.allFapels):
				#self.status = 2
				self.tag.currentFapels.clear()
				self.tag.currentFapels.update(self.tag.allFapels)
				Fapel.addTagToAll(self.tag, self.tag.allFapels)
			elif len(self.tag.initialFapels) == 0:
				# self.status = 1
				self.tag.currentFapels.clear()
				self.tag.currentFapels.update(self.tag.allFapels)
				Fapel.addTagToAll(self.tag, self.tag.allFapels)
			elif len(self.tag.initialFapels) < len(self.tag.allFapels):
				#self.status = 1
				self.tag.currentFapels.clear()
				self.tag.currentFapels.update(self.tag.initialFapels)
				Fapel.removeTagFromAll(self.tag, self.tag.allFapels)
				Fapel.addTagToAll(self.tag, self.tag.initialFapels)
		elif self.status == 1:
			#self.status = 2
			self.tag.currentFapels.clear()
			self.tag.currentFapels.update(self.tag.allFapels)
			Fapel.addTagToAll(self.tag, self.tag.allFapels)
		elif self.status == 2:
			#self.status = 0
			self.tag.currentFapels.clear()
			Fapel.removeTagFromAll(self.tag, self.tag.allFapels)
		self.updatestatus()
		self.updatecolor()


	def updatecolor(self):
		if self.status == 0:
			self['bg'] = FT_COLORS["button_tag_unselected"]
		elif self.status == 1:
			self['bg'] = FT_COLORS["button_tag_partially"]
		elif self.status == 2:
			self['bg'] = FT_COLORS["button_tag_selected"]

	def updatestatus(self):
		if len(self.tag.currentFapels) == len(self.tag.allFapels):
			self.status = 2
		elif len(self.tag.currentFapels) == 0:
			self.status = 0
		else:
			self.status = 1

	# take second element for sort
	def comparator(button):
		return button["text"]


class Fapel:
	def __init__(self, fullpath):
		self.initialTags = set()
		self.newTags = set()
		self.toBeRemovedTags = set()
		self.fullPath = fullpath
		head, tail = os.path.split(self.fullPath)
		self.filename = tail
		self.tagFilenames = {} # {tag,filename within tag} dictionary

	@staticmethod
	def addTagToAll(tag, fapels):
		for fapel in fapels:
			if tag not in fapel.initialTags:
				if tag not in fapel.newTags:
					fapel.newTags.add(tag)
			if tag in fapel.toBeRemovedTags:
				fapel.toBeRemovedTags.remove(tag)

	@staticmethod
	def removeTagFromAll(tag, fapels):
		for fapel in fapels:
			if tag in fapel.initialTags:
				fapel.toBeRemovedTags.add(tag)
			if tag in fapel.newTags:
				fapel.newTags.remove(tag)

	def applyTagStructure(self):
		print ("")
		print ("applying tag changes")
		print ("--------------------")
		# NEW TAGS
		# newtags -> initialtags
		for tag in self.newTags:
			print ("Hardlinking ",self.filename," to Tag ",tag.name)
			# rename till it fits
			new_twin_name = self.filename
			destinationFilename = os.path.join(tag.dir, self.filename)
			while os.path.isfile(destinationFilename):
				# change filename
				f_name, f_ext = os.path.splitext(new_twin_name)
				new_twin_name = f_name + "_A" + f_ext  # TODO better renaming if doubled!
				destinationFilename = os.path.join(tag.dir, new_twin_name)

			os.link(self.fullPath, os.path.join(tag.dir, new_twin_name))
			self.initialTags.add(tag)
		self.newTags.clear()

		# count how many initial tags will be removed
		remainingTags = set()
		for tag in self.initialTags:
			if (tag not in self.toBeRemovedTags):
				remainingTags.add(tag)

		for tag in remainingTags:
			print("Tag ", tag.name, " will remain")

		# all tags will be removed, hardlink to .recycled Folder before deleting all other files
		if (len(remainingTags) == 0):
			print("all tags will be removed, hardlinking ",self.filename," to .recycled folder")
			new_twin_name = self.filename
			destinationFilename = os.path.join(recycledPath, self.filename)
			while os.path.isfile(destinationFilename):
				# change filename
				f_name, f_ext = os.path.splitext(new_twin_name)
				new_twin_name = f_name + "_A" + f_ext # TODO better renaming when existing
				destinationFilename = os.path.join(recycledPath, new_twin_name)
			os.link(self.fullPath, os.path.join(recycledPath, new_twin_name))




		for tag in self.toBeRemovedTags:
			print("Removing ", self.filename, " from Tag ", tag.name)
			tagFilenameToBeRemoved = self.tagFilenames[tag]
			print("tagFilename (full path):",tagFilenameToBeRemoved)
			if (os.path.isfile(tagFilenameToBeRemoved)): # last security check: not a dir, okay?
				print("	deleting file ", tagFilenameToBeRemoved)
				os.remove(tagFilenameToBeRemoved)



class FinderElement:
	def __init__(self, text):
		self.text = text
		self.depth = 0
		self.children = []
		self.parent = None
		self.listbox = None
		self.fg = "#FFFFFF"
		self.bg = "#000000"
		
	def addChild(self, child):
		self.children.append(child)
		child.parent = self
		child.depth = self.depth + 1

class Finder:
	def __init__(self, root, numberOfColumns):
		self.frames = []
		self.listboxes = []
		self.currentFinderElement = []
		
	   
		for c in range(numberOfColumns):
			finderColumnFrame = Frame(root, bg = FT_COLORS["window_tagbackground"])
			if c < numberOfColumns:
				finderColumnFrame.pack( side = 'left', fill = 'both' ,expand=1 )
			else:
				finderColumnFrame.pack( side = 'right', fill = 'both' ,expand=1 )
			self.frames.append(finderColumnFrame)
			
			lb = Listbox(finderColumnFrame, bg = FT_COLORS["window_tagbackground"], fg = "#FFFFFF")
			self.listboxes.append(lb)
			
			lb.bind("<<ListboxSelect>>", self.callbackHandleSelection)
			lb.bind("<Double-Button-1>", self.callbackHandleSelectionDoubleClick)
			
			lb.pack(side = LEFT,fill = BOTH ,expand=1 )

			scrollbar = Scrollbar(finderColumnFrame)
			scrollbar.pack(side = RIGHT, fill = BOTH)

			lb.config(yscrollcommand = scrollbar.set)
			scrollbar.config(command = lb.yview)
	
	def setButtonsForTags(self,buttonsForTags):
		self.buttonsForTags = buttonsForTags
	
	def clearAllListboxes(self):
		for lb in self.listboxes:
			lb.delete(0,END)
			
	def clearListboxesFrom(self,fromPosition):
		for position,lb in enumerate(self.listboxes):
			if position >= fromPosition:
				lb.delete(0,END)
		if fromPosition < len(self.currentFinderElement):
			for c in range(len(self.currentFinderElement) - fromPosition ):
				self.currentFinderElement.pop()
	

	def callbackHandleSelectionDoubleClick(self, event):
		self.callbackHandleSelection(event=event, doubleClick=True)
	
	def callbackHandleSelection(self, event, doubleClick=False):
		selection = event.widget.curselection()
		if selection:
			index = selection[0]
			print("Selection pos:",index)
			print("DoubleClick:",doubleClick)
			data = event.widget.get(index)
			#print(data)
			#print(event.widget)
			clickedColumnNumber = -1
			for position, lb in enumerate(self.listboxes):
				if lb == event.widget:
					print("",position)
					clickedColumnNumber = position
			print("Clicked column",clickedColumnNumber)
			print("	Column generated from ",self.currentFinderElement[clickedColumnNumber].shortname)
			print("	No of Entries=List elements ",len(self.currentFinderElement[clickedColumnNumber].children))



			if doubleClick:
				element = self.currentFinderElement[clickedColumnNumber].children[index]
				button = self.buttonsForTags[element]
				button.clicked()
				
				self.listboxes[clickedColumnNumber].itemconfig(index, bg=self.getColorForListElement(element), fg=element.fg)


				self.listboxes[clickedColumnNumber].selection_clear(0, 'end')


			else:
				self.clearListboxesFrom(clickedColumnNumber+1)
				for position,element in enumerate(self.currentFinderElement[clickedColumnNumber].children[index].children):
					if (len(element.children) > 0):
						self.listboxes[ clickedColumnNumber + 1 ].insert("end", element.shortname + u" \u2192")
					else:
						self.listboxes[ clickedColumnNumber + 1 ].insert("end", element.shortname)
					self.listboxes[ clickedColumnNumber + 1 ].itemconfig(position, bg=self.getColorForListElement(element), fg=element.fg)
				self.currentFinderElement.append(self.currentFinderElement[clickedColumnNumber].children[index])

	def getColorForListElement(self, tag):
		if len(tag.currentFapels) == len(tag.allFapels):
			return FT_COLORS["finder_tag_selected"]
		elif len(tag.currentFapels) == 0:
			return FT_COLORS["finder_tag_unselected"]
		else:
			return FT_COLORS["finder_tag_partially"]


	# initially fill the first finder column	
	def loadFinderElements(self, rootElement):
		self.rootElement = rootElement
		self.clearAllListboxes()
		for position,element in enumerate(rootElement.children):
			if (len(element.children) > 0):
				self.listboxes[0].insert("end", element.shortname + u" \u2192")
			else:
				self.listboxes[0].insert("end", element.shortname)
			self.listboxes[0].itemconfig(position, bg=self.getColorForListElement(element), fg=element.fg)



		self.currentFinderElement = []
		self.currentFinderElement.append(rootElement)
		
	

##############################################################################################
#Main
##############################################################################################





# Build main Window
#-------------------

window = Tk()

window.title("fapel tagger")

if (configParser.get('window','fixedOrMinSize') == "fixed"):
	window.geometry(configParser.get('window','width')+"x"+configParser.get('window','height'))
else:
	window.minsize(configParser.get('window','width'), configParser.get('window','height'))

bottomframe = Frame(window, bg=FT_COLORS["window_background"])
bottomframe.pack( side = BOTTOM, fill = X )


style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
		"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] , "background": FT_COLORS["tabs_background"]} },
		"TNotebook.Tab": {"configure": {"padding": [50, 2],"background": FT_COLORS["tabs_unselected"] },
						  "map":{"background": [("selected", FT_COLORS["tabs_selected"])],
								 "expand": [("selected", [1, 1, 1, 0])] }}})

style.theme_use("MyStyle")


tabControl = ttk.Notebook(window)


tagframe = Frame(tabControl,bg=FT_COLORS["window_tagbackground"])
tabControl.add(tagframe, text = 'Tags')

finderframe = Frame(tabControl,bg=FT_COLORS["window_tagbackground"])


myFinder = Finder(finderframe,4)


tabControl.add(finderframe, text = 'Finder')

tabControl.pack( side = TOP, fill = BOTH ,expand=1 )





buttonFont = font.Font(family=configParser.get('fonts','tagFontFamily'), size=int(configParser.get('fonts','tagFontSize')))

progressbar = ttk.Progressbar(bottomframe, orient='horizontal', mode='determinate', length=280)

progressbar.pack( side = LEFT)

progresslabel = ttk.Label(bottomframe, text="")
progresslabel['background']=FT_COLORS["progressbar_background"]
progresslabel['foreground']=FT_COLORS["progressbar"]
progressbar.pack( side = LEFT,padx=20,pady=3)
progresslabel.pack( side = LEFT )

progressbar.update_idletasks()
progressbar.update()




# Create Fapels from Argument
#-----------------------------

fapels = set()

# first arg is name of script
arguments = len(sys.argv) - 1
print("Number of given files from command line:",arguments)
position = 1
while (arguments >= position):
	fapels.add(Fapel(sys.argv[position]))
	position = position + 1


progressbar['value'] = 20
progresslabel['text'] = "Loading Tags"
window.update_idletasks()
window.update()
progressbar.update_idletasks()
progressbar.update()





# Create Tags from Dirs
#-----------------------

tags = set()
parentTags = {}
ROOTTAG_KEY = "."
rootTag = Tag(ROOTTAG_KEY) 
parentTags[ROOTTAG_KEY] = rootTag

excludedSubDirs = []

for root,d_names,f_names in os.walk(rootpath):
	#print (root, d_names, f_names)

	traverseSubDirs = True
	for f_name in f_names:
		if (f_name == ".exclude_subdirs"):
			traverseSubDirs = False
			excludedSubDirs.append(root)

		if (f_name == ".hide_button"):
			parenttag = os.path.relpath(root, rootpath)
			parentTags[parenttag].hideButton = True

		if (f_name == ".hide_child_buttons"):
			parenttag = os.path.relpath(root, rootpath)
			parentTags[parenttag].hideChildButtons = True


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

	

#myFinder.loadFinderElements(rootTag)


progressbar['value'] = 40
window.update_idletasks()
window.update()
progressbar.update_idletasks()
progressbar.update()

# match tags with fapels
#------------------------

tagCount = len(tags)
currentTagNumber = 0

# remember inodes for speedup
known_fapel_inodes = {}
known_tagfile_inodes = {}



for tag in tags:
	#(_, _, filenames) = next(os.walk(tag.dir))
	#print (tag.name,"  ",tag.dir)
	#_, _, filenames = next(os.walk(tag.dir), (None, None, []))

	currentTagNumber = currentTagNumber + 1


	progressbar['value'] = 40 + (40 * currentTagNumber/tagCount)
	window.update_idletasks()
	window.update()
	progressbar.update_idletasks()
	progressbar.update()
	progresslabel['text'] = "Analyzing Fapels for Tag: " + tag.name

	tag.allFapels = fapels

	filenames = []

	for root, d_names, filenames in os.walk(tag.dir):
		#print (filenames)
		break


	for fapel in fapels:
		if fapel.fullPath in known_fapel_inodes:
			inode_fapel = known_fapel_inodes[fapel.fullPath]
		else:
			inode_fapel = os.stat(fapel.fullPath).st_ino
			known_fapel_inodes[fapel.fullPath] = inode_fapel
		for f_name in filenames:
			#print (fapel.filename,"--" ,f_name )
			f_name_fullPath = os.path.join(tag.dir,f_name)
			
			if f_name_fullPath in known_tagfile_inodes:
				inode_f_name = known_tagfile_inodes[f_name_fullPath]
			else:
				inode_f_name = os.stat(f_name_fullPath).st_ino
				known_tagfile_inodes[f_name_fullPath] = inode_f_name
			

		#if fapel.filename == f_name:
			if inode_fapel == inode_f_name:
				#match
				fapel.initialTags.add(tag)
				tag.initialFapels.add(fapel)
				tag.currentFapels.add(fapel)
				
				print (fapel.filename," found in ",tag.name, " as file ",f_name_fullPath)
				fapel.tagFilenames[tag] = f_name_fullPath

	if (os.path.isfile(os.path.join(tag.dir,".taginfo"))):
		configParserTT = configparser.RawConfigParser()
		configParserTT.read(os.path.join(tag.dir,".taginfo"))
		tag.tooltip = configParserTT.get('general','tooltip')
		



progressbar['value'] = 80
progresslabel['text'] = "Creating buttons and finder"
window.update_idletasks()
window.update()
progressbar.update_idletasks()
progressbar.update()


print("Creating finder entries")
myFinder.loadFinderElements(rootTag)



# create buttons
#----------------

buttons = set()
buttonsForTags = {}

for tag in tags:
	button = TagButton(tagframe, tag)
	if (tag.tooltip != ""):
		button_ttp = CreateToolTip(button,tag.tooltip)
	buttons.add(button)
	buttonsForTags[tag] = button

# sort list with key
buttons = sorted(buttons, key=TagButton.comparator)
myFinder.setButtonsForTags(buttonsForTags)


# remove all additional buttons from showing up:
# - button is not enabled AND
# - tag has button=none
# - tag has childrenbutton=none

displayedButtons = set()
for button in buttons:
	if (not button.tag.hideButton) or (button.status > 0):
		displayedButtons.add(button)
displayedButtons = sorted(displayedButtons, key=TagButton.comparator)


# arrange buttons


x = 0
y = 0
maxy = int(configParser.get('window','buttonsPerColumn'))
for button in displayedButtons:
	button.grid(column=x, row=y)
	y = y + 1
	if y == maxy:
		y = 0
		x = x + 1


progressbar['value'] = 90
progresslabel['text'] = "Almost done..."
window.update_idletasks()
window.update()
progressbar.update_idletasks()
progressbar.update()

# functional buttons

def clickApply():
	for fapel in fapels:
		fapel.applyTagStructure()
	window.destroy()

def clickCancel():
	window.destroy()


def clickShowAllButtons():
	x = 0
	y = 0
	maxy = int(configParser.get('window','buttonsPerColumn'))
	for button in buttons:
		button.grid(column=x, row=y)
		y = y + 1
		if y == maxy:
			y = 0
			x = x + 1
	showAllButtonsButton["state"] = "disabled"
	window.update_idletasks()
	window.update()


saveButton = Button(bottomframe, text="Apply", command=clickApply, bg = FT_COLORS["button_apply"])
showAllButtonsButton = Button(bottomframe, text="Show all buttons", command=clickShowAllButtons, bg = FT_COLORS["button_showallbuttons"])
cancelButton = Button(bottomframe, text="Cancel", command=clickCancel, bg = FT_COLORS["button_cancel"])
saveButton.pack( side = RIGHT,padx=20,pady=3)
cancelButton.pack( side = RIGHT)
showAllButtonsButton.pack( side = LEFT)


progressbar['value'] = 100
window.update_idletasks()
window.update()
progressbar.update_idletasks()
progressbar.update()

progresslabel.pack_forget()
progressbar.pack_forget()


window.mainloop()
