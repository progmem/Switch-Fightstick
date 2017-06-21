## Switch-Fightstick
Proof-of-Concept LUFA Project for the Nintendo Switch. Uses reverse-engineering of the Pokken Tournament Pro Pad for the Wii U and Switch System v3.0.0

### Wait, what?
On June 20, 2017, Nintendo released System Update v3.0.0 for the Nintendo Switch. Along with a number of additional features that were advertised or noted in the changelog, additional hidden features were added. One of those features allows for the use of compatible controllers, such as the Pokken Tournament Pro Pad, to be used on the Nintendo Switch.

Unlike the Wii U, the Switch treats the Pokken controller similar to a Switch Pro Controller. Along with having the icon for the Pro Controller, it functions just like it in terms of using it in other games.

### But games like ARMS use the analog sticks!
The Pokken Tournament Pro Pad was made by HORI, who also makes controllers for other consoles; the descriptors provided to Nintendo for the Pokken controller are -very- similar to that of some PS3 controllers (the Pokken controller -can- be used on the PS3, in fact). The original descriptors feature 13 buttons (this includes stick clicks and a 'Home' button), two analog sticks, a HAT switch, and some vendor-specific items that we can safely ignore.

### ...original descriptors?
Turns out we can modify the descriptors to expose 16 buttons; the Switch only makes use of 14 of these, but this gives us the addition of the most important button:

# THE CAPTURE BUTTON
