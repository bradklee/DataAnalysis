#
#ProcessFitLog.py
#

#SYSTEM CONFIGURATION VARIABLES
OUTBASE="."

PreValDict=list()
PreDevDict=list()

fracExpect={
"VARL":"1/4",
"VARQ":"9/64",
"VARC":"25/256"
}

floatExpect={
"VARL":float(1/4),
"VARQ":float(9/64),
"VARC":float(25/256)
}

EpExpect={
"VAR4":-2,
"VAR6":4,
"VAR8":-8
}

for line in open(OUTBASE+'/Output/fit.log', 'r'):
	if "+/-" in line:
		lineList = list(filter(lambda a: a!='', line.split(" ")))
		PreValDict.append((lineList[0],lineList[2]))
		PreDevDict.append((lineList[0],lineList[4]))

Deviations = dict(PreDevDict)
Values = dict(PreValDict)

e1 = -8*float(Values["VARL"])
e2 = -96*(float(Values["VARQ"])-float(35/768)*(e1**2)) 

cosValues={
"VAR4":e1,
"VAR6":e2,
"VAR8":1
}

cosDeviations={
"VAR4":1,
"VAR6":1,
"VAR8":1
}


print('======================================================================')
print('1. Estimation of EllipticK(m) expansion coefficients.')
print('======================================================================')
print('Expectation		Estimate		Confidence	Error')
print('----------------------------------------------------------------------')

for key in ["VARL","VARQ","VARC"]:
	print('{0} ~ {1}		{2} +/- {3}	{4} sigma	{5}%'
		.format(fracExpect[key], 		
		round(floatExpect[key],4), 
		round(float(Values[key]),4), 
		round(float(Deviations[key]),4),
		round((floatExpect[key]-float(Values[key]))/float(Deviations[key]),2),
		round(100*(floatExpect[key]-float(Values[key]))/floatExpect[key],1) ))

print('======================================================================')
#print('2. Estimation of cos(x) expansion coefficients.')
#print('======================================================================')
#print('Expectation		Estimate		Confidence	Error')
#print('----------------------------------------------------------------------')

#for key in ["VAR4","VAR6","VAR8"]:
#	print('{0}			{1} +/- {2}		{3} sigma	{4}%'
#		.format(EpExpect[key], 		
#		round(float(cosValues[key]),4), 
#		round(float(cosDeviations[key]),4),
#		round((EpExpect[key]-float(cosValues[key]))/float(cosDeviations[key]),2),
#		round(100*(EpExpect[key]-float(cosValues[key]))/EpExpect[key],1) ))

#print('======================================================================')
