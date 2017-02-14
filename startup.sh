#!/bin/bash

ssh pi@raspberrypinode2 'python /home/pi/sensor_node/grab_serial_sensor_data.py' & python /home/pi/sensor_node/detect_event.py



