
import os
import sys
import numpy as np
import pandas as pd



#os.chdir('/home/brainhacker/tms-tracto/tms-tracto/')
os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.1.3,share=brainhack/shared/Gabriel_brain')

while (1==1):

	a=pd.read_csv('Brainhack_stream2.txt',skiprows=5,sep='\t')


	#print(a)


	#stream=open('/run/user/1000/gvfs/smb-share:server=192.168.1.2,share=brainhack/shared/stream_PKbrain.txt')


	a1=a[['x','y','z']]

	#print(a1)

	#type(a1)

	a2=a1.as_matrix()

	#Import the Rotation matrix and the translation vecctor
	infile = open("ROTMAT.txt", "r")
	aline = str(infile.readline())
	aline2=aline[:-1]
	R1 = [float(i) for i in aline2.split('\t')]
	aline = str(infile.readline())
	aline2=aline[:-1]
	R2 = [float(i) for i in aline2.split('\t')]
	aline = str(infile.readline())
	aline2=aline[:-1]
	R3 = [float(i) for i in aline2.split('\t')]
	aline = str(infile.readline())
	aline2=aline[:-1]
	Translation = [float(i) for i in aline2.split('\t')]

	#Create a vector with the last value of the file
	q=a2[len(a2)-1: , : ]
	if (q[0,1] == "(null)"):
		print("Umbrella outsite field of view")
	else:
		q=q[0]
		q = [float(i) for i in q]
		print(q)

		'''
		c=pd.read_csv('Brainhack_stream2.txt')
		chead=c.head(10)
		ctail=c.tail(1)
		c = [chead, ctail]
		c = pd.concat(c)
		c.to_csv('Brainhack_stream2.txt', header=None, index=None, sep='	', mode='a')
		'''
		#Convert the coordinates of the dot
		R = np.array([R1,R2,R3]) # rotation matrix
		T = np.array(Translation) # extra translation

		print(np.dot(R,q)+T)
		trans_q=np.dot(R,q)+T



		np.savetxt('/home/brainhacker/tms-tracto/data/update_pts.txt',trans_q)

	#system sleep?
