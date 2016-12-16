#!/usr/bin/gnuplot -persist
set datafile separator ","
set title 'Experimental Determination of EllipticK Anharmonicity Constants'
set key left
set xlabel 'Dimensionless Energy m=k^2'
set ylabel 'Period (seconds)'
linear(x) = a*(1+b*x)
quadratic(x) = linear(x) + a*c*x**2
cubic(x) = quadratic(x) + a*d*x**3
ellk(x) = e*(2/pi)*EllipticK(sqrt(x))
fit ellk(x) './Data/MeanTmData.csv' using 1:2:3:4  xyerrors via e
fit linear(x) './Data/LinearData.csv' using 1:2:3:4  xyerrors via a, b
fit quadratic(x) './Data/QuadraticData.csv' using 1:2:3:4  xyerrors via a, c
fit cubic(x) './Data/CubicData.csv' using 1:2:3:4  xyerrors via a, d
plot [0.00:.4][.58:.66] ellk(x), linear(x),quadratic(x),cubic(x), './Data/CubicData.csv' using 1:2:3:4 with xyerrorbars , './Data/QuadraticData.csv' using 1:2:3:4 with xyerrorbars,  './Data/LinearData.csv' using 1:2:3:4 with xyerrorbars 


