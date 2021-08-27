import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import math
import os
import pandas as pd
from tabulate import tabulate
th=int(input())
path="/Users/kshitijsaluja/Desktop/video forgery/frame_measure"
no_of_forgery=[]
video_name=[]
for file in os.listdir(path):
	print(file)
	cap = cv2.VideoCapture(os.path.join(path,file))
	ret, frame1 = cap.read()
	prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame1)
	hsv[...,1] = 255
	frame_no=[]
	op_flow_per_frame=[]
	m=1
	f=1
	b=1
	a=frame1.size
	s=np.arange(a)
	while(1):
		s=0
		ret, frame2 = cap.read()
		if ret==True:
			next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
			flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
			
			frame_no.append(m)
			m=m+1
			mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
			#hsv[...,0] = ang*180/np.pi/2
			#hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
			#bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
			op_flow_1D=np.resize(mag,(1,a))
			#cv2.imshow('frame2',frame2)
			#cv2.waitKey(70)
			for i in op_flow_1D[0]:
				s=s+i
			op_flow_per_frame.append(s)
			prvs = next
			b=b+1
		else:
			break
	vrt_factor=[]
	vrt_factor_round_2=[]
	j=1
	awq=[]
	vrt_factor.append(1)
	for i in range(1,(m)):
		awq.append(i)
	#print(awq)
	for o in (range(m-3)):
		c=(2*op_flow_per_frame[j])/(op_flow_per_frame[(j-1)]+op_flow_per_frame[(j+1)])
		vrt_factor.append(c)
		j=j+1
	vrt_factor.append(1)
	for i in vrt_factor:
		i=round(i,2)
		#print(i)
		vrt_factor_round_2.append(i)
	sum=np.sum(vrt_factor_round_2)
	mean=(sum*1.0)/(b)
	#print(b)

	mean=round(mean,3)
	#print(mean)
	y=0
	poi=[]
	#print(k)
	for i in vrt_factor_round_2:
		y=y+((i-mean)*(i-mean))
	st=(y*1.0)/(b)
	st=round(st,3)
	#print(st)
	fg=math.sqrt(2*(22/7)*st)
	#for i in nbv:
	#	lt=math.exp(-((i-mean)*(i-mean))/(2*st))
	#	print(lt)
	#	pro=(lt*1.0)/(fg)
	#	poi.append((pro))
	anamoly_score=[]
	st=math.sqrt(st)
	for i in vrt_factor_round_2:
		kj=abs((i-mean))
		df=(kj*1.0)/st
		anamoly_score.append(df)
	#print(plk)
	#print(k)
	bv=0
	for i in range(len(anamoly_score)):
		if(anamoly_score[i]>th):
			bv=bv+1
	no_of_forgery.append(bv)
	
			
		
	#plt.title('Video forgery')
	#plt.xlabel('')
	#plt.ylabel('variation factor')
	#plt.plot(awq,k)
	#plt.show()
	
	video_name.append(file)
	print("next")
data=[]
for i in range(len(video_name)):
	data.append([video_name[i],no_of_forgery[i]])
df = pd.DataFrame(data)
filename="video_forgery"+str(th)+".txt"
plt.title('Video forgery')
plt.xlabel('Frame Number')
plt.ylabel('Anomly Score')
plt.plot(frame_no,anamoly_score)
plt.show()
f=open(filename,"w")
f.write(tabulate(df))
f.close()
print(df)
plt.title('Video forgery')
plt.xlabel('Frame Number')
plt.ylabel('Anomly Score')
plt.plot(frame_no,anamoly_score)
plt.show()
cv2.destroyAllWindows()
cap.release()