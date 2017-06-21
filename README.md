## Switch-Fightstick
Proof-of-Concept Fightstick for the Nintendo Switch. Uses the LUFA library and reverse-engineering of the Pokken Tournament Pro Pad for the Wii U to enable custom fightsticks on the Switch System v3.0.0.

### Wait, what?
On June 20, 2017, Nintendo released System Update v3.0.0 for the Nintendo Switch. Along with a number of additional features that were advertised or noted in the changelog, additional hidden features were added. One of those features allows for the use of compatible controllers, such as the Pokken Tournament Pro Pad, to be used on the Nintendo Switch.

Unlike the Wii U, which handles these controllers on a 'per-game' basis, the Switch treats the Pokken controller as if it was a Switch Pro Controller. Along with having the icon for the Pro Controller, it functions just like it in terms of using it in other games, apart from the lack of physical controls such as analog sticks, the buttons for the stick clicks, or other system buttons such as Home or Capture.

### But games like ARMS use the analog sticks!
The Pokken Tournament Pro Pad was made by HORI, who also makes controllers for other consoles; because of this, the descriptors provided to Nintendo for the Pokken controller are **very** similar to that of some third-party PS3 controllers. In fact, the Pokken Tournament Pro Pad -can- be used on the PS3 without anything special needing to be done. The original descriptors feature 13 buttons, two analog sticks, a HAT switch, and some vendor-specific items that we can safely ignore. Compare this to a PS3 controller, which has...13 buttons (4 Face, 4 Shoulders, 2 Sticks, Select/Start, and PS), two analog sticks, and a HAT switch (the D-Pad). 

### What do you mean by 'original descriptors?'
Turns out we can modify the descriptors to expose up to 16 buttons at **least**. The Switch Pro Controller has 14 buttons on it, and as it turns out, the modified set of descriptors does allow us to enable the use of the most important button:

### Is it the Captu-

# THE CAPTURE BUTTON

The Switch Pro Controller also exposes **additional** buttons within its descriptors; however, it's unknown as to what those do at this time. These come immediately after the HAT, so I'm under the assumption that they may be individual button presses instead of an angle. That being said, considering how flexible the Switch is with the Pokken controller descriptors, we may be able to mirror the Switch Pro Controller descriptors up to a certain point.