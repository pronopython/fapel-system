With the fapel-system you can organize your images and video collection under Linux with standard folders. Everything works with hardlinks.

The fapel-system was created and is optimized for adult-oriented images, videos and movies. Fapel stands for "fap-able element" :-) If you are a passionate collector, this might be for you.

![](img/27173524.png)


Start now!

- [Installation](#installation)
- [First steps!](#usage)



# Comparison with other Systems
advantages over database based systems

* works with every file type, jpg, gif, mov, mp4,...
* backup compatible
* Survives itself (software not needed to browse categories, since these are normal folders)
* perfectly integrated into linux
* files can be renamed and moved (on the same drive) in any other program without problem
* everything is mouse only (one hand)
* fixed positions of buttons
* delete hardlinks without consequences


# Requirements

* Ubuntu Linux (all other linux systems might require you to install by hand)
    * ... with Nautilus file manager (should be standard)
* Python 3 with tkinter
* all folders and fapels must be on one logical drive because everything works with hardlinks


# Installation


## Clone or download this repo

Yes, clone or download this repo now!

## Install python tkinter

`sudo apt-get install python3-tk`

## Run install.sh

Run `install.sh` in `fapelsystem/`

You do need sudo for that.

If you are new then let the fapelsystem create the dirs (`y`). Otherwise you have to change the config file yourself (NOT recommended for new users!)


# Usage

## Starting fapel_tagger


Now go to the media you like and start tagging!

I have this collection of images of Jordan Carver, let's add some tags!

Rightclick to start the tagger

![](img/001.png)

This is the fapel_tagger! It presents all tags for you as buttons you can press to select or deselect a tag!

![](img/002.png)

There are almost no buttons... We are missing Tags! Let's create some!


## Create Tags

Go to

`~/fapelsystem/Tags/`

And just create directories and nested directories as you like! These are your Tags!

You can also delete directories (delete Tags) as you like.

## Add Tags to media


Back to the images, rightclick and start the fapel-tagger.

It will now automatically have all the tags you created (as directories). I have create a few:

![](img/003.png)

Click the buttons, they will turn red. Red tags are selected.

Click Apply Button

The image is now tagged!

## Browse Media in Tags

Go to the Tag folder, in my example

`~/fapelsystem/Tags/Models/All purpose/Jordan Carver/`

![](img/004.png)

There it is! The image was automatically hard-linked into the Tag folder!

## Tag multiple files


Of course you can tag more than one file in the go.

Just start the tagger with more files:

![](img/005.png)

Here the tagger noticed that one file is already tagged (the buttons are blue). Let's add all the other files to the tags except tag "Beauty":

![](img/006.png)


## Add a fav to a file ("notice a file")

Browsing through my collection, this shiny red image caught my attention:

![](img/007.png)

Rightclicking and running the fapel-notice script!

![](img/008.png)

This adds the image to the "notice dir":

![](img/009.png)

Which as you can see ("0001" sub dir) remembers how often I started the "notice script" on the image!

The image will automatically move the numbered folders up!

Running notice script again:

![](img/010.png)

![](img/011.png)

Now it is in the sub folder "0002".

## "Enjoy" a media file

So, notice script counts "events" you noticed some file. The same is true for the "ct" script, except it's purpose is to count how many times you "enjoyed" a file ;-)

Oh this beach wear image...

![](img/013.png)

So clean the mouse and run the ct script!

![](img/014.png)

Now run the tagger and see that the ct - counting directory is also present (Ct/Ct/0001)!

![](img/015.png)


This is important to know:

* The ct directory is inside the /Tags folder, the /Notice directory is outside. So you only see the ct hardlinked media!
* BUT You only see the ct and numbered dirs when a file was tagged! This is to prevent cluttering the tag button gui.

If you want to see all buttons, press the button in the bottom left corner.




# There is more

... but this readme is not done yet...




# Remarks
remember that hardlinks do point to the same binary data of a file, altering it in one place alters it everywhere!






