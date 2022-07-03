#!/usr/bin/env python3
#
##############################################################################################
#
# The fapel system organizes image and video collections under Linux with standard folders.
# fappel_elo is a GUI based ranking application for all fapels / media in the tag folder
# system.
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
#
# TODO random from dirs
# TODO install Pillow  ;; pip3 install Pillow ;; sudo apt-get install python3-pil.imagetk
# TODO cleanup: delete last 20%
# TODO not interested in left => eloignoredpath
# TODO not interested in right => eloignoredpath
# TODO rightclick bei leftmode only => do you want to swtich??


from tkinter import messagebox
from tkinter import *
import os
import sys
import random
from PIL import Image, ImageTk
import configparser


##############################################################################################
#Load Config
##############################################################################################



sys.path.insert(0, INSTALLDIR)
from fapelsystemlib import fapelSystemConfig
from fapelsystemlib import dirHelper


configParser = fapelSystemConfig.FapelSystemConfig()



# load to be excluded tag names (=dirs)
excludedTagNames = []
for item in configParser.items('excludedTagNames'):
    excludedTagNames.append(item[0])
print("Excluded Tag names:",excludedTagNames)


##############################################################################################
#Init Vars
##############################################################################################



rootpath = configParser.getDir('dirs','tagDir')
print("tagDir",rootpath)

elopath = configParser.getDir('dirs','eloDir')
print("eloDir",elopath)


#eloignoredpath = configParser.getDir('dirs','eloIgnoredDir')
#print("eloIgnoredDir",eloignoredpath)

MIN_ELO_RANK = 100000000000000000
MAX_ELO_RANK = 999999999999999999


FT_COLORS = {}
for item in configParser.items('colors'):
    FT_COLORS[item[0]]=item[1]

TEXT_MOUSE=("Mouse Mode: Left only","Mouse Mode: Left + Right")


##############################################################################################
#Classes
##############################################################################################




class FapelLabel(Label):
#    status: int

    global FT_COLORS
    original: Image
    def __init__(self, window, image):
        self.original = image

        super().__init__(window,  bg=FT_COLORS["fapel_background"])

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = image
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0, bg=FT_COLORS["fapel_background"])
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize)


    def resize(self, event):

        if self.original.width/self.original.height > self.winfo_width()/self.winfo_height():
           size = (int(self.winfo_width()), int((self.winfo_width()*self.original.height)/self.original.width))     
        else:
           size = (int((self.original.width*self.winfo_height())/self.original.height), int(self.winfo_height())) 



        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")



    def setAlpha(self, alphaValue):
        self.original.putalpha(alphaValue)
        self.event_generate("<Configure>")

    def setImage(self, image):
        self.original = image
        self.event_generate("<Configure>")






class Fapel:
    def __init__(self, fullpath, elopath, inode):
        self.fullPath = fullpath
        self.inode = inode
        head, tail = os.path.split(self.fullPath)
        self.filename = tail
        self.eloDirFullPath = ""
        self.elo = -1 # no ranking yet (=-1)
        self.elopath = elopath
        self.extension = os.path.splitext(self.fullPath)[1]

    def updateElo(self):
        if (self.eloDirFullPath == ""): # fapel not ranked yet, hardlink it now
            self.eloDirFullPath = os.path.join(self.elopath, str(self.elo)+self.extension)
            os.link(self.fullPath, self.eloDirFullPath)
        else:
            newName = os.path.join(self.elopath, str(self.elo)+self.extension)
            #print("RENAME:",self.eloDirFullPath,"==>",newName)
            os.rename(self.eloDirFullPath, newName)
            self.eloDirFullPath = newName
            self.fullPath = newName
    def changeToTempName(self):  # is used while defrag runs, so that nothing is overwritten
        if (self.eloDirFullPath != ""):
            newName = os.path.join(self.elopath, "TEMP_"+str(self.elo)+self.extension)
            #print("RENAME:",self.eloDirFullPath,"==>",newName)
            os.rename(self.eloDirFullPath, newName)
            self.eloDirFullPath = newName
            self.fullPath = newName

class CurrentFapels:
    #self.leftLabel: FapelLabel
    #self.rigthtLabel: FapelLabel

    global MIN_ELO_RANK
    global MAX_ELO_RANK

    PROBABILITY_TAKE_FROM_RANKED = 0.8

    useBothMouseButtons = True
    clicksUntilChange = 3
    leftClicks = 0
    rightClicks = 0

    def __init__(self, allFapels, rankedFapels):
        self.allFapels = allFapels
        self.rankedFapels = rankedFapels
        self.sortFapels()
        self.shuffle()

    def sortFapels(self):
        self.rankedFapels.sort(key=self.comparator)


    def comparator(self, fapel):
        return fapel.elo


    def shuffle(self):
        #print("Shuffling..")
        
        if (len(self.rankedFapels) == 0):  # if you first start elo with no ranked fapels
            self.choiceLeft = random.choice(self.allFapels)
        else:
            self.choiceLeft = random.choice(self.rankedFapels)
        self.choiceRight = self.choiceLeft
        while (self.choiceLeft == self.choiceRight):
            if (random.random() < self.PROBABILITY_TAKE_FROM_RANKED) and (len(self.rankedFapels) > 0):
                self.choiceRight = random.choice(self.rankedFapels)
            else:
                self.choiceRight = random.choice(self.allFapels)



    def setFapelLabels(self, leftLabel, rightLabel):
        self.leftLabel = leftLabel
        self.rightLabel = rightLabel



    def mouseLeftOnLeft(self, event=None):
        if (self.useBothMouseButtons):
            self.clickLeft()
        else:
            self.clickLeft()

    def mouseRightOnLeft(self, event=None):
        if (self.useBothMouseButtons):
            self.clickRight()
        else:
            self.clickLeft()

    def mouseLeftOnRight(self, event=None):
        if (self.useBothMouseButtons):
            self.clickLeft()
        else:
            self.clickRight()

    def mouseRightOnRight(self, event=None):
        if (self.useBothMouseButtons):
            self.clickRight()
        else:
            self.clickRight()

    def toggleMouseMode(self):
        if (self.useBothMouseButtons):
            self.toggleButton['text'] = TEXT_MOUSE[0]
            self.useBothMouseButtons=False
        else:
            self.toggleButton['text'] = TEXT_MOUSE[1]
            self.useBothMouseButtons=True
            
    def setToggleButton(self, toggleButton):
        self.toggleButton = toggleButton


    def clickLeft(self, event=None):
        # `command=` calls function without argument
         # `bind` calls function with one argument
        #print("fapel left clicked")
        
        self.leftClicks = self.leftClicks + 1
        self.rightClicks = 0
        if (self.leftClicks >= self.clicksUntilChange):
            self.rankFapelWinnerLooser(self.choiceLeft,self.choiceRight)
            self.shuffle()
            image = Image.open(self.choiceLeft.fullPath)
            self.leftLabel.setImage(image)
            image = Image.open(self.choiceRight.fullPath)
            self.rightLabel.setImage(image)
            self.leftClicks = 0
            self.rightClicks = 0
        else:
            self.leftLabel.setAlpha(255)
            self.rightLabel.setAlpha(int(255-((255/self.clicksUntilChange)*self.leftClicks)))
            


    def clickRight(self, event=None):
        # `command=` calls function without argument
         # `bind` calls function with one argument
        #print("fapel right clicked")

        self.leftClicks = 0
        self.rightClicks = self.rightClicks + 1
        if (self.rightClicks >= self.clicksUntilChange):
            self.rankFapelWinnerLooser(self.choiceRight,self.choiceLeft)
            self.shuffle()
            image = Image.open(self.choiceLeft.fullPath)
            self.leftLabel.setImage(image)
            image = Image.open(self.choiceRight.fullPath)
            self.rightLabel.setImage(image)
            self.leftClicks = 0
            self.rightClicks = 0
        else:
            self.leftLabel.setAlpha(int(255-((255/self.clicksUntilChange)*self.rightClicks)))
            self.rightLabel.setAlpha(255)
        

    def defragmentAllElos(self):
        print("Defragmenting Elos... might take a while")
        
        messagebox.showinfo("Defragmentation needed", "About to defragment all elo filenames, this might take a while and app seems unresponsive. Do not abort this process!")
        
        spaceBetweenElos = int((MAX_ELO_RANK - MIN_ELO_RANK) / (len(self.rankedFapels) + 1))

        self.sortFapels()
        currentEloNumber = MIN_ELO_RANK + spaceBetweenElos
        for fapel in self.rankedFapels:
            fapel.elo = currentEloNumber
            currentEloNumber = currentEloNumber + spaceBetweenElos
        self.sortFapels()
        print("...renaming all ranked Fapels...")
        for fapel in self.rankedFapels:
            fapel.changeToTempName()
        for fapel in self.rankedFapels:
            fapel.updateElo()
        messagebox.showinfo("Defragmentation", "Defragmentation finished!")

    def getEloRankedOneHigher(self, fapel):
        eloLeft = MIN_ELO_RANK
        for fapelLeft in self.rankedFapels:
            if fapelLeft.elo >= fapel.elo:
                break;
            else:
                eloLeft = fapelLeft.elo
        return eloLeft

    def getFittingElo(self, fapelLooser):
        # find the LEFT neighbour of fapelLooser
        eloLeft = self.getEloRankedOneHigher(fapelLooser)
        if ((fapelLooser.elo - eloLeft) < 3):
            self.defragmentAllElos()
            eloLeft = self.getEloRankedOneHigher(fapelLooser)
            if ((fapelLooser.elo - eloLeft) < 3): # still too close?
                print("elos to close together, too many elos, giving up... panic") 
                exit();
        return random.randint(eloLeft + 1, fapelLooser.elo - 1)

    def rankFapelWinnerLooser(self, fapelWinner, fapelLooser):
        
        # [no elo] wins over [no elo]   -> only one time when no ranked fapel exists

        if ((fapelWinner.elo == -1) and (fapelLooser.elo == -1)):
            print("First fapel ranked")
            fapelWinner.elo = MAX_ELO_RANK
            fapelWinner.updateElo()
            self.rankedFapels.append(fapelWinner)
            self.sortFapels()

        # [ELO] wins over [no elo]            
        elif ((fapelWinner.elo > -1) and (fapelLooser.elo == -1)):  # TODO remove thisone
            # nothing to do?!
            xyz = 1
        # [no elo] wins over [ELO]
        elif ((fapelWinner.elo == -1) and (fapelLooser.elo > -1)):
            newElo = self.getFittingElo(fapelLooser)
            fapelWinner.elo = newElo
            self.rankedFapels.append(fapelWinner)
            fapelWinner.updateElo()
            self.sortFapels()

        # [ELO] wins over [ELO] AND winner.elo > looser.elo
        elif ((fapelWinner.elo > -1) and (fapelLooser.elo > -1)):
            # only, when winner is not already ranked better
            if (fapelWinner.elo > fapelLooser.elo):
                newElo = self.getFittingElo(fapelLooser)
                fapelWinner.elo = newElo
                #if (fapelWinner not in rankedFapels):
                #    self.rankedFapels.append(fapelWinner)
                fapelWinner.updateElo()
                self.sortFapels()
        



# --- main ---

# init    
tinkerRoot = Tk()

tinkerRoot['bg'] = bg=FT_COLORS["window_background"]
fapelframe = Frame(tinkerRoot, bg=FT_COLORS["window_background"])

tinkerRoot.title("fapel elo")

inodeToFapel = {} # dictionary
allFapels = []
rankedFapels = []
WORKING_EXTENSIONS = [".jpg",".jpeg",".tif",".tiff",".png",".gif"]

excludedSubDirs = []

# create Fapels of all Elements inside Tags Dir
for root,d_names,f_names in os.walk(rootpath):
    traverseDir = True
    for excludedSubDir in excludedSubDirs:
        if (root.find(excludedSubDir) != -1):
            traverseDir = False

    for excludedTagName in excludedTagNames:
        if (root.find(excludedTagName) != -1):
            traverseDir = False
        
    if (traverseDir):
        for f_name in f_names:
            if (f_name == ".exclude_subdirs"):
                excludedSubDirs.append(root)
            else:
                f_fullPath = os.path.join(root, f_name)
                f_nameOnly, f_ext = os.path.splitext(f_name)
                if (f_ext.lower() in WORKING_EXTENSIONS):
                    inode = os.stat(f_fullPath).st_ino
                    if (inode not in inodeToFapel):
                        fapel = Fapel(f_fullPath, elopath, inode)
                        inodeToFapel[inode] = fapel
                        allFapels.append(fapel)

print("Found",len(inodeToFapel), "individual fapels in Tags")


# create Fapels of all Elements inside Elo Dir (if not already created before), and get their rank
for root,d_names,f_names in os.walk(elopath):
    for f_name in f_names:
        f_fullPath = os.path.join(root, f_name)
        inode = os.stat(f_fullPath).st_ino

        if (inode in inodeToFapel):           # fapel is known
            fapel = inodeToFapel[inode]

        else:                                 # fapel is new
            fapel = Fapel(f_fullPath, elopath, inode)
            inodeToFapel[inode] = fapel
            allFapels.append(fapel)
        fapel.eloDirFullPath = f_fullPath
        f_name_eloNumber, f_ext = os.path.splitext(f_name)
        fapel.elo = int(f_name_eloNumber)
        rankedFapels.append(fapel)
        #print("Fapel ",fapel.filename," ranked ",fapel.elo)        

print("Found",len(rankedFapels), "ranked fapels in Elo")




currentFapels = CurrentFapels(allFapels, rankedFapels)



# load image
image = Image.open(currentFapels.choiceLeft.fullPath)
image2 = Image.open(currentFapels.choiceRight.fullPath)


# label with image
l = FapelLabel(fapelframe, image=image)
#l.grid(row=0, column=0)
l.pack(side = LEFT,  fill = BOTH ,expand=1 )
l.display.bind('<Button-1>', currentFapels.mouseLeftOnLeft)
l.display.bind('<Button-3>', currentFapels.mouseRightOnLeft)

m = FapelLabel(fapelframe, image=image2)
#m.grid(row=0, column=1)
m.pack(side = RIGHT,  fill = BOTH ,expand=1 )
m.display.bind('<Button-1>', currentFapels.mouseLeftOnRight)
m.display.bind('<Button-3>', currentFapels.mouseRightOnRight)

currentFapels.setFapelLabels(l,m)

fapelframe.pack(side = TOP, fill = BOTH ,expand=1 )


buttonframe = Frame(tinkerRoot, bg=FT_COLORS["window_background"])


b = Button(buttonframe, text=TEXT_MOUSE[1], command=currentFapels.toggleMouseMode, bg=FT_COLORS["button_cancel"])
currentFapels.setToggleButton(b)
b.pack(side='left')

# button with text closing window
t = Button(buttonframe, text="Exit", command=tinkerRoot.destroy, bg=FT_COLORS["button_cancel"])
t.pack(side='right')


buttonframe.pack(side = BOTTOM)



# "start the engine"
tinkerRoot.mainloop()
