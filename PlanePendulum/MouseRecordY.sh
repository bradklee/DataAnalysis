#!/bin/bash
for i in {0..5000}
do 
date +"%H.%M.%S.%3N"
eval $(xdotool getmouselocation --shell)
echo $Y
done
