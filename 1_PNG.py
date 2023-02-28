# Convert JSON to TXT file #

import cv2
import os
import glob

path=os.path.abspath(os.getcwd())

if not os.path.exists('1_PNG/txt'):
  os.mkdir('1_PNG/txt')

pathJSON=os.path.join(path,'1_PNG/json')
for filenameR in glob.glob("1_PNG/json/.*"):
    os.remove(filenameR)
file_list=os.listdir(pathJSON)
file_list=sorted(file_list)

for iFile in range(0,len(file_list),1):
	mylines = []
	mylines2 = []
	[imName,imExt] = os.path.splitext("%s" %file_list[iFile])
	with open ('1_PNG/json/%s' %file_list[iFile], 'rt') as myfile: # Open txt file for reading text data.
	    for myline in myfile:
	    	mylines.append(myline)
	with open('1_PNG/txt/%s.txt' %imName, 'w') as f:
    		f.write(mylines[0]);

print('DONE')