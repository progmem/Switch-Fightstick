# Switch-Fightstick Teensy 2 ++

This is a fork from [progmem/Switch-Fightstick](https://github.com/progmem/Switch-Fightstick) to turn a [Teensy 2++](https://www.pjrc.com/store/teensypp.html)
into a Nintento Switch Fighting Stick.


# Mapping

                              GND +---.....---+ Vcc
                      DPad Up PB7 +           + PB6 DPad Down
                     Button Y PD0 +           + PB5 DPad Right
                     Button B PD1 +           + PB4 DPad Left
                     Button A PD2 +           + PB3 Shoulder ZL
                     Button X PD3 +           + PB2
                   Shoulder L PD4 +           + PB1
                   Shoulder R PD5 +           + PB0
                    Power LED PD6 +           + PE7
                  Shoulder ZR PD7 +           + PE6
                              PE0 +           + GND
                              PE1 +           + REF
                Button Select PC0 +           + PF0
                 Button Start PC1 +           + PF1
         Button Left Joystick PC2 +           + PF2
        Button Right Joystick PC3 +           + PF3
                  Button Home PC4 +           + PF4
               Button Capture PC5 +           + PF5
                              PC6 +           + PF6
                              PC7 +--+--+--+--+ PF7
                      RST ----------/   |   \---------- Vcc
                                       GND

# Copyright

Copyright &copy; 2021 Benjamin Van Ryseghem <benjamin.vanryseghem@gmail.com>

Distributed under a MIT License (MIT) (see "LICENSE")
