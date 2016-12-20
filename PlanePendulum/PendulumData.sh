#!/bin/bash

#PROMPTS HERE

while [[ ! ${EXAMPLE} =~ ^([1-9]|[1-9][0-9]|100)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 1 -p "	Index for example time series plot (integer [1,100]):  " EXAMPLE
done

while [[ ! ${OFFSET} =~ ^(0\.[0-9]+|\.[0-9]+)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 0.005 -p "	Minimum Energy (float [0.0,0.01]):  " OFFSET
done

while [[ ! ${BINWIDTH} =~ ^(0\.[0-9]+|\.[0-9]+)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 0.0085 -p "	Bin Energy Width (float [0.0,0.05]):  " BINWIDTH
done

while [[ ! ${LINEAR} =~ ^(0\.[0-9]+|\.[0-9]+)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 0.084 -p "	Max Energy for Linear Data (float [0.0,1.0]):  " LINEAR
done

while [[ ! ${QUADRATIC} =~ ^(0\.[0-9]+|\.[0-9]+)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 0.217 -p "	Max Energy for Quadratic Data (float [$LINEAR,1.0]):  " QUADRATIC
done

while [[ ! ${CUBIC} =~ ^(0\.[0-9]+|\.[0-9]+)$ ]]; do
        clear
	cat ./Style/FRAME2.ASC	
	read -e -i 0.9 -p "	Max Energy for Cubic Data (float [$QUADRATIC,1.0]):  " CUBIC
done


# Clear and regenerate processed data slices
rm ./Data/*Data.csv
(python ProcessData.py $OFFSET $BINWIDTH $LINEAR $QUADRATIC $CUBIC $EXAMPLE > /dev/null) & pid=$!


# Waiting Animation 
while kill -0 $pid 2> /dev/null;
do 
  for i in {0..3}
  do
	clear
        if [ $(( $i % 4)) -eq 0 ]; then
		cat ./Style/FRAME2.ASC
        fi
        if [ $(( $i % 4)) -eq 1 ]; then
		cat ./Style/FRAME1.ASC
        fi
        if [ $(( $i % 4)) -eq 2 ]; then
		cat ./Style/FRAME2.ASC
        fi
        if [ $(( $i % 4)) -eq 3 ]; then
		cat ./Style/FRAME3.ASC
        fi
	echo "			Processing the data..."
        sleep .1
  done
done

# Clear fit log, regenerate fit
rm ./fit.log
rm ./Output/EditedFit.log
rm ./Output/Tm.png
./GeneratePlots.sh 

# Redact fit log
python ./ProcessFitLog.py > ./Output/EditedFit.log
clear
cat ./Style/FRAME2.ASC
cat ./Output/EditedFit.log
echo "**** Files in './Output' updated."
