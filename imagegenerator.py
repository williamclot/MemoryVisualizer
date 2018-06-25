from __future__ import division
import numpy as np
from PIL import Image
import sys
import math
import os

# Usage python ./image.py <memorydump> <datafile> <outputname>

DUMPFILE = sys.argv[1]
FILE = sys.argv[2]
FILENAME = sys.argv[3]
PAGE_SIZE = 4096


##########################################
##     SIZE CALCULATION OF THE IMAGE    ##
##########################################

#Size of the dump file
statinfo = os.stat(DUMPFILE)
SIZE = statinfo.st_size
print("Size of Dump file:")
print(SIZE)

#Number of pages in the dumpfile
nb_pages = int(SIZE / 4096)
print("Number of pages:")
print(nb_pages)

#Calculating image size with square root of the number of pages
image_size = int(math.ceil((math.sqrt(nb_pages))))
print("Image size:")
print(image_size)

######################################
##        ANALYSING THE DATA        ##
######################################

def xy(n, image_size):
    """Returns position of pixel n in 2D array"""
    x = int(n % image_size)
    y = int(math.floor(n / image_size))
    return (x,y)

#Open up the data file generated by our volatility plugin
with open(FILE) as f:
    lines = f.read().splitlines()

pages = []

#Going through all the lines of data
for i in range(len(lines)):
    lines[i]=lines[i].split()
    #Getting the physical address of the page, the size and if it's kernel
    physical_addr = int(lines[i][1])
    page_size = int(lines[i][2])
    is_kernel = lines[i][3]

    pages.append([physical_addr, page_size, is_kernel])

#Creating numpy array that will be transformed into the image
image = np.zeros((image_size, image_size, 3), dtype=np.uint8)

#Filling up the image in white (all RGB values to 255)
for x in range(image_size):
    for y in range(image_size):
        image[y][x][0] = 255
        image[y][x][1] = 255
        image[y][x][2] = 255

#Filling up the image with the values of the pages list
for i in range(len(pages)):
    #importing data for each page
    page_nb = int(pages[i][0]/4096)
    page_pixel_size = int(pages[i][1]/4096)
    is_kernel = pages[i][2]

    if(page_nb < nb_pages):
        for j in range(page_pixel_size):
            #Dealing with longer pages that 4096 bits
            (x,y) = xy(page_nb + j, image_size)

            if is_kernel == "True":
                #Setting color to a light blue
                image[y][x][0] = 95     #R
                image[y][x][1] = 194    #G
                image[y][x][2] = 205    #B

            if is_kernel == "False":
                #Setting color to red
                image[y][x][0] = 212    #R
                image[y][x][1] = 70     #G
                image[y][x][2] = 45     #B

#Transforming the array into a png file with the Image library of Pillow
png = Image.fromarray(image)
if png.mode != 'RGB':
    png = png.convert('RGB')
#Saving the file
png.save("images/"+FILENAME+".png")

print("\nPNG image file is generated!")
print("The result can be found at the following path: images/"+FILENAME+".png")

print("\nlight blue pixels corresponds to kernel pages")
print("light red pixels corresponds to user pages")