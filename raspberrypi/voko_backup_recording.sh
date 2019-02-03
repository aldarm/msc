#!/bin/bash
cp /home/pi/Videos/*.mp4 /media/pi/Maxtor/pi1pi2pi3pi4/Videos/pi0/
if [ $? -eq 0 ]; then
	rm /home/pi/Videos/*.mp4
else
    	echo FAIL
fi


