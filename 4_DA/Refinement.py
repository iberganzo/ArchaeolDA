# VIA TOOL JSON
# Changing how polygons data is presented for polygon cropping algorithm

import numpy as np
import cv2
import re
import os
import glob

from PIL import Image, ImageDraw, ImageFilter, ImageFile
import random
import math

# Refinement Dataset #

backImagesStorage = 1 # Number of original background images
backImagesNumber = 10 # Number of background back%d.png images to use
numBacksImg = math.ceil(backImagesNumber/backImagesStorage) # Number of back%d.png per background image
createBackImages = 0 # Background images creation: 0: PNG images, 1: TIFF images, 2: Already Created
imgFP = 50 # Avergae number of each false positive per background image

# Refinement Configuration #

rotateFP = 1 # Negative training data rotation
margin = 200 # Maximun size of a false positive

# Helper function to perform sort
def num_sort1(test_string):
    return list(map(int, re.findall(r'(?<=back)\d+', test_string)))[0]
#def num_sort2(test_string):
#    return list(map(int, re.findall(r'(?<=split_)\d+', test_string)))[0]

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Create Background Images #

path=os.path.abspath(os.getcwd())

if not os.path.exists('backs'):
  os.mkdir('backs')

if createBackImages==1:
  pathDataImgTIFF=os.path.join(path,'TIFF')
  pathDataImg=os.path.join(path,'img')
  pathDataImgBacks=os.path.join(path,'backs')
  for filenameR in glob.glob("TIFF/.*"):
      os.remove(filenameR)
  file_list=os.listdir(pathDataImgTIFF)
  file_list=sorted(file_list)

  for iFile in range(0,len(file_list),1):
    [imName,imExt] = os.path.splitext("%s" %file_list[iFile])
    img = cv2.imread(os.path.join(pathDataImgTIFF,"%s" %file_list[iFile]))
    cv2.imwrite(os.path.join(pathDataImg, "%s.png" %imName),img)
    for num1 in range(1,numBacksImg+1,1):
      cv2.imwrite(os.path.join(pathDataImgBacks, "back%d.png" %(1+iFile+(len(file_list)*(num1-1)))),img)

  print("Images converted from TIFF to PNG")

if createBackImages !=2:
  pathDataImg=os.path.join(path,'img')
  pathDataImgBacks=os.path.join(path,'backs')
  for filenameR in glob.glob("img/.*"):
    os.remove(filenameR)
  file_list=os.listdir(pathDataImg)
  file_list=sorted(file_list)

  for iFile in range(0,len(file_list),1):
    [imName,imExt] = os.path.splitext("%s" %file_list[iFile])
    img = cv2.imread(os.path.join(pathDataImg,"%s" %file_list[iFile]))
  for num1 in range(1,numBacksImg+1,1):
    cv2.imwrite(os.path.join(pathDataImgBacks, "back%d.png" %(1+iFile+(len(file_list)*(num1-1)))),img)

print("Background images created")

pathDataImg=os.path.join(path,'backs')
for filenameR in glob.glob("backs/.*"):
    os.remove(filenameR)
file_list=os.listdir(pathDataImg)
file_list.sort(key=num_sort1)

pathDataFP=os.path.join(path,'FP')
for filenameR in glob.glob("FP/.*"):
    os.remove(filenameR)
file_list2=os.listdir(pathDataFP)
file_list2=sorted(file_list2)

for i1 in range(0, len(file_list2), 1):
    numFP = 0
    print('Time left: %d' %int(imgFP*(len(file_list2)-i1)))
    while numFP != imgFP:
        im2 = Image.open(os.path.join(pathDataFP, file_list2[i1]))
        iR = random.randint(0,len(file_list)-1)
        im1 = Image.open(os.path.join(pathDataImg, file_list[iR]))
        img1 = cv2.imread(os.path.join(pathDataImg, file_list[iR]))
        print('%s: %s' %(file_list2[i1],file_list[iR]))
        back_im = im1.copy()
        #height, width, channels = img1.shape
        width, height = im1.size
        sizeX = width # Image pixel size in x axis
        sizeY = height # Image pixel size in y axis
        nX = random.randint(1,sizeX-margin) # Random movement in x axis
        nY = random.randint(1,sizeY-margin) # Random movement in y axis
        if rotateFP == 0:
        	im2R = im2
        else:
            nF = random.randint(0,360) # Random flip angle in degrees
            im2R = im2.rotate(nF)
        back_im.paste(im2R, (nX, nY), mask=im2R)

        numFP = numFP + 1
        back_im.save(os.path.join(pathDataImg, file_list[iR]), quality=100)
  
print("Refinement DONE")

