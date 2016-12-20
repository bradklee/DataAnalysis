#!/bin/bash 
gnuplot <<EOF
set fit quiet
set terminal pngcairo size 800,600
set output './Output/Tm.png'
set datafile separator ","
set title 'Experimental Determination of EllipticK Anharmonicity Constants'
set key left
set xlabel 'Dimensionless Energy m=k^2'
set ylabel 'Period (seconds)'
linear(x) = VART*(1+VARL*x)
quadratic(x) = linear(x) + VART*VARQ*x**2
cubic(x) = quadratic(x) + VART*VARC*x**3
ellk(x) = VART2*(2/pi)*EllipticK(sqrt(x))
fit ellk(x) './Data/MeanTmData.csv' using 1:2:3:4  xyerrors via VART2
fit linear(x) './Data/LinearData.csv' using 1:2:3:4  xyerrors via VART, VARL
fit quadratic(x) './Data/QuadraticData.csv' using 1:2:3:4  xyerrors via VART, VARQ
fit cubic(x) './Data/CubicData.csv' using 1:2:3:4  xyerrors via VART, VARC
plot [0.00:.4][.58:.66]  \
	ellk(x), linear(x),quadratic(x),cubic(x), \
	'./Data/CubicData.csv' using 1:2:3:4 with xyerrorbars , \
	'./Data/QuadraticData.csv' using 1:2:3:4 with xyerrorbars, \
	'./Data/LinearData.csv' using 1:2:3:4 with xyerrorbars 
set output './Output/AllData.png'
set title 'All Period(Energy) Data ( no binning )'
plot [0.00:.4][.58:.66] './Data/CombinedTmData.csv' using 1:2
set title 'Example Time Series Data'
set output './Output/ExampleTimeSeries.png'
set key right
set xlabel 'Time (seconds)'
set ylabel 'Amplitude (radians / 2 pi)'
plot [0.0:20.0][-0.25:0.25] './Data/ExampleTimeSeries.csv' using 1:2
EOF
