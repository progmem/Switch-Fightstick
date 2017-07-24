## Switch-Fightstick
Proof-of-Concept Fightstick for the Nintendo Switch. Uses the LUFA library and reverse-engineering of the Pokken Tournament Pro Pad for the Wii U to enable custom fightsticks on the Switch System v3.0.0.

### Wait, what?
On June 20, 2017, Nintendo released System Update v3.0.0 for the Nintendo Switch. Along with a number of additional features that were advertised or noted in the changelog, additional hidden features were added. One of those features allows for the use of compatible controllers, such as the Pokken Tournament Pro Pad, to be used on the Nintendo Switch.

Unlike the Wii U, which handles these controllers on a 'per-game' basis, the Switch treats the Pokken controller as if it was a Switch Pro Controller. Along with having the icon for the Pro Controller, it functions just like it in terms of using it in other games, apart from the lack of physical controls such as analog sticks, the buttons for the stick clicks, or other system buttons such as Home or Capture.

### Printing Splatoon Posts
For my own personal use, I repurposed Switch-Fightstick to output a set sequence of inputs to systematically print Splatoon posts. This works by using the smallest size pen and D-pad inputs to plot out each pixel one-by-one.

#### Printing Procedure
Use the analog stick to bring the cursor to the top-right corner, then press the D-pad down once to make sure the cursor is at y-position `0` instead of y-position `-1`. Then plug in the controller. Currently there are issues with controller conflicts while in docked mode which are avoided by using a USB-C to USB-A adapter in handheld mode. Printing currently takes about an hour.

The image printed depends on `image.c` which is generated with `bin2c.py` which takes a 1-bit RAW paletted .data exported from GIMP. An example file is included as `ironic.data`. `bin2c.py` will pack the 8bpp .data to a linear 1bpp array, ie

```
$ python2 bin2c.py ironic.data > image.c
```

Each line is printed from right to left in order to avoid pixel skipping issues. Currently there are also issues printing to the right and bottom edges. This repository has been tested using a Teensy 2.0++.

### Sample
![http://i.imgur.com/93B1Usb.jpg](http://i.imgur.com/93B1Usb.jpg)
*image via [/u/Stofers](https://www.reddit.com/user/Stofers)*
