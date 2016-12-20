#
# ProcessData.py
#

#DATA PROCESSING. EXTRACT 100 DATA RUNS. CONSTRUCT AVERAGED T(m) DATA.

import csv
import math
import sys

#META-ANALYSIS DEPENDANT VARIABLES.

OFFSET = float(sys.argv[1])
BINWIDTH = float(sys.argv[2])
LINEAR = float(sys.argv[3])
QUADRATIC = float(sys.argv[4])
CUBIC = float(sys.argv[5])
EXAMPLE = int(sys.argv[6])

#FUNCTION DEFINITIONS. MATHEMATICA TRANSCRIPTIONS.

def transpose(x):
	return list(map(list,zip(*x)))

def mapthread(fun,list1,list2):
	return list(map(lambda x:fun(list1[x],list2[x]),range(0,len(list1),1) ))	

def partition(l,n,m):
	return list(map(lambda x: l[m*x:m*x+n],
		range(0,math.floor((len(l)-(n-m))/m),1 )
		))	
def sign(x): 
	return (x>0)-(x<0)

def dot(x,y):
	return sum(list(mapthread(lambda a,b : a*b,x,y)))

#FUNCTION DEFINITIONS. SPECIAL.

def zeroSwitch(x):
	return {
		# base-10 encode to 'hashable' value
		89:(x[0][0]+x[1][0])/2,
		99:x[1][0],
		100:x[1][0]
		}.get(
			dot(list(map(sign,list(zip(*x))[1])),[100,10,1])
			,0)

def zeroSet(OneTrial):
	return list(filter(
		lambda a: a!=0,
		list(map(
		zeroSwitch, 
		partition(OneTrial,3,1)
		))))

def MaxMinAvg(l):
	return (abs(max(l))+abs(min(l)))/2

def TVSmData(OneTrial,ZSet):
	return list(map(lambda x:
		[math.sin(
			math.pi*MaxMinAvg(
			list(zip(*list(filter(lambda a: a[0] <x[1] and a[0]>x[0],OneTrial))))[1])
			)**2,
		x[1]-x[0]], ZSet))	

def BinData(TmData):
	return  list(filter(lambda x:x!=[],
		list(map(lambda b: 
		filter(lambda c: OFFSET+b*BINWIDTH < c[0] < OFFSET+(b+1)*BINWIDTH, TmData),
		#----VVV---- start @ 1 cuts off some frictional noise  
		range(0,math.ceil(1/BINWIDTH),1) )) ))

def MeanData(TmData):
	return  list(map(lambda DataPart:
		list(map(lambda a: sum(a)/len(a),transpose(DataPart))),
		BinData(TmData)
		))

def StdDevData(means,TmData):
	return  mapthread(lambda DataPart, mean :
			mapthread(lambda row, a0: 
				math.sqrt(sum(list(map(lambda a: (a-a0)**2 , row)))/len(row)),
				transpose(DataPart),mean),
			BinData(TmData),means)

# VALIDATION / EXIT

# MAIN PROGRAM.

#Read File
with open('./Data/100Trials.csv','r') as DataIn:
	reader = csv.reader(DataIn)
	RawData = list(map(lambda a:list(map(float,a)),list(reader)))

#List of (time,amplitude) values per trial, 100 total trials. 
Data = list(map(transpose,list(partition(RawData,2,2))))

#Find One Period Intervals
ZeroSets = list(map(lambda x: partition(zeroSet(x),2,1),Data))

#T(m) data for each of 100 trials
TmData=mapthread(TVSmData,Data,ZeroSets)
CombinedTmData = list(item for sublist in TmData for item in sublist ) 

#Redact
MD = MeanData(CombinedTmData)
SDD = StdDevData(MD,CombinedTmData)
DataOut = list(map(lambda row: list(map(lambda element: round(element,5), row)),
	list(filter(lambda a: a!=[], mapthread(lambda a,b:a+b,MD,SDD))) ))

#Write Example Time Series Data
with open("./Data/ExampleTimeSeries.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(Data[EXAMPLE-1])

#Write Combined Data
with open("./Data/CombinedTmData.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(CombinedTmData)

#Write Averaged Data
with open("./Data/MeanTmData.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(DataOut)

#Write Linear Averaged Data
with open("./Data/LinearData.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(
		list(filter(lambda a: a[0] < LINEAR,DataOut))
		)

#Write Quadratic Averaged Data
with open("./Data/QuadraticData.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(
		list(filter(lambda a: a[0] < QUADRATIC,DataOut))
		)

#Write Cubic Averaged Data
with open("./Data/CubicData.csv","w") as f:
	writer= csv.writer(f)
	writer.writerows(
		list(filter(lambda a: a[0] < CUBIC,DataOut))
		)

