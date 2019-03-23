import numpy as np

with open("coordinates_brainsight.txt","r") as fi:
                        for ln in fi:
                                                if ln.startswith("LPA\tSession"):
                                                                        LPA = ln[14:-1]
                                                                        print(type(LPA))
                                                                        LPA=LPA.split('\t')
                                                                        LPA_bs = [float(i) for i in LPA]
                                                if ln.startswith("RPA\tSession"):
                                                                        RPA = ln[14:-1]
                                                                        RPA=RPA.split('\t')
                                                                        RPA_bs = [float(i) for i in RPA]
                                                if ln.startswith("Nasion\tSession"):
                                                                        Nasion = ln[17:-1]
                                                                        Nasion=Nasion.split('\t')
                                                                        Nasion_bs = [float(i) for i in Nasion]

print(LPA_bs)
print(RPA_bs)
print(Nasion_bs)

with open("coordinates_native.txt","r") as fi:
                        for ln in fi:
                                                if ln.startswith("LPA\tSession"):
                                                                        LPA = ln[14:-1]
                                                                        LPA=LPA.split('\t')
                                                                        LPA_native = [float(i) for i in LPA]
                                                if ln.startswith("RPA\tSession"):
                                                                        RPA = ln[14:-1]
                                                                        RPA=RPA.split('\t')
                                                                        RPA_native = [float(i) for i in RPA]
                                                if ln.startswith("Nasion\tSession"):
                                                                        Nasion = ln[17:-1]
                                                                        Nasion=Nasion.split('\t')
                                                                        Nasion_native = [float(i) for i in Nasion]

print(LPA_native)
print(RPA_native)
print(Nasion_native)

#from matlab (will see this later)
#R = np.array([   [-0.9996,0.0000,-0.0266],[0.0053,-0.9802,-0.1980],[-0.0260,-0.1981,0.9798]])
#T = np.array(  [122.6837,140.5232,-29.3043])

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

R = np.array([R1,R2,R3]) # rotation matrix
T = np.array(Translation) # extra translation

print(type(LPA_bs))
print(np.dot(R,LPA_bs)+T) # convert LPA into native space and display
print(np.dot(R,RPA_bs)+T) # convert RPA into native space and display
print(np.dot(R,Nasion_bs)+T) # convert Nasion into native space and display
