import os

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from  PIL  import Image
"""
img = cv.imread('images/MichaelJordan.jpg', cv.IMREAD_UNCHANGED)
original = img.copy()

l = int(max(5, 6))
u = int(min(6, 6))

ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.GaussianBlur(img, (21, 51), 3)
edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
edges = cv.Canny(edges, l, u)

_, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

data = mask.tolist()
sys.setrecursionlimit(10**8)
for i in  range(len(data)):
    for j in  range(len(data[i])):
        if data[i][j] !=  255:
            data[i][j] =  -1
        else:
            break
    for j in  range(len(data[i])-1, -1, -1):
        if data[i][j] !=  255:
            data[i][j] =  -1
        else:
            break
image = np.array(data)
image[image !=  -1] =  255
image[image ==  -1] =  0

mask = np.array(image, np.uint8)

result = cv.bitwise_and(original, original, mask=mask)
result[mask ==  0] =  255
cv.imwrite('images\\bg.png', result)

img = Image.open('images\\bg.png')
img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("images\MichaelJordan_edit.jpg", "JPEG")

"""
"""
# -*- coding: utf-8 -*-
from PIL import Image

os.system('cmd /c "backgroundremover -i images/MichaelJordan.jpg -o images/MichaelJordanTmp.png"')

image = Image.open('images\\MichaelJordanTmp.png')
image = image.convert('RGBA')
image.convert('RGB').save("images\\MJ_WhiteBG.jpg")
"""
"""
import Image
from resizeimage import resizeimage

os.system('cmd /c "backgroundremover -i images/MichaelJordan.jpg -o images/MichaelJordanTmp.png"')

f = Image.open('images\\MichaelJordan.jpg')
alpha1 = 0 # Original value
r2, g2, b2, alpha2 = 255, 255, 255,255 # Value that we want to replace it with

red, green, blue,alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
mask = (alpha==alpha1)
data[:,:,:3][mask] = [r2, g2, b2, alpha2]

data = np.array(f)
f = Image.fromarray(data)
f = f.resize((basewidth,hsize), PIL.Image.ANTIALIAS)

f.save('modified.png', image.format)
"""


import cv2

keywords = sys.argv[1]

cmd = 'backgroundremover -i images//' + keywords + '.jpg -o images//' + keywords + 'Tmp.png'
os.system('cmd /c ' + cmd)

#load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
image = cv2.imread('images/' + keywords + 'Tmp.png', cv2.IMREAD_UNCHANGED)

#make mask of where the transparent bits are
trans_mask = image[:,:,3] == 0

#replace areas of transparency with white and not transparent
image[trans_mask] = [255, 255, 255, 255]

#new image without alpha channel...
new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

cv2.imwrite("images\\" + keywords + "_Final.jpg",new_img)
os.remove('images\\MichaelJordanTmp.png')
