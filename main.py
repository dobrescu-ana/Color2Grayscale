from app_config import *

import numpy
import cv2
from PIL import Image
import math
from sklearn import preprocessing

def normalize(image):
    if normalization:
        (rows, cols, channels)=image.shape
        normImage = numpy.zeros((rows, cols, channels), dtype=int)
        for channel in range(channels):
            minVal=255
            maxVal=0
            for row in range(rows):
                for col in range(cols):
                    if image[row][col][channel]<minVal:
                        minVal=image[row][col][channel]
                    if image[row][col][channel]>maxVal:
                        maxVal=image[row][col][channel]
            for row in range(rows):
                for col in range(cols):
                    normImage[row][col][channel]=math.ceil(((image[row][col][channel]-minVal)/(maxVal-minVal))*255)
        return normImage
    else:
        return image

def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

image = get_image(InputImageNamePath+ImageExtension)
(rows, cols, channels)=image.shape

newImage=normalize(image)
myConversion = normalize(image)
for itter in range(R_coef.__len__()):
    grayImage = numpy.zeros((rows, cols), dtype=int)
    auxMax = numpy.zeros((rows, cols), dtype=int)

    for row in range(rows):
        for col in range(cols):
            grayImage[row][col]=newImage[row][col][0]*R_coef[itter]+newImage[row][col][1]*G_coef[itter]+newImage[row][col][2]*B_coef[itter]

    if normalization:
        cv2.imwrite(OutputImageNamePath+"_NORMALIZED_"+str(itter)+ImageExtension,grayImage)
    else:
        cv2.imwrite(OutputImageNamePath+"_"+str(itter)+ImageExtension,grayImage)


for row in range(rows):
        for col in range(cols):
            aux = (newImage[row][col][0] + newImage[row][col][1] + newImage[row][col][2])/(3*255)
            myConversion[row][col]=newImage[row][col][0]*aux+newImage[row][col][1]*aux+newImage[row][col][2]*aux

cv2.imwrite(OutputImageNamePath+"_PERSONAL_CONVERSION"+ImageExtension,myConversion)
print("Eop")