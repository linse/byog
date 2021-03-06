#!/usr/bin/python

from __future__ import division
from Tkinter import *
from PIL import Image, ImageTk
from numpy import *
import sys
import numpy

Image.DEBUG = 0
# loop image list forever
eternalloop = True

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

    def __init__(self, master, ims, probs):
        self.ims = ims # image queue
        self.probs = probs # choice probabilities
        self.nr = 0 # image number
        self.backwards = False
        self.pause = False
        self.speed = 1.0
        # no images to display
        if len(ims)==0:
          return
        # im is just the image file opened
        self.im = Image.open(ims[self.nr])
        # image is the actual image object
        if self.im.mode == "1":
            self.image = ImageTk.BitmapImage(self.im, foreground="white")
        else:
            self.image = ImageTk.PhotoImage(self.im)

        # APPLET SUPPORT (very crude, and not 100% safe)
        global animation_display
        animation_display = AppletDisplay(self)

        Label.__init__(self, master, image=self.image, bg="black", bd=0, width=800, height=600)

        self.update()

        try:
            duration = self.im.info["duration"]
        except KeyError:
            duration = 100
        self.after(int(self.speed*duration), self.next)

    # go to next frame or pic
    def next(self):

      self.end
      if self.pause:
      	return
      else:
        try:
				 		# next frame
				 		im = self.im
				 		frameNr = im.tell()
				 		#print im.tell()
				 		if self.backwards:
				 			if frameNr == 0:
                # prevPic does now work yet, so we just go forwards again
								self.backwards = not self.backwards
				 			# mimick backwards seeking with a loop
				 			if frameNr > 0:
				 				im.seek(0)
				 				for i in xrange(0,frameNr-1):
				 				  im.seek(im.tell() + 1)
				 		else:
				 			im.seek(frameNr + 1)
				 		self.image.paste(im)
        except EOFError:
             # 50:50 chance for 0 or 1
             draw = random.randint(0,2)
             if draw == 1:
               # take same pic as we have
               self.choosePic(self.nr)
             else:
               # change it
               self.weightedNextPic()

        try:
            duration = im.info["duration"]
        except KeyError:
            duration = 100
        self.after(int(self.speed*duration), self.next)

        self.update_idletasks()

        # TODO four loop modes: run image and finish, run image forever, run image n times, run image n seconds
        # self.repeatOne
        # self.repeatedTimes
        # self.repeatTimes
        # self.repeatTimespan

    #def checkPic(self):

    def nextPic(self):
        self.choosePic(self.nr + 1)

    def weightedNextPic(self):
        minval = min(self.probs)
        positive = self.probs
        # shift all votes to being positive
        # pseudocount of 1 so no probability will be 0
        if minval < 0:
          positive = [ x-minval+1 for x in positive]
        else:
          positive = [ x+1 for x in positive]
        # normalize so we have probabilities
        completesum = sum(positive)
        percentages = positive
        if completesum > 0:
          percentages = [ x / completesum for x in positive ]
        # draw from the urn of pics :D
        indices = [ c for c,i in enumerate(percentages) ]
        nextPicNr = random.choice(indices, p=percentages)
        self.choosePic(nextPicNr)

    def choosePic(self,number):
 				self.nr = number
        # if no more pics in queue, quit or loop
				if self.nr >= len(self.ims):
					if eternalloop:
						self.nr = 0
					else:
						self.end()
				self.im = Image.open(self.ims[self.nr])
				self.im.seek(0)
				if self.im.mode == "1":
				    self.image = ImageTk.BitmapImage(im, foreground="white")
				else:
				    self.image = ImageTk.PhotoImage(self.im)
				self.configure(image = self.image)

    # does not work properly
    def prevPic(self):
				print 'lower pic number to'
 				self.nr = self.nr - 1
        # if no more pics in queue, quit
				if self.nr < 0:
					if eternalloop:
						self.nr = len(self.ims) - 1
					else:
						self.end()
				print "nr",self.nr
				im = self.ims[self.nr]
        # TODO seek last frame is faulty
				im.seek(0)
				try: 
					while True:
				 		im.seek(im.tell() + 1)
				except EOFError:
					print "reached the last frame which is ",im.tell()
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
    # rating
    if event.char=='y':
      frame.probs[frame.nr] = frame.probs[frame.nr]+1
      print frame.probs[frame.nr]
      print str(frame.probs)
      print "Yay"
    elif event.char=='n':
      frame.probs[frame.nr] = frame.probs[frame.nr]-1
      print "Nay"
    # speeeeed
    if event.char=='f':
      frame.speed = frame.speed/2
      #print "Faster"
    elif event.char=='s':
      frame.speed = 2 * frame.speed
      #print "Slower"
    # backward and pause play
    elif event.char=='b':
      frame.backwards = not frame.backwards
      #print "backwards"
    elif event.char=='p':
      frame.weightedNextPic()
    elif event.char==' ':
      frame.pause = not frame.pause
      if frame.pause:
        print "paused"
      else:
        print "unpaused"
        frame.next()
    else:
      print "Press y(ay) or n(ay)!"
      print "pressed", repr(event.char)

# --------------------------------------------------------------------
# script interface

if __name__ == "__main__":

    if not sys.argv[1:]:
        print "Syntax: python player.py imagefile"
        sys.exit(1)

    filename = sys.argv[1]
    root = Tk()
    # remove borders - removes also resizing and keybindings :(
    #root.overrideredirect(1)
    root.title('BYOG - Bring your own *.gif!')

    # enqueue further images
    ims = []
    probs = []
    for file in sys.argv[1:]:
      #ims.append(Image.open(file))
      ims.append(file)
      probs.append(0)
    # open the first image
    frame = UI(root, ims, probs)
    frame.bind("<Key>", key)
    frame.pack(side="bottom",fill="both",expand="yes")
    frame.focus_set()
    root.mainloop()
