#!/bin/python

import sys, os
from PIL import Image

im = Image.open(sys.argv[1])            # import 320x120 png
if not (im.size[0] == 320 and im.size[1] == 120):
  print("ERROR: Image must be 320px by 120px!")
else:
  im = im.convert("1").load()            # convert to bilevel image
  data = []                              # dithering if necessary
  for i in range(0,120):                 # iterate over the columns
    for j in range(0,320):               # and convert 255 vals to 1
       data.append(1 if im[j,i] == 255 else 0)

  str_out = "#include <stdint.h>\n\nuint8_t image_data[0x12c1] = {"
  for i in range(0, (320*120) / 8):
     val = 0;
     
     for j in range(0, 8):
        val |= data[(i * 8) + j] << j
     
     val = ~val & 0xFF;
     str_out += hex(val) + ", "         # append hexidecimal bytes
                                        # to the output .c array 
  str_out += "0x0};"                    # of bytes

  with open('image.c', 'w') as f:       # save output into image.c
    f.write(str_out)