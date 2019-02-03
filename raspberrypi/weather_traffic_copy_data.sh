#!/bin/bash
rclone copy /home/pi/traffic_data dropbox:pi/traffic_flow_data
rclone copy /home/pi/weather_data dropbox:pi/weather_data
if [ $? -eq 0 ]; then
    mv /home/pi/traffic_data/*.txt  /media/pi/Maxtor/pi1pi2pi3pi4/data/traffic_flow_data/
    mv /home/pi/weather_data/*.txt  /media/pi/Maxtor/pi1pi2pi3pi4/data/weather_data/
else
    echo FAIL
fi

