byog
====

Bring Your Own Gif. This is a script that displays your collection of `*.gif` files as a party projection.
Just call the `player.py` script with the gifs you want to display, for example like `./player.py mycollection/*.gif`. The files will be played in a black rectangular window, to allow borderless projection, and they are chosen randomly, starting all with equal probability. With a probability of 0.5 they will be played again. The files can be rated interactively with `y`ay and `n`ay, 
played backwards with `b`ackwards, and the overall play can be made `s`lower and `f`aster interactively. Enjoy!
This script uses `PIL` and `tkinter`.

If your gifs are compressed and don't display properly, or if they are too small, you can preprocess them with the provided shell scripts, `clean.sh` and `grow.sh`. These scripts ues `ImageMagick`.

![Zoomenkohl](https://github.com/linse/byog/blob/master/gif_raw/zoomenkohl.gif)
