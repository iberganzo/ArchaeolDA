# To create a database for Data Augmentation #
# To create new Data Augmentation images #

import numpy as np
import cv2
import re
import os
import glob

if not os.path.exists('3_Objects/DDBB'):
    os.mkdir('3_Objects/DDBB')
if not os.path.exists('3_Objects/DA'):
    os.mkdir('3_Objects/DA')

path=os.path.abspath(os.getcwd())
pathDataImg=os.path.join(path,'1_PNG/img')
for filenameR in glob.glob("1_PNG/img/.*"):
    os.remove(filenameR)
file_list=os.listdir(pathDataImg)
file_list=sorted(file_list)

pathDataImgTrain=os.path.join(path,'1_PNG/train')
for filenameR in glob.glob("1_PNG/train/.*"):
    os.remove(filenameR)
file_listT=os.listdir(pathDataImgTrain)
file_listT=sorted(file_listT)

pathDataImgCrop=os.path.join(path,'2_Polygons/preproToCrop')
for filenameR in glob.glob("2_Polygons/preproToCrop/.*"):
    os.remove(filenameR)
file_listC=os.listdir(pathDataImgCrop)
file_listC=sorted(file_listC)

# Crops for DDBB

i1=1;
for iFile in range(0,len(file_listC),1):
  # Open the JPG image with the objects and its associated preprocesed TXT file

  [imName,imExt] = os.path.splitext("%s" %file_listC[iFile])
  imName = imName[:-13]

  isInImg = 0;
  for iIs1 in range(0,len(file_list),1):
    [imNameImg,imExtImg] = os.path.splitext("%s" %file_list[iIs1])
    if imNameImg == imName:
      isInImg = 1
      imNameImg1 = imNameImg
      imExtImg1 = imExtImg

  if isInImg == 1:
    img = cv2.imread("1_PNG/img/%s%s" %(imNameImg1,imExtImg1))
    height, width, channels = img.shape
    sizeX = width # Objects image pixel size in x axis
    sizeY = height # Objects image pixel size in y axis

    mylines = []                             # Declare an empty list named mylines.
    with open ('2_Polygons/preproToCrop/%s_preproToCrop.txt' %imName, 'rt') as myfile: # Open txt file for reading text data.
        for myline in myfile:                # For each line, stored as myline,
            mylines.append(myline)           # add its contents to mylines.

    # Crop the objects

    for i0 in range(0, len(mylines), 1):

      mylinesNumbers = []
      mylinesNormalized = []

      pts = np.matrix("[%s]" % mylines[i0])
        
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
      
    # Crop the associated polygon data for each cropped object

      mylinesNumbers = re.sub("[\]]", ",", mylines[i0].split()[0])
      mylinesNumbers = re.sub("[\[]", "", mylinesNumbers)
      mylinesNumbers = re.sub("[;]", "", mylinesNumbers)
      mylinesNumbers = mylinesNumbers[:-1]

      mylinesNumbers = "%s" % mylinesNumbers
      mylinesNumbersSize = mylinesNumbers.count(",")

      for i2 in range(0, mylinesNumbersSize, 2):
        mylinesNormalized.append(int(mylinesNumbers.split(",")[i2].strip()))
        mylinesNormalized.append(int(mylinesNumbers.split(",")[i2+1].strip()))
      	# mylinesNormalized.append(int(mylinesNumbers.split(",")[i2].strip())/sizeX) # Normalized
      	# mylinesNormalized.append(int(mylinesNumbers.split(",")[i2+1].strip())/sizeY) # Normalized

    # Save the polygon data into a TXT file

      with open("3_Objects/DDBB/crop%d.txt" %i1, "w") as f:
        for s in mylinesNormalized:
            f.write(str(s) +" ")
      f.close()

    # Save the polygon object into a PNG file

      cv2.imwrite(os.path.join('3_Objects/DDBB', "crop%d.png" %i1),dst)
      i1=i1+1

    print('%s for DDBB done' %imName)

# Crops for DA

i1=1;
for iFile in range(0,len(file_listC),1):
  # Open the JPG image with the objects and its associated preprocesed TXT file

  [imName,imExt] = os.path.splitext("%s" %file_listC[iFile])
  imName = imName[:-13]

  isInImgT = 0;
  for iIs2 in range(0,len(file_listT),1):
    [imNameImgT,imExtImgT] = os.path.splitext("%s" %file_listT[iIs2])
    if imNameImgT == imName:
      isInImgT = 1
      imNameImgT1 = imNameImgT
      imExtImgT1 = imExtImgT

  if isInImgT == 1:
    img = cv2.imread("1_PNG/img/%s%s" %(imNameImgT1,imExtImgT1))
    height, width, channels = img.shape
    sizeX = width # Objects image pixel size in x axis
    sizeY = height # Objects image pixel size in y axis

    mylines = []                             # Declare an empty list named mylines.
    with open ('2_Polygons/preproToCrop/%s_preproToCrop.txt' %imName, 'rt') as myfile: # Open txt file for reading text data.
        for myline in myfile:                # For each line, stored as myline,
            mylines.append(myline)           # add its contents to mylines.

    # Crop the objects

    for i0 in range(0, len(mylines), 1):

      mylinesNumbers = []
      mylinesNormalized = []

      pts = np.matrix("[%s]" % mylines[i0])
        
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
      
    # Crop the associated polygon data for each cropped object

      mylinesNumbers = re.sub("[\]]", ",", mylines[i0].split()[0])
      mylinesNumbers = re.sub("[\[]", "", mylinesNumbers)
      mylinesNumbers = re.sub("[;]", "", mylinesNumbers)
      mylinesNumbers = mylinesNumbers[:-1]

      mylinesNumbers = "%s" % mylinesNumbers
      mylinesNumbersSize = mylinesNumbers.count(",")

      for i2 in range(0, mylinesNumbersSize, 2):
        mylinesNormalized.append(int(mylinesNumbers.split(",")[i2].strip()))
        mylinesNormalized.append(int(mylinesNumbers.split(",")[i2+1].strip()))
        # mylinesNormalized.append(int(mylinesNumbers.split(",")[i2].strip())/sizeX) # Normalized
        # mylinesNormalized.append(int(mylinesNumbers.split(",")[i2+1].strip())/sizeY) # Normalized

    # Save the polygon data into a TXT file

      with open("3_Objects/DA/crop%d.txt" %i1, "w") as f:
        for s in mylinesNormalized:
            f.write(str(s) +" ")
      f.close()

    # Save the polygon object into a PNG file

      cv2.imwrite(os.path.join('3_Objects/DA', "crop%d.png" %i1),dst)
      i1=i1+1

    print('%s for DA done' %imName)


print('DONE')
