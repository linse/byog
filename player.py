#!/usr/bin/python
#
# The Python Imaging Library
# $Id$
#

from Tkinter import *
from PIL import Image, ImageTk
import sys

Image.DEBUG = 0


# --------------------------------------------------------------------

def applet_hook(animation, images):
    app = animation(animation_display, images)
    app.run()

class AppletDisplay:
    def __init__(self, ui):
        self.__ui = ui
    def paste(self, im, bbox):
        self.__ui.image.paste(im, bbox)
    def update(self):
        self.__ui.update_idletasks()

# --------------------------------------------------------------------
# an image animation player

class UI(Label):

    def __init__(self, master, ims):
        self.ims = ims
        # no images to display
        if len(ims)==0:
          return
        self.im = ims[0]
        self.ims.pop(0)

        if im.mode == "1":
            self.image = ImageTk.BitmapImage(im, foreground="white")
        else:
            self.image = ImageTk.PhotoImage(im)

        # APPLET SUPPORT (very crude, and not 100% safe)
        global animation_display
        animation_display = AppletDisplay(self)

        Label.__init__(self, master, image=self.image, bg="black", bd=0)

        self.update()

        try:
            duration = im.info["duration"]
        except KeyError:
            duration = 100
        self.after(duration, self.next)

    # go to next frame or pic
    def next(self):

        if type(self.im) == type([]):
                return # end of list

        else:
            try:
                # next frame
        				im = self.im
        				im.seek(im.tell() + 1)
        				self.image.paste(im)
            except EOFError:
                self.nextPic('turn.gif')

        try:
            duration = im.info["duration"]
        except KeyError:
            duration = 100
        self.after(duration, self.next)

        self.update_idletasks()

    def nextFrame(self):
        im = self.im
        im.seek(im.tell() + 1)
        self.image.paste(im)

    def nextPic(self,filename):
        im = Image.open(filename)
        self.im = im
        self.image.paste(im)

    def end(self):
        sys.exit(0)

    def loop(self):
        im = self.im
        im.seek(0)
        self.image.paste(im)

# ------------------------
# key and mouse events

def key(event):
    frame.focus_set()
    if event.char=='y':
      print "Yay"
    elif event.char=='n':
      print "Nay"
    else:
      print "Press y(ay) or n(ay)!"
      print "pressed", repr(event.char)

def callback(event):
    frame.focus_set()
    #print "clicked at", event.x, event.y

# --------------------------------------------------------------------
# script interface

if __name__ == "__main__":

    if not sys.argv[1:]:
        print "Syntax: python player.py imagefile"
        sys.exit(1)

    filename = sys.argv[1]
    root = Tk()
    # remove borders - removes also resizing
    #root.overrideredirect(1)
    root.title(filename)

    # enqueue further images
    if len(sys.argv) > 2:
        print "can just play one for now"
    ims = []
    for file in sys.argv[1:]:
      ims.append(Image.open(file))
    # open the first image
    im = Image.open(filename)
    frame = UI(root, ims)
    frame.bind("<Key>", key)
    frame.bind("<Button-1>", callback)
    frame.pack()
    root.mainloop()
