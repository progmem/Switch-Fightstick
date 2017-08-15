#!/bin/python

import sys

data = open(sys.argv[1], 'rb').read()

str_out = "#include <stdint.h>\n#include <avr/pgmspace.h>\n\nconst uint8_t image_data[0x12c1] PROGMEM = {"
for i in range(0, (320*120) / 8):
   val = 0;
   
   for j in range(0, 8):
      val |= ord(data[(i * 8) + j]) << j
   
   val = ~val & 0xFF;
   str_out += hex(val) + ", "
   
str_out += "0x0};"
   
with open('image.c', 'w') as f:
  f.write(str_out)