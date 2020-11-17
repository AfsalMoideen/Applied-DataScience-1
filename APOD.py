#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:34:37 2020

@author: afsalmoideen
"""
__author__ = "Afsal Moideen"
__date__ = "2020-11-17"
__version__ = "1.0.1" 
__maintainer__ = "Afsal Moideen" 
__email__ = "ac20adi@herts.ac.uk"

from skimage import io
import numpy as np
import requests

#define original url to apod
url = 'https://apod.nasa.gov/apod/astropix.html'

#get the text of the webpage
data = requests.get(url).text

#split into lines
lines = data.split('\n')

for l in lines:
   #arch for the html tag
    if "IMG SRC" in l:
        #when found split by quotation marks to get path
        img = l.split('"')[1]
        break
    
#make our new url to source image
new_url = url.replace('astrpix.html',img) 

#make our request
image_data = requests.get(url)

#open a file to write binary mode
filehandle = open('/users/afsalmoideen/Desktop/apod.jpg', 'wb')

#write the content of the request to the file
filehandle.write(image_data.content)
filehandle.close()

#read into numpy array
image = io.imread('/users/afsalmoideen/Desktop/apod.jpg')

#find the coordinates of the central pixel
xc = int(image.shape[0]/2)
yc = int(image.shape[1]/2)

#define a cropping window
win =128

#define a cropping window
cropped = image[xc-win:xc+win,yc-win:yc+win]

#slice out the array in the first two axis
io.imsave = ('/users/afsalmoideen/Desktop/apod_crop.jpg')