# Divide in smaller images #

import numpy as np
import cv2
import os
import glob

tesela = 512 # Image size to train, validate, test and detect in pixels
addPointsNumber = 8 # Number of points between labeled points

def getEquidistantPoints(p1, p2, parts):
	
	#To create more points in the polygon	

	xL=np.linspace(p1[0], p2[0], parts+1)
	yL=np.linspace(p1[1], p2[1], parts+1)
	
	#To improve the outline of a polygon

	for icount in range(0,addPointsNumber,1):
		for iL in range(1,len(xL),1):
			if iL+1 < len(xL):
				if int(xL[iL+1])-int(xL[iL])==1 and int(yL[iL+1])-int(yL[iL])==0:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)
			if iL+2 < len(xL):
				if int(xL[iL+2])-int(xL[iL])==2 and int(yL[iL+2])-int(yL[iL])==1:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)
		for iL in range(1,len(yL),1):
			if iL+1 < len(yL):
				if int(yL[iL+1])-int(yL[iL])==1 and int(xL[iL+1])-int(xL[iL])==0:
					yL = np.delete(yL, iL+1)
					xL = np.delete(xL, iL+1)
			if iL+2 < len(yL):
				if int(yL[iL+2])-int(yL[iL])==2 and int(xL[iL+2])-int(xL[iL])==1:
					yL = np.delete(yL, iL+1)
					xL = np.delete(xL, iL+1)

		for iL in range(0,len(yL),1):
			if len(yL)==iL+2:
				if int(xL[iL+1])-int(xL[iL])==0 and int(yL[0])-int(yL[iL+1])==0:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)
			elif iL+1 < len(yL):
				if int(xL[iL+1])-int(xL[iL])==0 and int(yL[iL+2])-int(yL[iL+1])==0:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)
		for iL in range(0,len(xL),1):
			if len(xL)==iL+2:
				if int(yL[iL+1])-int(yL[iL])==0 and int(xL[0])-int(xL[iL+1])==0:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)
			elif iL+1 < len(xL):
				if int(yL[iL+1])-int(yL[iL])==0 and int(xL[iL+2])-int(xL[iL+1])==0:
					xL = np.delete(xL, iL+1)
					yL = np.delete(yL, iL+1)

	return zip(xL,
               yL)

path=os.path.abspath(os.getcwd())
pathDataImg=os.path.join(path,'1_PNG/img')
for filenameR in glob.glob("1_PNG/img/.*"):
    os.remove(filenameR)
file_list=os.listdir(pathDataImg)
file_list=sorted(file_list)

for iFile in range(0,len(file_list),1):
	
	img = cv2.imread('1_PNG/img/%s' %file_list[iFile])
	height, width, channels = img.shape

	[imName,imExt] = os.path.splitext("%s" %file_list[iFile])

	txtFile4A0 = np.loadtxt("2_Polygons/prepro/%s_prepro.txt" %imName, dtype=int)

	originalSizeX=width; originalSizeY=height; pos=0; pos2=0; pos3=0; j3=1; count=1; zeroPos=0;

	xMax=np.ceil(originalSizeX/tesela)
	yMax=np.ceil(originalSizeY/tesela)
	iTeselaMax=int(max(xMax,yMax))
	numMaxImage=int(xMax*yMax)
	row4_0, col4_0 = txtFile4A0.shape
	txtFile4AP = np.zeros(shape=(row4_0,int((col4_0*(addPointsNumber))+2)))

	# Add points to the object polygons

	txtFile4B0 = np.zeros(shape=(row4_0,col4_0))
	txtFile4C0 = np.zeros(shape=(row4_0,col4_0))
	txtFile4C0Check = np.zeros(shape=(row4_0,1))
	for i7 in range(0, row4_0, 1):
		for j7 in range(0, col4_0, 1):
			for iTesela in range(1, iTeselaMax, 1):
				if txtFile4A0[i7,j7] == (tesela*iTesela):
					txtFile4A0[i7,j7] = (tesela*iTesela)-1
			if txtFile4A0[i7,j7] <= 0 and txtFile4A0[i7,j7] != -9999:
				txtFile4A0[i7,j7] = 1
			if txtFile4A0[i7,j7] == -9999:
				txtFile4A0[i7,j7] = 0
	for i7 in range(0, row4_0, 2):
		for j7 in range(0, col4_0, 1):
			if txtFile4A0[i7,j7] >= originalSizeX:
				txtFile4A0[i7,j7] = originalSizeX - 1
			if txtFile4A0[i7+1,j7] >= originalSizeY:
				txtFile4A0[i7+1,j7] = originalSizeY - 1

	for i8 in range(0, row4_0, 1):
		for j8 in range(0, col4_0, 1):
			if txtFile4A0[i8,j8] != 0:
				num=(txtFile4A0[i8,j8]/tesela)
				txtFile4B0[i8,j8]=(num-np.fix(num))*tesela
				if np.remainder(i8,2)==0:
					num1=np.ceil((txtFile4A0[i8,j8]/tesela))
					num2=np.ceil((txtFile4A0[i8+1,j8]/tesela)); numImage=(xMax*(num2-1))+num1; txtFile4C0[i8,j8]=numImage; txtFile4C0[i8+1,j8]=numImage;

	for iChck in range(0, row4_0, 1):
		chkd=0
		for jChck in range(0, col4_0, 1):
			if txtFile4C0[iChck,jChck]==0 and chkd==0:
				if len(set(txtFile4C0[iChck,0:jChck]))==1:
					txtFile4C0Check[iChck,0]=0
				else:
					txtFile4C0Check[iChck,0]=1 #Object polygon to be cropped
				chkd=1

	for iP in range(0, row4_0, 2):
		if txtFile4C0Check[iP,0]==1:
			txtFile4AP[iP,0] = txtFile4A0[iP,0]
			txtFile4AP[iP+1,0] = txtFile4A0[iP+1,0]
			numjP=1
			for jP in range(0, col4_0-1, 1):
				if txtFile4A0[iP,jP+1] != 0:
					addPoints =	list(getEquidistantPoints((txtFile4A0[iP,jP],txtFile4A0[iP+1,jP]), (txtFile4A0[iP,jP+1],txtFile4A0[iP+1,jP+1]), addPointsNumber))
					for iP2 in range(1,len(addPoints),1):
						txtFile4AP[iP,numjP] = int(addPoints[iP2][0])
						txtFile4AP[iP+1,numjP] = int(addPoints[iP2][1])
						numjP=numjP+1
				elif txtFile4A0[iP,jP+1] == 0 and txtFile4A0[iP,jP] != 0:
					addPoints =	list(getEquidistantPoints((txtFile4A0[iP,jP],txtFile4A0[iP+1,jP]), (txtFile4A0[iP,0],txtFile4A0[iP+1,0]), addPointsNumber))
					for iP2 in range(1,len(addPoints),1):
						txtFile4AP[iP,numjP] = int(addPoints[iP2][0])
						txtFile4AP[iP+1,numjP] = int(addPoints[iP2][1])
						numjP=numjP+1
		else:
			for jP2 in range(0, col4_0, 1):
				txtFile4AP[iP,jP2] = txtFile4A0[iP,jP2]
				txtFile4AP[iP+1,jP2] = txtFile4A0[iP+1,jP2]

	# Divide the object polygon image in teselas

	txtFile4A=txtFile4AP
	row4, col4 = txtFile4A.shape
	txtFile4B = np.zeros(shape=(row4,col4))
	txtFile4C = np.zeros(shape=(row4,col4))
	txtFile4E = np.zeros(shape=(row4,col4))
	txtFile4R = np.zeros(shape=(1,numMaxImage))

	for i7 in range(0, row4, 1):
		for j7 in range(0, col4, 1):
			for iTesela in range(1, iTeselaMax, 1):
				if txtFile4A[i7,j7] == (tesela*iTesela):
					txtFile4A[i7,j7]=(tesela*iTesela)-1

	for i8 in range(0, row4, 1):
		for j8 in range(0, col4, 1):
			if txtFile4A[i8,j8] != 0:
				num=(txtFile4A[i8,j8]/tesela)
				txtFile4B[i8,j8]=(num-np.fix(num))*tesela
				if np.remainder(i8,2)==0:
					num1=np.ceil((txtFile4A[i8,j8]/tesela))
					num2=np.ceil((txtFile4A[i8+1,j8]/tesela)); numImage=(xMax*(num2-1))+num1; txtFile4C[i8,j8]=numImage; txtFile4C[i8+1,j8]=numImage;

	txtFile4B = np.hstack([txtFile4B,np.zeros(shape=(row4,4))])
	txtFile4C = np.hstack([txtFile4C,np.zeros(shape=(row4,4))])
	row4C, col4C = txtFile4C.shape
	for iC in range(0, row4C, 2):
		numC=0; numJ=np.zeros(shape=(1,4)); Z=np.zeros(shape=(1,4)); Z[0,0]=txtFile4C[iC,1];
		for jC in range(0, col4C-1, 1):
			if txtFile4C[iC,jC] != 0 and txtFile4C[iC,jC+1] != 0:
				if txtFile4C[iC,jC] != txtFile4C[iC,jC+1]:
					if txtFile4C[iC,int(numJ[0,0])] != txtFile4C[iC,jC+1]:
						if txtFile4C[iC,int(numJ[0,1])] != txtFile4C[iC,jC+1]:
							if txtFile4C[iC,int(numJ[0,2])] != txtFile4C[iC,jC+1]:
								if txtFile4C[iC,int(numJ[0,3])] != txtFile4C[iC,jC+1]:
									numJ[0,numC]=jC+1;
									if txtFile4C[iC,1] != txtFile4C[iC,jC+1]:
										numC=numC+1;
										if numC >= 4:
											print("Some problem found with %s_prepro.txt file. If the object size is larger than the tesela, increase the tesela size to make it larger. If not recreate the %s.png synthetic image." %(imName,imName))
										else:
											Z[0,numC]=txtFile4C[iC,jC+1];
								else:
									numJ[0,3]=jC+1;
							else:
								numJ[0,2]=jC+1;
						else:
							numJ[0,1]=jC+1;
					else:
						numJ[0,0]=jC+1;

		numJ[0]=numJ[0][Z[0].argsort()]
		Z.sort()
		numZa=0; numZb=0; numZc=0; numZd=0;
		Zax=np.zeros(shape=(1,1)); Zay=np.zeros(shape=(1,1));
		Zbx=np.zeros(shape=(1,1)); Zby=np.zeros(shape=(1,1));
		Zcx=np.zeros(shape=(1,1)); Zcy=np.zeros(shape=(1,1));
		Zdx=np.zeros(shape=(1,1)); Zdy=np.zeros(shape=(1,1));
		if numC==3:
			jNum=0
			for iJ in range(0, 4, 1):
				if numJ[0,iJ]==0:
					for jC in range(0, col4C, 1):
						if txtFile4C[iC,jC] == 0 and jNum == 0:
							jNum=jC
					numJ[0,iJ]=jNum
			for jC in range(0, col4C, 1):
				if txtFile4C[iC,jC] == Z[0,0]:
					Zax = np.hstack([Zax,np.zeros(shape=(1,1))])
					Zay = np.hstack([Zay,np.zeros(shape=(1,1))])
					Zax[0,numZa] = txtFile4B[iC,jC]
					Zay[0,numZa] = txtFile4B[iC+1,jC]
					numZa=numZa+1
				if txtFile4C[iC,jC] == Z[0,1]:
					Zbx = np.hstack([Zbx,np.zeros(shape=(1,1))])
					Zby = np.hstack([Zby,np.zeros(shape=(1,1))])
					Zbx[0,numZb] = txtFile4B[iC,jC]
					Zby[0,numZb] = txtFile4B[iC+1,jC]
					numZb=numZb+1
				if txtFile4C[iC,jC] == Z[0,2]:
					Zcx = np.hstack([Zcx,np.zeros(shape=(1,1))])
					Zcy = np.hstack([Zcy,np.zeros(shape=(1,1))])
					Zcx[0,numZc] = txtFile4B[iC,jC]
					Zcy[0,numZc] = txtFile4B[iC+1,jC]
					numZc=numZc+1
				if txtFile4C[iC,jC] == Z[0,3]:
					Zdx = np.hstack([Zdx,np.zeros(shape=(1,1))])
					Zdy = np.hstack([Zdy,np.zeros(shape=(1,1))])
					Zdx[0,numZd] = txtFile4B[iC,jC]
					Zdy[0,numZd] = txtFile4B[iC+1,jC]
					numZd=numZd+1
			Zax=np.delete(Zax, -1); Zay=np.delete(Zay, -1);
			Zbx=np.delete(Zbx, -1); Zby=np.delete(Zby, -1);
			Zcx=np.delete(Zcx, -1); Zcy=np.delete(Zcy, -1);
			Zdx=np.delete(Zdx, -1); Zdy=np.delete(Zdy, -1);
			Za=np.zeros(shape=(1,2)); Za[0,0]=max(Zax);  Za[0,1]=max(Zay);
			Zb=np.zeros(shape=(1,2)); Zb[0,0]=min(Zbx);  Zb[0,1]=max(Zby);
			Zc=np.zeros(shape=(1,2)); Zc[0,0]=max(Zcx);  Zc[0,1]=min(Zcy);
			Zd=np.zeros(shape=(1,2)); Zd[0,0]=min(Zdx);  Zd[0,1]=min(Zdy);

			addPointZa=1; addPointZb=1; addPointZc=1; addPointZd=1;
			if len(Zax)==2:
				for iZa in range(0,len(Zax),1):
					if Zax[iZa] == Za[0,0] and Zay[iZa] == Za[0,1]:
						addPointZa=0
			elif len(Zax)==1:
				addPointZa=0
			else:
				addPointZa=1
			if len(Zbx)==2:
				for iZb in range(0,len(Zbx),1):
					if Zbx[iZb] == Zb[0,0] and Zby[iZb] == Zb[0,1]:
						addPointZb=0
			elif len(Zbx)==1:
				addPointZb=0
			else:
				addPointZb=1
			if len(Zcx)==2:
				for iZc in range(0,len(Zcx),1):
					if Zcx[iZc] == Zc[0,0] and Zcy[iZc] == Zc[0,1]:
						addPointZc=0
			elif len(Zcx)==1:
				addPointZc=0
			else:
				addPointZc=1
			if len(Zdx)==2:
				for iZd in range(0,len(Zdx),1):
					if Zdx[iZd] == Zd[0,0] and Zdy[iZd] == Zd[0,1]:
						addPointZd=0
			elif len(Zdx)==1:
				addPointZd=0
			else:
				addPointZd=1

			if addPointZa == 1:		
				txtFile4B[iC,int(numJ[0,0])+1:-4]=txtFile4B[iC,int(numJ[0,0]):-5]; txtFile4B[iC+1,int(numJ[0,0])+1:-4]=txtFile4B[iC+1,int(numJ[0,0]):-5];
				txtFile4C[iC,int(numJ[0,0])+1:-4]=txtFile4C[iC,int(numJ[0,0]):-5]; txtFile4C[iC+1,int(numJ[0,0])+1:-4]=txtFile4C[iC+1,int(numJ[0,0]):-5];
				txtFile4B[iC,int(numJ[0,0])]=Za[0,0]; txtFile4B[iC+1,int(numJ[0,0])]=Za[0,1]; txtFile4C[iC,int(numJ[0,0])]=Z[0,0]; txtFile4C[iC+1,int(numJ[0,0])]=Z[0,0];
				if numJ[0,1]>=numJ[0,0]:
					numJ[0,1]=numJ[0,1]+1
				if numJ[0,2]>=numJ[0,0]:
					numJ[0,2]=numJ[0,2]+1
				if numJ[0,3]>=numJ[0,0]:
					numJ[0,3]=numJ[0,3]+1
			
			if addPointZb == 1:
				txtFile4B[iC,int(numJ[0,1])+1:-3]=txtFile4B[iC,int(numJ[0,1]):-4]; txtFile4B[iC+1,int(numJ[0,1])+1:-3]=txtFile4B[iC+1,int(numJ[0,1]):-4];
				txtFile4C[iC,int(numJ[0,1])+1:-3]=txtFile4C[iC,int(numJ[0,1]):-4]; txtFile4C[iC+1,int(numJ[0,1])+1:-3]=txtFile4C[iC+1,int(numJ[0,1]):-4];
				txtFile4B[iC,int(numJ[0,1])]=Zb[0,0]; txtFile4B[iC+1,int(numJ[0,1])]=Zb[0,1]; txtFile4C[iC,int(numJ[0,1])]=Z[0,1]; txtFile4C[iC+1,int(numJ[0,1])]=Z[0,1];
				if numJ[0,2]>=numJ[0,1]:
					numJ[0,2]=numJ[0,2]+1
				if numJ[0,3]>=numJ[0,1]:
					numJ[0,3]=numJ[0,3]+1
			
			if addPointZc == 1:
				txtFile4B[iC,int(numJ[0,2])+1:-2]=txtFile4B[iC,int(numJ[0,2]):-3]; txtFile4B[iC+1,int(numJ[0,2])+1:-2]=txtFile4B[iC+1,int(numJ[0,2]):-3];
				txtFile4C[iC,int(numJ[0,2])+1:-2]=txtFile4C[iC,int(numJ[0,2]):-3]; txtFile4C[iC+1,int(numJ[0,2])+1:-2]=txtFile4C[iC+1,int(numJ[0,2]):-3];
				txtFile4B[iC,int(numJ[0,2])]=Zc[0,0]; txtFile4B[iC+1,int(numJ[0,2])]=Zc[0,1]; txtFile4C[iC,int(numJ[0,2])]=Z[0,2]; txtFile4C[iC+1,int(numJ[0,2])]=Z[0,2];
				if numJ[0,3]>=numJ[0,2]:
					numJ[0,3]=numJ[0,3]+1

			if addPointZd == 1:
				txtFile4B[iC,int(numJ[0,3])+1:-1]=txtFile4B[iC,int(numJ[0,3]):-2]; txtFile4B[iC+1,int(numJ[0,3])+1:-1]=txtFile4B[iC+1,int(numJ[0,3]):-2];
				txtFile4C[iC,int(numJ[0,3])+1:-1]=txtFile4C[iC,int(numJ[0,3]):-2]; txtFile4C[iC+1,int(numJ[0,3])+1:-1]=txtFile4C[iC+1,int(numJ[0,3]):-2];
				txtFile4B[iC,int(numJ[0,3])]=Zd[0,0]; txtFile4B[iC+1,int(numJ[0,3])]=Zd[0,1]; txtFile4C[iC,int(numJ[0,3])]=Z[0,3]; txtFile4C[iC+1,int(numJ[0,3])]=Z[0,3];
		

	for i9 in range(0, numMaxImage, 1):
		numR1=0
		for i10 in range(0, row4, 1):
			for j10 in range(0, col4-1, 1):
				if txtFile4C[i10,j10] == i9+1:
					numR1=numR1+1
					txtFile4R[0,i9]=numR1

	txtFile4B1 = np.hstack([txtFile4B,np.zeros(shape=(row4,1))])
	row4A1, col4A1 = txtFile4B1.shape
	for i11 in range(0, row4A1, 1):
		pos2=pos3
		for j11 in range(0, col4A1, 1):
			if txtFile4B1[i11,j11]==0 and pos2==pos3:
				txtFile4E[i11,0:j11]=i11+1
				pos3=pos2+1

	txtFile4D = np.zeros(shape=(int(numMaxImage*2),int(max(max(txtFile4R)))))

	row4D, col4D = txtFile4D.shape
	txtFile4F = np.zeros(shape=(row4D,col4D))
	for i12 in range(0, row4, 2):
		for j12 in range(0, col4, 1):
			if txtFile4C[i12,j12] != 0:

				for j12b in range(0, col4D, 1):
					if pos==0 and txtFile4D[int((txtFile4C[i12,j12]*2)-2),j12b]==0:
						pos=j12b

				txtFile4D[int((txtFile4C[i12,j12]*2)-2),pos]=txtFile4B[i12,j12];
				txtFile4D[int((txtFile4C[i12,j12]*2)-1),pos]=txtFile4B[i12+1,j12];
				txtFile4F[int((txtFile4C[i12,j12]*2)-2),pos]=txtFile4E[i12,j12];
				txtFile4F[int((txtFile4C[i12,j12]*2)-1),pos]=txtFile4E[i12+1,j12];
				pos=0;
	row4D, col4D = txtFile4D.shape
	for i12c in range(0, row4D, 1):
		for j12c in range(0, col4D-1, 1):
			txtFile4D[i12c,j12c]=txtFile4D[i12c,j12c+1]
			txtFile4F[i12c,j12c]=txtFile4F[i12c,j12c+1]
	
	row4F, col4F = txtFile4F.shape
	for i13 in range(0, row4F, 1):
		valuePol=txtFile4F[i13,0]
		for j13 in range(0, col4F, 1):
			if txtFile4F[i13,j13] != 0 and txtFile4F[i13,j13] != valuePol:
				valuePol = txtFile4F[i13,j13]
				row4F, col4F = txtFile4F.shape
				row4D, col4D = txtFile4D.shape
				txtFile4F = np.hstack([txtFile4F,np.zeros(shape=(row4F,1))])
				txtFile4D = np.hstack([txtFile4D,np.zeros(shape=(row4D,1))])
				txtFile4F[i13,j13+1:-1] = txtFile4F[i13,j13:-2]
				txtFile4D[i13,j13+1:-1] = txtFile4D[i13,j13:-2]
				if np.remainder(i13,2)==0:
					txtFile4F[i13,j13]=66666
					txtFile4D[i13,j13]=66666
				else:
					txtFile4F[i13,j13]=88888
					txtFile4D[i13,j13]=88888

	row4F, col4F = txtFile4F.shape
	for i14 in range(0, row4F, 1):
		count2=0
		for j14 in range(0, col4F, 1):
			if txtFile4F[i14,j14] == 0 and count2 == 0:
				txtFile4F[i14,j14]=66666
				txtFile4D[i14,j14]=66666
				count2=1

	row4D, col4D = txtFile4D.shape
	for j15 in range(0, col4D, 1):
		if np.mean(txtFile4D[:,j15]) == 0 and zeroPos == 0:
			zeroPos=j15
	txtFile4D = txtFile4D[:,0:zeroPos];
	zeroPos=0

	txtFile4D1 = np.zeros(shape=(row4D,col4D))
	txtFile4D1 = txtFile4D
	row4D, col4D = txtFile4D.shape
	for i16 in range(0, row4D, 2):
		pos4=0; inc=0; posInf=0; posIni=0;
		for j16 in range(0, col4D, 1):
			if txtFile4D[i16,j16] == 66666 and j16 != 0:
				pos5=j16-1
				posIni=j16+1+inc;
				posInf=j16+(pos5-pos4)+1+inc;
				for i16b in range(posIni, posInf+2, 1):
					row4D1, col4D1 = txtFile4D1.shape
					txtFile4D1 = np.hstack([txtFile4D1,np.zeros(shape=(row4D1,1))])
				txtFile4D1[i16,posInf+2:posInf+col4D-pos5] = txtFile4D[i16,pos5+2:col4D]
				txtFile4D1[i16,posIni:posInf+1] = txtFile4D[i16+1,pos4:pos5+1]
				txtFile4D1[i16,posInf+1] = 77777
				pos4=j16+1
				inc=inc+posInf-posIni+2
	
	row4D1, col4D1 = txtFile4D1.shape
	txtFile4D1 = np.hstack([txtFile4D1,np.zeros(shape=(row4D1,1))]) # For one-object images
	row4D1, col4D1 = txtFile4D1.shape
	for j17 in range(0, col4D1, 1):
		if np.mean(txtFile4D1[:,j17]) == 0 and zeroPos == 0:
			zeroPos=j17
	txtFile4D1 = txtFile4D1[:,0:zeroPos];
	zeroPos=0
	
	row4D, col4D = txtFile4D.shape
	for i18 in range(1, int((row4D/2)+1), 1):
		txtFile4D1 = np.delete(txtFile4D1, i18, 0)
	
	row4D1, col4D1 = txtFile4D1.shape
	for i19 in range(0, row4D1, 1):
		count3=0
		for j19 in range(0, col4D1, 1):
			if txtFile4D1[i19,j19] == 0 and count3 == 0 and j19 != 1:
				if j19 != col4D1 and txtFile4D1[i19,j19+1] == 0:
					txtFile4D1[i19,j19-1] = 99999
					count3=1
				if j19 == col4D1:
					txtFile4D1[i19,j19-1] = 99999
					count3=1
			if txtFile4D1[i19,j19] == 77777 and count3 == 0 and j19 == col4D1-1:
				txtFile4D1[i19,j19] = 99999
				count3=1

	row4D, col4D = txtFile4D.shape
	txtFile4D1 = txtFile4D1[0:int(row4D/2),:]
	row4D1, col4D1 = txtFile4D1.shape
	txtFile4D2 = np.hstack([55555*np.ones(shape=(row4D1,1)),txtFile4D1])

	row4D2, col4D2 = txtFile4D2.shape
	for i20 in range(0, row4D2, 1):
		for j20 in range(0, col4D2-4, 1):
			if txtFile4D2[i20,j20] == 55555 and txtFile4D2[i20,j20+4] == 77777:
				txtFile4D2[i20,j20+1:-4]=txtFile4D2[i20,j20+5:]
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;
			if txtFile4D2[i20,j20] == 77777 and txtFile4D2[i20,j20+4] == 77777:
				txtFile4D2[i20,j20+1:-4]=txtFile4D2[i20,j20+5:]
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;
			if txtFile4D2[i20,j20] == 77777 and txtFile4D2[i20,j20+4] == 99999:
				txtFile4D2[i20,j20+1:-4]=txtFile4D2[i20,j20+5:]
				txtFile4D2[i20,j20]=99999
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;
			if txtFile4D2[i20,j20] == 55555 and txtFile4D2[i20,j20+4] == 99999:
				txtFile4D2[i20,j20+1]=66666;txtFile4D2[i20,j20+2]=99999;txtFile4D2[i20,j20+3]=0;txtFile4D2[i20,j20+4]=0;
	row4D2, col4D2 = txtFile4D2.shape
	for i20 in range(0, row4D2, 1):
		for j20 in range(0, col4D2-6, 1):		
			if txtFile4D2[i20,j20] == 55555 and txtFile4D2[i20,j20+6] == 77777:
				txtFile4D2[i20,j20+1:-6]=txtFile4D2[i20,j20+7:]
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;txtFile4D2[i20,-5]=0;txtFile4D2[i20,-6]=0;
			if txtFile4D2[i20,j20] == 77777 and txtFile4D2[i20,j20+6] == 77777:
				txtFile4D2[i20,j20+1:-6]=txtFile4D2[i20,j20+7:]
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;txtFile4D2[i20,-5]=0;txtFile4D2[i20,-6]=0;
			if txtFile4D2[i20,j20] == 77777 and txtFile4D2[i20,j20+6] == 99999:
				txtFile4D2[i20,j20+1:-6]=txtFile4D2[i20,j20+7:]
				txtFile4D2[i20,j20]=99999
				txtFile4D2[i20,-1]=0;txtFile4D2[i20,-2]=0;txtFile4D2[i20,-3]=0;txtFile4D2[i20,-4]=0;txtFile4D2[i20,-5]=0;txtFile4D2[i20,-6]=0;

	np.savetxt("5_Split/%s_divided.txt" %imName, txtFile4D2, fmt='%d', delimiter=',')
	print("%s_divided.txt created" %imName)


