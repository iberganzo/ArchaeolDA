# Add the DA database cropped PNG objects to new only background images #

from PIL import Image, ImageDraw, ImageFilter, ImagePath
import cv2
import os
import glob
import random
import math
from math import sin, cos, radians
import numpy as np
import warnings
import time
import sys

# Ignore DecompressionBombWarning, big size images are used
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

# DA Dataset #

createBackImages = 0 # Background images creation: 0: PNG images, 1: TIFF images, 2: Already created
backImagesStorage = 1 # Number of original background images
backImagesNumberIni = 1 # Initial number of background back%d.png images to use
backImagesNumber = 10 # Number of background back%d.png images to use
numBacksImg = math.ceil(backImagesNumber/backImagesStorage) # Number of back%d.png per background image
cropImagesPerBackImages = 30 # Number of cropped crop%d.png objects to be in each background image
cropImageStoreSize = 1 # List of cropped crop%d.png objects to be used
cropImageStoreSizeInitial = 1 # Initial number of the list of cropped crop%d.png objects to be used

# DA Techniques #

daRotate = 0 # DA Rotation: 0: No, 1: Yes 
daResize = 0 # DA Resizing: 0: No, 1: Yes, 2: Just Decrease, 3: Just Increase
daElastic = 0 # DA Elastic Deformation: 0: No, 1: Yes
doppel = 0 # DA Doppelgänger Technique: 0: No, 1: Yes

# DA Configuration #

margin = 200 # Maximun size of an object
minResized = 45 # Minimun object size after DA Resizing
maxResized = margin - 1 # Maximun object size after DA Resizing
fileWeigthTh = 0 # Minimun file size for DA Resizing: 0: All, e.g. 4000: 4 KB
nDiamRMax = 3 # The maximum side ratio for DA Elastic Deformation
maxPointsNumber = 250 # Maximun number of points in a object polygon
timeoutMin = 5 # Minutes for a timeout during a synthetic image creation

def rotatePolygon(polygon, degrees, height, width, minsize):
    
    # Convert angle to radians
    theta = radians(degrees)
    
    # Getting sin and cos with respect to theta
    cosang, sinang = cos(theta), sin(theta) 

    # find center point of Polygon to use as pivot
    x, y = [i for i in zip(*polygon)]

    # find center point of Polygon to use as pivot
    cx1 = (width / 2) + minsize[0]
    cy1 = (height / 2) + minsize[1]

    # Rotating every point
    new_points = []
    for x, y in zip(x, y):
        tx, ty = x-cx1, y-cy1
        new_x = (tx*cosang - ty*sinang) + cx1
        new_y = (tx*sinang + ty*cosang) + cy1
        new_points.append((new_x, new_y))
    return new_points, cx1, cy1

def Point(x, y):
  point = (x,y)
  return point

# Create Background Images #

path=os.path.abspath(os.getcwd())

if not os.path.exists('4_DA/backs'):
  os.mkdir('4_DA/backs')

if createBackImages==1:
  pathDataImgTIFF=os.path.join(path,'4_DA/TIFF')
  pathDataImg=os.path.join(path,'4_DA/img')
  pathDataImgBacks=os.path.join(path,'4_DA/backs')
  for filenameR in glob.glob("4_DA/TIFF/.*"):
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
  pathDataImg=os.path.join(path,'4_DA/img')
  pathDataImgBacks=os.path.join(path,'4_DA/backs')
  for filenameR in glob.glob("4_DA/img/.*"):
    os.remove(filenameR)
  file_list=os.listdir(pathDataImg)
  file_list=sorted(file_list)

  for iFile in range(0,len(file_list),1):
    [imName,imExt] = os.path.splitext("%s" %file_list[iFile])
    img = cv2.imread(os.path.join(pathDataImg,"%s" %file_list[iFile]))
    for num1 in range(1,numBacksImg+1,1):
      cv2.imwrite(os.path.join(pathDataImgBacks, "back%d.png" %(1+iFile+(len(file_list)*(num1-1)))),img)

print("Background images created")

# Create Synthetic Data #

if not os.path.exists('4_DA/synthetic'):
  os.mkdir('4_DA/synthetic')
for i3 in range(backImagesNumberIni, backImagesNumber+1, 1):
  
  timeout = time.time() + 60*timeoutMin # minutes from now
  
  im1 = Image.open("4_DA/backs/back%d.png" %i3)
  img = cv2.imread('4_DA/backs/back%d.png' %i3)
  height, width, channels = img.shape
  sizeX = width # Objects image pixel size in x axis
  sizeY = height # Objects image pixel size in y axis

  txtFile3 = np.zeros(shape=(cropImagesPerBackImages,maxPointsNumber))
  back_im = im1.copy()

  iPoly=0; iPolyCount=0; overlappingPolys=np.zeros(shape=(3*cropImagesPerBackImages,4))
  while True:
    fileWeigth = 0
    doppelDone = 0
    
    while fileWeigth <= fileWeigthTh:
      nC = random.randint(cropImageStoreSizeInitial,cropImageStoreSize)
      im2 = Image.open("3_Objects/DA/crop%d.png" %nC)
      pathForSize=os.path.join(path,'3_Objects/DA/crop%d.png' %nC)
      fileWeigth = int(os.path.getsize(pathForSize))

    txtFile1 = np.loadtxt("3_Objects/DA/crop%d.txt" %nC, dtype=int)
    txtFile2t = np.zeros(shape=(txtFile1.shape))

    # DA Translation #

    nX = random.randint(margin,sizeX-margin) # Random movement in x axis
    nY = random.randint(margin,sizeY-margin) # Random movement in y axis
    
    # DA Rotation #

    if (daRotate==1):
    	nF = random.randint(0,359) # Random flip angle in degrees
    else:
    	nF = 0 # No rotation

    w1, h1 = im2.size
    txtFile2x = np.zeros(shape=(1,int(len(txtFile1)/2)));
    txtFile2y = np.zeros(shape=(1,int(len(txtFile1)/2)));
    num3=0; numX=0; numY=0;
    for it2 in range(0,len(txtFile1),2):
      txtFile2x[0,num3]=txtFile1[it2]
      txtFile2y[0,num3]=txtFile1[it2+1]
      num3=num3+1
      numX=numX+txtFile1[it2]
      numY=numY+txtFile1[it2+1]
    numX=numX/num3
    numY=numY/num3
    xmin=min(txtFile2x[0,:])
    ymin=min(txtFile2y[0,:])
    xmax=max(txtFile2x[0,:])
    ymax=max(txtFile2y[0,:])
    xmino=int(xmin); ymino=int(ymin);

    txtFile2r1 = []
    for ir in range(0, len(txtFile1), 2):
      if txtFile1[ir] != 0:
        txtFile2r1.append(Point(txtFile1[ir],txtFile1[ir+1]))

    txtFile2rp, cx, cy = rotatePolygon(txtFile2r1, 360-nF, h1, w1, [xmin,ymin])
    rotate_im2= im2.rotate(nF, expand=1)
    w2, h2 = rotate_im2.size

    num2=0
    txtFile2r = np.zeros(txtFile1.shape)
    for row in txtFile2rp:
      txtFile2r[num2]=row[0]
      txtFile2r[num2+1]=row[1]
      num2=num2+2

    txtFile2xr = np.zeros(shape=(1,int(len(txtFile2r)/2)));
    txtFile2yr = np.zeros(shape=(1,int(len(txtFile2r)/2)));
    num3r=0
    for it2r in range(0,len(txtFile2r),2):
      txtFile2xr[0,num3r]=txtFile1[it2r]
      txtFile2yr[0,num3r]=txtFile1[it2r+1]
      num3r=num3r+1
    xminr=int(min(txtFile2xr[0,:]))
    yminr=int(min(txtFile2yr[0,:]))
    
    tw=int((w2-w1)/2); th=int((h2-h1)/2)
    xmint=xmino-xminr+nX-tw
    ymint=ymino-yminr+nY-th

    for i6 in range(0, len(txtFile2r), 2):
      txtFile2t[i6]=txtFile2r[i6]-xminr+nX
      txtFile2t[i6+1]=txtFile2r[i6+1]-yminr+nY

    # DA Elastic Deformation #

    sxR,syR = rotate_im2.size
    sR1 = max(sxR,syR)
    sR2 = min(sxR,syR)
    nDiamR = random.uniform(1,nDiamRMax)
    if daElastic == 1:
      nDiamR = nDiamR
    else:
      nDiamR = sR1 / sR2

    # DA Resizing #

    if daResize != 0:
      nS = random.randint(minResized,maxResized) # Random size in pixels
      nS1 = random.randint(minResized,sR1)
      nS2 = random.randint(sR1,maxResized)
      #nS = random.choice([sR1, sR1, sR1, sR1, sR1, nS1, nS1, nS1, nS2, nS2]) # 50% chance to remain equal, 30% to decrease, 20% to increase
      if daResize == 1:
        if daElastic == 0:
          if sR1 == sxR:
            fx = nS
            fy = fx / nDiamR
          else:
            fy = nS
            fx = fy / nDiamR
        else:
          fx = random.choice([nS, nS/nDiamR])
          if fx == nS:
            fy = fx / nDiamR
          else:
            fy = nS
      elif daResize == 2: # Only decreasing
        if daElastic == 0:
          if sR1 == sxR:
            fx = nS1
            fy = fx / nDiamR
          else:
            fy = nS1
            fx = fy / nDiamR
        else:
          fx = random.choice([nS1, nS1/nDiamR])
          if fx == nS1:
            fy = fx / nDiamR
          else:
            fy = nS1
      else: # Only increasing
        if daElastic == 0:
          if sR1 == sxR:
            fx = nS2
            fy = fx / nDiamR
          else:
            fy = nS2
            fx = fy / nDiamR
        else:
          fx = random.choice([nS2, nS2/nDiamR])
          if fx == nS2:
            fy = fx / nDiamR
          else:
            fy = nS2
    else: # No resizing
        fx = sxR
        fy = fx / nDiamR

    dsizeX = math.ceil((sxR/sxR)*fx)
    dsizeY = math.ceil((syR/syR)*fy)
    dsize = (dsizeX,dsizeY)
    resizedDeformed_im2 = rotate_im2.resize(dsize)
    sxD,syD = resizedDeformed_im2.size

    xminrD0 = math.ceil((xmint/sxR)*fx)
    yminrD0 = math.ceil((ymint/syR)*fy)
    xminrD = int(xminrD0 - (xminrD0 - xmint))
    yminrD = int(yminrD0 - (yminrD0 - ymint))

    # Overlap Avoidance #

    overlappingPolys[iPoly,0] = xminrD # xmin
    overlappingPolys[iPoly,1] = yminrD # ymin
    overlappingPolys[iPoly,2] = xminrD + sxD # xmax
    overlappingPolys[iPoly,3] = yminrD + syD # ymax

    overlap1 = 0
    for iOv in range(0,iPoly,1):
      # A new polygon inside/over an old one #
      overlap1X = 0; overlap1Y = 0;
      # xmin(new) >= xmin(old) and xmin(new) < xmax(old)
      if overlappingPolys[iPoly,0] >= overlappingPolys[iOv,0] and overlappingPolys[iPoly,0] < overlappingPolys[iOv,2]:
        overlap1X = overlap1X + 1
      # ymin(new) >= ymin(old) and ymin(new) < ymax(old)
      if overlappingPolys[iPoly,1] >= overlappingPolys[iOv,1] and overlappingPolys[iPoly,1] < overlappingPolys[iOv,3]:
        overlap1Y = overlap1Y + 1 
      # xmax(new) > xmin(old) and xmax(new) <= xmax(old)
      if overlappingPolys[iPoly,2] > overlappingPolys[iOv,0] and overlappingPolys[iPoly,2] <= overlappingPolys[iOv,2]:
        overlap1X = overlap1X + 1
      # ymax(new) > ymin(old) and ymax(new) <= ymax(old)
      if overlappingPolys[iPoly,3] > overlappingPolys[iOv,1] and overlappingPolys[iPoly,3] <= overlappingPolys[iOv,3]:
        overlap1Y = overlap1Y + 1
      # xmin(new) < xmin(old) and xmax(new) > xmax(old)
      if overlappingPolys[iPoly,0] < overlappingPolys[iOv,0] and overlappingPolys[iPoly,2] > overlappingPolys[iOv,2]:
        overlap1X = overlap1X + 1
      # ymin(new) < ymin(old) and ymax(new) > ymax(old)
      if overlappingPolys[iPoly,1] < overlappingPolys[iOv,1] and overlappingPolys[iPoly,3] > overlappingPolys[iOv,3]:
        overlap1Y = overlap1Y + 1
      # decision: more than two condition but not the same axis or none
      if ((overlap1X+overlap1Y>=2) and (overlap1X*overlap1Y != 0)):
        overlap1 = 1

    if overlap1 == 0:
      
      # DA Doppelgänger #

      if doppel == 1:
        pts = np.matrix("[[%d,%d];[%d,%d];[%d,%d];[%d,%d]]" %(xminrD,yminrD,xminrD,yminrD+syD,xminrD+sxD,yminrD+syD,xminrD+sxD,yminrD))

        ## (1) Crop the bounding rect
        rect = cv2.boundingRect(pts)
        x,y,w,h = rect
        croped = img[y:y+h, x:x+w].copy()

        ## (2) make mask
        pts = pts - pts.min(axis=0)

        mask = np.zeros(croped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ## (3) do bit-op
        dst = cv2.bitwise_and(croped, croped, mask=mask)
        
        ## (4) add the transparent background
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2BGRA)
        dst[:,:,3] = mask #Set mask as alpha channel

        cv2.imwrite(os.path.join('4_DA', "crop.png"),dst)
        dst = Image.open("4_DA/crop.png")

        # Paste back cropped
        if xminrD + 1 + (2*sxD) < sizeX:
          pasteIn = 0
        elif yminrD + 1 + (2*syD) < sizeY:
          pasteIn = 1
        elif xminrD - 1 - sxD > 0:
          pasteIn = 2
        else: # yminrD - 1 - syD > 0
          pasteIn = 3

        if pasteIn == 0:
          x1 = overlappingPolys[iPoly,2] + 1
          x2 = overlappingPolys[iPoly,2] + 1 + sxD
          y1 = overlappingPolys[iPoly,1]
          y2 = overlappingPolys[iPoly,3]
        elif pasteIn == 1:
          x1 = overlappingPolys[iPoly,0]
          x2 = overlappingPolys[iPoly,2]
          y1 = overlappingPolys[iPoly,3] + 1
          y2 = overlappingPolys[iPoly,3] + 1 + syD
        elif pasteIn == 2:
          x1 = overlappingPolys[iPoly,0] - 1 - sxD
          x2 = overlappingPolys[iPoly,0] - 1
          y1 = overlappingPolys[iPoly,1]
          y2 = overlappingPolys[iPoly,3]
        else:
          x1 = overlappingPolys[iPoly,0]
          x2 = overlappingPolys[iPoly,2]
          y1 = overlappingPolys[iPoly,1] - 1 - syD
          y2 = overlappingPolys[iPoly,1] - 1


        overlap2 = 0
        for iOv in range(0,iPoly,1):
          # A new polygon inside/over an old one #
          overlap2X = 0; overlap2Y = 0;
          # xmin(new) >= xmin(old) and xmin(new) < xmax(old)
          if x1 >= overlappingPolys[iOv,0] and x1 < overlappingPolys[iOv,2]:
            overlap2X = overlap2X + 1
          # ymin(new) >= ymin(old) and ymin(new) < ymax(old)
          if y1 >= overlappingPolys[iOv,1] and y1 < overlappingPolys[iOv,3]:
            overlap2Y = overlap2Y + 1 
          # xmax(new) > xmin(old) and xmax(new) <= xmax(old)
          if x2 > overlappingPolys[iOv,0] and x2 <= overlappingPolys[iOv,2]:
            overlap2X = overlap2X + 1
          # ymax(new) > ymin(old) and ymax(new) <= ymax(old)
          if y2 > overlappingPolys[iOv,1] and y2 <= overlappingPolys[iOv,3]:
            overlap2Y = overlap2Y + 1
          # xmin(new) < xmin(old) and xmax(new) > xmax(old)
          if x1 < overlappingPolys[iOv,0] and x2 > overlappingPolys[iOv,2]:
            overlap2X = overlap2X + 1
          # ymin(new) < ymin(old) and ymax(new) > ymax(old)
          if y1 < overlappingPolys[iOv,1] and y2 > overlappingPolys[iOv,3]:
            overlap2Y = overlap2Y + 1
          # decision: more than two condition but not the same axis or none
          if ((overlap2X+overlap2Y>=2) and (overlap2X*overlap2Y != 0)):
            overlap2 = 1

        if pasteIn == 0:
          x1 = overlappingPolys[iPoly,0] - 1 - sxD
          x2 = overlappingPolys[iPoly,0] - 1
          y1 = overlappingPolys[iPoly,1]
          y2 = overlappingPolys[iPoly,3]
        elif pasteIn == 1:
          x1 = overlappingPolys[iPoly,0]
          x2 = overlappingPolys[iPoly,2]
          y1 = overlappingPolys[iPoly,1] - 1 - syD
          y2 = overlappingPolys[iPoly,1] - 1
        elif pasteIn == 2:
          x1 = overlappingPolys[iPoly,2] + 1
          x2 = overlappingPolys[iPoly,2] + 1 + sxD
          y1 = overlappingPolys[iPoly,1]
          y2 = overlappingPolys[iPoly,3]
        else:
          x1 = overlappingPolys[iPoly,0]
          x2 = overlappingPolys[iPoly,2]
          y1 = overlappingPolys[iPoly,3] + 1
          y2 = overlappingPolys[iPoly,3] + 1 + syD

        overlap3 = 0
        for iOv in range(0,iPoly,1):
          # A new polygon inside/over an old one #
          overlap3X = 0; overlap3Y = 0;
          # xmin(new) >= xmin(old) and xmin(new) < xmax(old)
          if x1 >= overlappingPolys[iOv,0] and x1 < overlappingPolys[iOv,2]:
            overlap3X = overlap3X + 1
          # ymin(new) >= ymin(old) and ymin(new) < ymax(old)
          if y1 >= overlappingPolys[iOv,1] and y1 < overlappingPolys[iOv,3]:
            overlap3Y = overlap3Y + 1 
          # xmax(new) > xmin(old) and xmax(new) <= xmax(old)
          if x2 > overlappingPolys[iOv,0] and x2 <= overlappingPolys[iOv,2]:
            overlap3X = overlap3X + 1
          # ymax(new) > ymin(old) and ymax(new) <= ymax(old)
          if y2 > overlappingPolys[iOv,1] and y2 <= overlappingPolys[iOv,3]:
            overlap3Y = overlap3Y + 1
          # xmin(new) < xmin(old) and xmax(new) > xmax(old)
          if x1 < overlappingPolys[iOv,0] and x2 > overlappingPolys[iOv,2]:
            overlap3X = overlap3X + 1
          # ymin(new) < ymin(old) and ymax(new) > ymax(old)
          if y1 < overlappingPolys[iOv,1] and y2 > overlappingPolys[iOv,3]:
            overlap3Y = overlap3Y + 1
          # decision: more than two condition but not the same axis or none
          if ((overlap3X+overlap3Y>=2) and (overlap3X*overlap3Y != 0)):
            overlap3 = 1

        if overlap2 == 0 and overlap3 == 0:
          # DoppelDone #
          # The object
          back_im.paste(resizedDeformed_im2, (xminrD, yminrD), mask=resizedDeformed_im2)

          #overlappingPolys[iPoly,0] = xminrD # xmin
          #overlappingPolys[iPoly,1] = yminrD # ymin
          #overlappingPolys[iPoly,2] = xminrD + sxD # xmax
          #overlappingPolys[iPoly,3] = yminrD + syD # ymax

          for i5 in range(0, len(txtFile2t), 2):
            txtFile3[iPolyCount,i5]= int(((txtFile2t[i5]/sxR)*fx) - (xminrD0 - xmint)) # X point
            txtFile3[iPolyCount,i5+1]= int(((txtFile2t[i5+1]/syR)*fy) - (yminrD0 - ymint)) # Y point

          # Its back 1 and 2
          if pasteIn == 0:
            back_im.paste(dst, (xminrD+sxD+1, yminrD), mask=dst)
            back_im.paste(dst, (xminrD-sxD-1, yminrD), mask=dst)

            overlappingPolys[iPoly+1,0] = xminrD+sxD+1 # xmin
            overlappingPolys[iPoly+1,1] = yminrD # ymin
            overlappingPolys[iPoly+1,2] = xminrD+sxD+1 + sxD # xmax
            overlappingPolys[iPoly+1,3] = yminrD + syD # ymax

            overlappingPolys[iPoly+2,0] = xminrD-sxD-1 # xmin
            overlappingPolys[iPoly+2,1] = yminrD # ymin
            overlappingPolys[iPoly+2,2] = xminrD-sxD-1 + sxD # xmax
            overlappingPolys[iPoly+2,3] = yminrD + syD # ymax
          
          elif pasteIn == 1:
            back_im.paste(dst, (xminrD, yminrD+syD+1), mask=dst)
            back_im.paste(dst, (xminrD, yminrD-syD-1), mask=dst)

            overlappingPolys[iPoly+1,0] = xminrD # xmin
            overlappingPolys[iPoly+1,1] = yminrD+syD+1 # ymin
            overlappingPolys[iPoly+1,2] = xminrD + sxD # xmax
            overlappingPolys[iPoly+1,3] = yminrD+syD+1 + syD # ymax

            overlappingPolys[iPoly+2,0] = xminrD # xmin
            overlappingPolys[iPoly+2,1] = yminrD-syD-1 # ymin
            overlappingPolys[iPoly+2,2] = xminrD + sxD # xmax
            overlappingPolys[iPoly+2,3] = yminrD-syD-1 + syD # ymax
          
          elif pasteIn == 2:
            back_im.paste(dst, (xminrD-sxD-1, yminrD), mask=dst)
            back_im.paste(dst, (xminrD+sxD+1, yminrD), mask=dst)

            overlappingPolys[iPoly+1,0] = xminrD-sxD-1 # xmin
            overlappingPolys[iPoly+1,1] = yminrD # ymin
            overlappingPolys[iPoly+1,2] = xminrD-sxD-1 + sxD # xmax
            overlappingPolys[iPoly+1,3] = yminrD + syD # ymax

            overlappingPolys[iPoly+2,0] = xminrD+sxD+1 # xmin
            overlappingPolys[iPoly+2,1] = yminrD # ymin
            overlappingPolys[iPoly+2,2] = xminrD+sxD+1 + sxD # xmax
            overlappingPolys[iPoly+2,3] = yminrD + syD # ymax
          
          else: # pasteIn == 3
            back_im.paste(dst, (xminrD, yminrD-syD-1), mask=dst)
            back_im.paste(dst, (xminrD, yminrD+syD+1), mask=dst)

            overlappingPolys[iPoly+1,0] = xminrD # xmin
            overlappingPolys[iPoly+1,1] = yminrD-syD-1 # ymin
            overlappingPolys[iPoly+1,2] = xminrD + sxD # xmax
            overlappingPolys[iPoly+1,3] = yminrD-syD-1 + syD # ymax

            overlappingPolys[iPoly+2,0] = xminrD # xmin
            overlappingPolys[iPoly+2,1] = yminrD+syD+1 # ymin
            overlappingPolys[iPoly+2,2] = xminrD + sxD # xmax
            overlappingPolys[iPoly+2,3] = yminrD+syD+1 + syD # ymax
          
          iPoly = iPoly + 3
          iPolyCount = iPolyCount + 1

      # Paste
      else: # doppel == 0
        back_im.paste(resizedDeformed_im2, (xminrD, yminrD), mask=resizedDeformed_im2)

        for i5 in range(0, len(txtFile2t), 2):
          txtFile3[iPolyCount,i5]= int(((txtFile2t[i5]/sxR)*fx) - (xminrD0 - xmint)) # X point
          txtFile3[iPolyCount,i5+1]= int(((txtFile2t[i5+1]/syR)*fy) - (yminrD0 - ymint)) # Y point
        iPoly = iPoly + 1
        iPolyCount = iPolyCount + 1

    if iPolyCount == cropImagesPerBackImages:
      break
    elif time.time() > timeout:
      print("Timeout: Cannot create synthetic images with more than %d objects for selected DA conditions" %iPolyCount)
      sys.exit()
      
  np.savetxt("4_DA/synthetic/synthAux%d.txt" %i3, txtFile3, fmt='%d', delimiter=' ')
  back_im.save("4_DA/synthetic/synth%d.png" %i3, quality=100)
  back_im.save("1_PNG/img/synth%d.png" %i3,"PNG")
  back_im.save("1_PNG/train/synth%d.png" %i3,"PNG")
  print('synth%d image done' %i3)

print("Synthetic image created")

# VGG IMAGE ANNOTATOR FORMAT

for i6 in range(backImagesNumberIni, backImagesNumber+1, 1):
  txtFile3 = np.loadtxt("4_DA/synthetic/synthAux%d.txt" %i6, dtype=int)
  txtFile4 = np.zeros(shape=(cropImagesPerBackImages*2,maxPointsNumber))
  if cropImagesPerBackImages == 1:
    col3 = txtFile3.shape
    row3 = 1
    col3 = col3[0]
    for i8 in range(0, math.trunc((col3/2))-1, 1):
        txtFile4[0,i8]=txtFile3[i8*2]
        txtFile4[1,i8]=txtFile3[(i8*2)+1]
  else:
    row3, col3 = txtFile3.shape
    for i7 in range(0, row3*2, 2):
      for i8 in range(0, math.trunc((col3/2))-1, 1):
          txtFile4[i7,i8]=txtFile3[int(i7/2),i8*2]
          txtFile4[i7+1,i8]=txtFile3[int(i7/2),(i8*2)+1]

  np.savetxt("2_Polygons/prepro/synth%d_prepro.txt" %i6, txtFile4, fmt='%d', delimiter=' ')
  os.remove('4_DA/synthetic/synthAux%d.txt' %i6)
  print('synth%d data done' %i6)

print("Synthetic data created")


print('DONE')
