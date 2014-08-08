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

    def __init__(self, master, im):
        if type(im) == type([]):
            # list of images
            self.im = im[1:]
            im = self.im[0]
        else:
            # sequence
            self.im = im

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

    # go to next frame
    def next(self):

        if type(self.im) == type([]):
                return # end of list

        else:

            try:
                im = self.im
                im.seek(im.tell() + 1)
                self.image.paste(im)
            except EOFError:
                #self.end()
                self.loop()
                # end of file

        try:
            duration = im.info["duration"]
        except KeyError:
            duration = 100
        self.after(duration, self.next)

        self.update_idletasks()

    def end(self):
        sys.exit(0)

    def loop(self):
        im = self.im
        im.seek(0)
        self.image.paste(im)

# --------------------------------------------------------------------
# script interface

if __name__ == "__main__":

    if not sys.argv[1:]:
        print "Syntax: python player.py imagefile"
        sys.exit(1)

    filename = sys.argv[1]
    root = Tk()
    root.title(filename)

    # for 2 gifs it is not working!
    if len(sys.argv) > 2:
        print "can just play one for now"
    else:
        # sequence
        im = Image.open(filename)

    UI(root, im).pack()
    root.mainloop()
