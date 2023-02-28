# Creation of training, validation and test datasets, only the labeled images #

import numpy as np
import os
import glob
import cv2

trainVal = 0 # 0: To create training data
			# 1: To create validation data
			# 2: To create test data

# Helper function to perform sort
def num_sort(test_string):
    return list(map(int, re.findall(r'(?<=split_)\d+', test_string)))[0]

mylines=[]
if trainVal == 0:
	if not os.path.exists('7_Data/train'):
		os.mkdir('7_Data/train')	
	with open('6_Merge/train/dataset/via_region_data.json', 'rt') as f:
	    for myline in f:
		    mylines.append(myline)
elif trainVal == 1:
	if not os.path.exists('7_Data/val'):
		os.mkdir('7_Data/val')
	with open('6_Merge/val/dataset/via_region_data.json', 'rt') as f:
	    for myline in f:
		    mylines.append(myline) 
else:
	if not os.path.exists('7_Data/test'):
		os.mkdir('7_Data/test')
	with open('6_Merge/test/dataset/via_region_data.json', 'rt') as f:
	    for myline in f:
		    mylines.append(myline) 

mylines[0]=mylines[0].replace('"filename":"', '¿')
mylines[0]=mylines[0].replace('.jpg"', '?')
mylines[0]=mylines[0].replace('"regions":[]', '!')

b=mylines[0]
c = np.zeros(shape=(len(b),1))
c = c.astype(str)
num=0
i3=b.find("¿")
i0=i3
iW=0
for i in range(i3+1,len(b),1):
	if b[i]=='¿':
		ie=i
		for i2 in range(i0,ie,1):
			if b[i2]=='?':
				iN=i2
			if b[i2]=='!':
				iW=1
		if iW==0:
			c[num,0]=b[i0+1:iN]
			num=num+1
		iW=0
		i0=ie

ie2=0
for i4 in range(0,len(c),1):
	if c[i4,0]=='0.0' and ie2==0:
		ie2=i4

c=c[0:ie2,:]

if trainVal == 0:
	for i in range(0,len(c),1):
		img = cv2.imread('6_Merge/train/dataset/%s.jpg' %c[i][0])
		cv2.imwrite('7_Data/train/%s.jpg' %c[i][0], img)	
elif trainVal == 1:
	for i in range(0,len(c),1):
		img = cv2.imread('6_Merge/val/dataset/%s.jpg' %c[i][0])
		cv2.imwrite('7_Data/val/%s.jpg' %c[i][0], img)
else:
	for i in range(0,len(c),1):
		img = cv2.imread('6_Merge/test/dataset/%s.jpg' %c[i][0])
		cv2.imwrite('7_Data/test/%s.jpg' %c[i][0], img)

# Create the associated JSON file

mylinesUnited =[]
mylinesUnited1 =[]
mylinesUnited2 =[]

path=os.path.abspath(os.getcwd())
if trainVal == 0:
	pathDataImg=os.path.join(path,'7_Data/train')
	for filenameR in glob.glob("7_Data/train/.*"):
		os.remove(filenameR)
elif trainVal == 1:
	pathDataImg=os.path.join(path,'7_Data/val')
	for filenameR in glob.glob("7_Data/val/.*"):
		os.remove(filenameR)
else:
	pathDataImg=os.path.join(path,'7_Data/test')
	for filenameR in glob.glob("7_Data/test/.*"):
		os.remove(filenameR)
file_list=os.listdir(pathDataImg)
file_list=sorted(file_list)

for i1 in range(0,len(file_list),1):

	if trainVal == 0:
		img = cv2.imread('7_Data/train/%s' %file_list[i1])
	elif trainVal == 1:
		img = cv2.imread('7_Data/val/%s' %file_list[i1])
	else:
		img = cv2.imread('7_Data/test/%s' %file_list[i1])
	height, width, channels = img.shape

	originalSizeX=width; originalSizeY=height; num=0; num2=0;
	numMaxImage=1
	imageFileSize=np.zeros(shape=(1,numMaxImage))
	[imName1,imExt] = os.path.splitext("%s" %file_list[i1])
	imName = imName1.split('_split_')[0]
	imNameSplitNum = imName1.split('_split_')[1]

	with open ('5_Split/%s_divided.txt' %imName, 'rt') as myfile: # Open txt file for reading text data.
	    for mylineDivided in myfile:              # For each line, stored as myline,
	        iX = 0
	        mylineDivided=mylineDivided.replace(',0',''); mylineDivided=mylineDivided.replace('55555,66666,99999','X'); mylineDivided=mylineDivided.replace('55555,',',"regions":[{"shape_attributes":{"name":"polygon","all_points_x":['); mylineDivided=mylineDivided.replace(',66666,','],"all_points_y":['); mylineDivided=mylineDivided.replace(',77777,',']},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}},{"shape_attributes":{"name":"polygon","all_points_x":['); mylineDivided=mylineDivided.replace(',99999',']},"region_attributes":{"name":"not_defined","type":"unknown","image_quality":{"good":true,"frontal":true,"good_illumination":true}}}],"file_attributes":{"caption":"","public_domain":"no","image_url":""}},');
	        if num2 == int(imNameSplitNum):
	        	pathTrainImg2=os.path.join(pathDataImg,'%s.jpg' %(imName1));
	        	mylinesUnited.append('\"' + str(imName1) + '.jpg' + str(int(os.path.getsize(pathTrainImg2))) + '":{"filename":"' + str(imName1) + '.jpg' + '","size":' + str(int(os.path.getsize(pathTrainImg2))) + str(mylineDivided))
	        num2 = num2 + 1

	mylinesUnited1=''.join(mylinesUnited);
	mylinesUnited =[]
	mylinesUnited1=mylinesUnited1.replace ('\n', '')

	mylinesUnited2.append(mylinesUnited1)

# Merge the JSON files

mylinesUnited3=''.join(mylinesUnited2);
mylinesUnited3=mylinesUnited3.replace ('\n', '')
mylinesUnited3='{'+mylinesUnited3+'+}+'
mylinesUnited3=mylinesUnited3.replace (',+}+', '}')

if trainVal == 0:
	print("Training data created")
	with open('7_Data/train/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)
elif trainVal == 1:
	print("Validation data created")
	with open('7_Data/val/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)
else:
	print("Test data created")
	with open('7_Data/test/via_region_data.json', 'w') as f:
	    f.write(mylinesUnited3)
