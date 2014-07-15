#!/usr/bin/env python

import sys
import scipy
import numpy as np
import scipy.misc

def main():
    image = scipy.misc.imread('./challenge.png')                        # Open the image as a numpy array
    boxes = create_boxes(image)                                         # Get the character array boxes
    widths = []
    location = 12                                                       # How far down each picture to look
    for box in boxes:                                                   # Iterate through all the boxes
        width    = 0
        state    = False
        previous = False
        for x in range(len(box[1])):                                    # Iterate through the row of pixels at y=12
            pixel = np.array([box[location, x]])                        # Current color pixel
            white = (int(pixel[0][2]) > 220)                            # Boolean flag
            if state == False and white == True:                        # "State Machine" to get width
                state = True
                previous = True
            elif state == True and white == True and previous == True:
                pass
            elif state == True and white == True and previous == False:
                break
            elif state == True and white != True:
                previous = False
                width += 1
        widths.append(width)
    bitstring = ''
    zero = max(widths)                                                  # Get zero value
    index = 1
    one = sorted(widths)[len(widths) - index]                           # Get one value
    while one == zero:
        index += 1
        one = sorted(widths)[len(widths) - index]
    for item in widths:
        if item == zero:
            bitstring += '0'
        elif item == one:
            bitstring += '1'
    bits = [bitstring[x:x + 7] for x in range(0, len(bitstring), 7)]    # List of bytes in bit form
    text = ''                                                           # Convert bytes to ascii characters
    for item in bits:
        final_bit = '0' + item
        value = int('0' + item, 2)
        text += (chr(value))
    print(text)

def create_boxes(image):
    '''
    Chunk the image into boxes
    '''
    x_gap = 12                                                          # How far sideways to go for each box
    y_gap = 23                                                          # How far vertically to go for each box
    images = []                                                         # List of boxes
    for y in range(0, len(image), y_gap):                               # Iterate each row
        for x in range(0, len(image), x_gap):                           # Iterate each column
            n_image = image[y:y + y_gap, x:x + x_gap]                   # Image is our position + gap
            if len(np.array(n_image[0])) > 10 and len(n_image) > 20:    # If the image is the wrong dimension, ignore
                images.append(n_image)                                  # Else, append to array
    return images


if __name__ == "__main__":
    sys.exit(main())
