#!/bin/bash

# Set environment defaults
OFFSET=0.005
BINWIDTH=0.0085
LINEAR=0.084
QUADRATIC=0.217
CUBIC=0.9

# Clear and regenerate processed data slices
rm ./Data/*Data.csv
python ProcessData.py $OFFSET $BINWIDTH $LINEAR $QUADRATIC $CUBIC

# Clear fit log, regenerate fit
rm ./fit.log
rm ./Tm.png
./EllKDataPlot.sh 

# Redact fit log
