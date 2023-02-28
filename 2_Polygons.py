# Changing how polygons data is presented for polygon cropping algorithm #

import numpy as np
import cv2
import re
import os
import glob

path=os.path.abspath(os.getcwd())
pathDataImg=os.path.join(path,'1_PNG/img')
pathDataTXT=os.path.join(path,'1_PNG/txt')
if not os.path.exists('2_Polygons/prepro'):
  os.mkdir('2_Polygons/prepro')
if not os.path.exists('2_Polygons/preproToCrop'):
  os.mkdir('2_Polygons/preproToCrop')

for filenameR in glob.glob("1_PNG/img/.*"):
    os.remove(filenameR)
file_list=os.listdir(pathDataImg)
file_list=sorted(file_list)

for filenameR in glob.glob("1_PNG/txt/.*"):
    os.remove(filenameR)
file_list3=os.listdir(pathDataTXT)
file_list3=sorted(file_list3)

for iFile in range(0,len(file_list3),1):
	
	os.chdir(path)

	# Open via_region_data TXT file

	[imName,imExt] = os.path.splitext("%s" %file_list3[iFile])
	mylines = []; mylinesNumbers=[]; i2=0; i3=0; i5=-1; zeroPos=0; zeroPos2=0; # Declare an empty list named mylines.
	with open ('1_PNG/txt/%s' %file_list3[iFile], 'rt') as myfile: # Open txt file for reading text data.
	    for myline in myfile:                # For each line, stored as myline,
	        mylines.append(myline)           # add its contents to mylines.

	# Change the way polygons data is presented

	[myFileToDel,myFileToSave] = mylines[0].split('regions')

	mylines[0]=mylines[0].replace(',"all_points_x":', '')
	mylines[0]=mylines[0].replace(',"all_points_y":', '')
	mylines[0]=mylines[0].replace('},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}},{"shape_attributes":{"name":"polygon"', '')
	mylines[0]=mylines[0].replace('},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}}],"file_attributes":{"caption":"","public_domain":"no","image_url":""}}}', '')
	mylines[0]=mylines[0].replace(myFileToDel,'')
	mylines[0]=mylines[0].replace('regions":[{"shape_attributes":{"name":"polygon"', '')
	mylines[0]=mylines[0].replace('[', '[,')
	mylines[0]=mylines[0].replace(']', ',],')

	mylinesNumbersSize1 = mylines[0].count("[")
	mylinesNumbersSize2 = mylines[0].count(",")
	mylinesNumbers = np.zeros(shape=(mylinesNumbersSize1,mylinesNumbersSize2))

	for i1 in range(0, mylinesNumbersSize2, 1):
		if mylines[0].split(",")[i1].strip() == ']':
			i2=i2+1; i3=0;
		elif mylines[0].split(",")[i1].strip() == '[' or mylines[0].split(",")[i1].strip() == '':
			jump=1
		else:
			mylinesNumbers[i2,i3]=int(mylines[0].split(",")[i1].strip())
			i3=i3+1

	row, col = mylinesNumbers.shape
	for j1 in range(0, col-1, 1):
		if np.mean(mylinesNumbers[:,j1]) == 0 and zeroPos == 0:
			zeroPos=j1
	mylinesNumbers = mylinesNumbers[:,0:zeroPos];
	mylinesNumbers = mylinesNumbers.astype(int)

	np.savetxt("2_Polygons/prepro/%s_prepro.txt" %imName, mylinesNumbers, fmt="%d", delimiter=" ")

	row2, col2 = mylinesNumbers.shape
	col2 = col2 + 1
	mylinesNumbersI = np.zeros(shape=(int(row2/2),col2))
	mylinesNumbersB = mylinesNumbersI.astype(str)
	for i4 in range(0, row2-1, 2):
		i5 = i5 + 1
		for j4 in range(0, col2-1, 1):
			if mylinesNumbers[i4,j4] != 0:
				mylinesNumbersB[i5,j4] = '[' + str(mylinesNumbers[i4,j4]) + ',' + str(mylinesNumbers[i4+1,j4]) + ']'

	# Save the polygon data

	row6, col6 = mylinesNumbersB.shape
	for i6 in range(0, row6, 1):
		i7=i6+1
		for j6 in range(0, col6, 1):
			if mylinesNumbersB[i6,j6] == '0.0' and zeroPos2 == 0:
				zeroPos2=j6
		np.savetxt("2_Polygons/%d.txt" %i6, [mylinesNumbersB[i6,0:zeroPos2]], fmt="%s", delimiter=";")
		zeroPos2=0

	os.chdir(os.path.join(os.path.abspath(os.getcwd()),'2_Polygons'))

	filenames = list(range(row6))

	for i8 in range(0, len(filenames), 1):
		filenames[i8] = str(filenames[i8]) + '.txt'


	with open("preproToCrop/%s_preproToCrop.txt" %imName, "w") as outfile:
	    for filename in filenames:
	        with open(filename) as infile:
	            contents = infile.read()
	            outfile.write(contents)

	for i8 in range(0, len(filenames), 1):
		os.remove(os.path.join(os.path.abspath(os.getcwd()),'%d.txt' %i8))

	print('%s done' %imName)

print('DONE')

