# Creation of training, validation and test datasets #

import numpy as np
import cv2
import os
import glob
import re

# Helper function to perform sort
def num_sort(test_string):
    return list(map(int, re.findall(r'(?<=split_)\d+', test_string)))[0]

tesela = 512 # Image size to train, validate, test and detect in pixels
trainVal = 0 # 0: To create training data
			# 1: To create validation data
			# 2: To create test data

path=os.path.abspath(os.getcwd())

if trainVal == 0:
	pathDataImg=os.path.join(path,'1_PNG/train')
	for filenameR in glob.glob("1_PNG/train/.*"):
    		os.remove(filenameR)
elif trainVal == 1:
	pathDataImg=os.path.join(path,'1_PNG/val')
	for filenameR in glob.glob("1_PNG/val/.*"):
    		os.remove(filenameR)
else:
	pathDataImg=os.path.join(path,'1_PNG/test')
	for filenameR in glob.glob("1_PNG/test/.*"):
    		os.remove(filenameR)

pathTrain=os.path.join(path,'6_Merge')
file_list=os.listdir(pathDataImg)
file_list=sorted(file_list)
mylinesUnited2 =[]

if trainVal == 0:
	if not os.path.exists('6_Merge/train'):
		os.mkdir('6_Merge/train')
		os.mkdir('6_Merge/train/dataset')
elif trainVal == 1:
	if not os.path.exists('6_Merge/val'):
		os.mkdir('6_Merge/val')
		os.mkdir('6_Merge/val/dataset')
else:
	if not os.path.exists('6_Merge/test'):
		os.mkdir('6_Merge/test')
		os.mkdir('6_Merge/test/dataset')

for i1 in range(0,len(file_list),1):
	
	if trainVal == 0:
		img = cv2.imread('1_PNG/train/%s' %file_list[i1])
	elif trainVal == 1:
		img = cv2.imread('1_PNG/val/%s' %file_list[i1])
	else:
		img = cv2.imread('1_PNG/test/%s' %file_list[i1])
	height, width, channels = img.shape

	originalSizeX=width; originalSizeY=height; num=0; num2=0;
	xMax=np.ceil(originalSizeX/tesela)
	yMax=np.ceil(originalSizeY/tesela)
	numMaxImage=int(xMax*yMax)
	imageFileSize=np.zeros(shape=(1,numMaxImage))

	[imName,imExt] = os.path.splitext("%s" %file_list[i1])

	if trainVal == 0:
		if not os.path.exists('6_Merge/train/%s' %imName):
	    		os.mkdir('6_Merge/train/%s' %imName)
	elif trainVal == 1:
		if not os.path.exists('6_Merge/val/%s' %imName):
	    		os.mkdir('6_Merge/val/%s' %imName)
	else:
		if not os.path.exists('6_Merge/test/%s' %imName):
	    		os.mkdir('6_Merge/test/%s' %imName)

	pathDataImg1=os.path.join(pathDataImg,file_list[i1])
	img = cv2.imread(pathDataImg1)
	
	# Split the image in tesela size images

	if trainVal == 0:
		pathTrainImgFolder=os.path.join(path,'6_Merge/train/%s' %imName)
		pathTrainTrain=os.path.join(path,'6_Merge/train/dataset')
	elif trainVal == 1:
		pathTrainImgFolder=os.path.join(path,'6_Merge/val/%s' %imName)
		pathTrainTrain=os.path.join(path,'6_Merge/val/dataset')
	else:
		pathTrainImgFolder=os.path.join(path,'6_Merge/test/%s' %imName)
		pathTrainTrain=os.path.join(path,'6_Merge/test/dataset')

	for i2 in range(0,originalSizeY,tesela):
		for j2 in range(0,originalSizeX,tesela):
			cropped_image = img[i2:i2+tesela, j2:j2+tesela]
			# Save the cropped image
			pathTrainImg1=os.path.join(pathTrainImgFolder,'%s_split_%d.jpg' %(imName,num))
			pathTrainTrainImg1=os.path.join(pathTrainTrain,'%s_split_%d.jpg' %(imName,num))
			cv2.imwrite(pathTrainImg1, cropped_image)
			cv2.imwrite(pathTrainTrainImg1, cropped_image)
			num=num+1

	# Create the associated JSON file

	mylinesUnited =[]
	mylinesUnited1 =[]
	mylinesDivided = []
	if trainVal == 0:
		for filenameR2 in glob.glob("6_Merge/train/%s/.*" %imName):
		    os.remove(filenameR2)
	elif trainVal == 1:
		for filenameR2 in glob.glob("6_Merge/val/%s/.*" %imName):
		    os.remove(filenameR2)
	else:
		for filenameR2 in glob.glob("6_Merge/test/%s/.*" %imName):
		    os.remove(filenameR2)
	file_list2=os.listdir(pathTrainImgFolder)
	file_list2.sort(key=num_sort) 
	with open ('5_Split/%s_divided.txt' %imName, 'rt') as myfile: # Open txt file for reading text data.
	    for mylineDivided in myfile:              # For each line, stored as myline,
	        mylineDivided=mylineDivided.replace(',0',''); mylineDivided=mylineDivided.replace('55555,66666,99999',',"regions":[],"file_attributes":{"caption":"","public_domain":"no","image_url":""}},'); mylineDivided=mylineDivided.replace('55555,',',"regions":[{"shape_attributes":{"name":"polygon","all_points_x":['); mylineDivided=mylineDivided.replace(',66666,','],"all_points_y":['); mylineDivided=mylineDivided.replace(',77777,',']},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}},{"shape_attributes":{"name":"polygon","all_points_x":['); mylineDivided=mylineDivided.replace(',99999',']},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}}],"file_attributes":{"caption":"","public_domain":"no","image_url":""}},');
	        pathTrainImg2=os.path.join(pathTrainImgFolder,'%s_split_%d.jpg' %(imName,num2));
	        imageFileSize[0,num2] = os.path.getsize(pathTrainImg2);
	        mylinesUnited.append('\"' + str(file_list2[num2]) + str(int(imageFileSize[0,num2])) + '":{"filename":"' + str(file_list2[num2]) + '","size":' + str(int(imageFileSize[0,num2])) + str(mylineDivided))
	        num2=num2+1

	mylinesUnited1=''.join(mylinesUnited);
	mylinesUnited1=mylinesUnited1.replace ('\n', '')

	mylinesUnited2.append(mylinesUnited1)

	mylinesUnited1='{'+mylinesUnited1+'+}+'
	mylinesUnited1=mylinesUnited1.replace (',+}+', '}')

	if trainVal == 0:
		with open('6_Merge/train/%s/via_region_data.json' %imName, 'w') as f:
		    f.write(mylinesUnited1)
	elif trainVal == 1:
		with open('6_Merge/val/%s/via_region_data.json' %imName, 'w') as f:
		    f.write(mylinesUnited1)
	else:
		with open('6_Merge/test/%s/via_region_data.json' %imName, 'w') as f:
		    f.write(mylinesUnited1)

	print('%s done' %file_list[i1])

# Merge the JSON files

mylinesUnited3=''.join(mylinesUnited2);
mylinesUnited3=mylinesUnited3.replace ('\n', '')
mylinesUnited3='{'+mylinesUnited3+'+}+'
mylinesUnited3=mylinesUnited3.replace (',+}+', '}')

if trainVal == 0:
	with open('6_Merge/train/dataset/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)
elif trainVal == 1:
	with open('6_Merge/val/dataset/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)
else:
	with open('6_Merge/test/dataset/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)

print('via_region_data.json done')


