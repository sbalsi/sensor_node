#!/usr/bin/env python

import time
import grovepi
import math

# to calibrate your sensor, put a glass over it, but the sensor should not be
# touching the desktop surface however.
# adjust the zeroWindAdjustment until your sensor reads about zero with the glass over it.

zeroWindAdjustment_sensor_1 = 0 #2.08 negative numbers yield smaller wind speeds and vice versa
zeroWindAdjustment_sensor_2 = 0
zeroWindAdjustment_sensor_3 = 0

#Windsensor 1
#Tmp Sensor connected to A0 Port, Pin 14
#RV connected to A1 Port, Pin 15 
tmp_sensor_1 = 14	
rv_sensor_1 = 15

#Windsensor 2
#Tmp Sensor connected to A1 Port, Pin 15
#RV connected to A2 Port, Pin 16
tmp_sensor_2 = 15
rv_sensor_2 = 16

#Windsensor 3
#Tmp Sensor connected to A3 Port, Pin 16
#RV connected to A3 Port, Pin 17
tmp_sensor_3 = 16
rv_sensor_3 = 17

	
grovepi.pinMode(tmp_sensor_1,"INPUT")
grovepi.pinMode(rv_sensor_1, "INPUT")
grovepi.pinMode(tmp_sensor_2,"INPUT")
grovepi.pinMode(rv_sensor_2, "INPUT")
grovepi.pinMode(tmp_sensor_3,"INPUT")
grovepi.pinMode(rv_sensor_3, "INPUT")

while True:
    try:
        tmp_therm_adUnits_1 = grovepi.analogRead(tmp_sensor_1)
	tmp_therm_volts_1 = tmp_therm_adUnits_1*0.0048828125
	rv_wind_adUnits_1 = grovepi.analogRead(rv_sensor_1)
	rv_wind_adUnits_3 = grovepi.analogRead(rv_sensor_3)
	rv_wind_volts_1 = rv_wind_adUnits_1 * 0.0048828125
	rv_wind_volts_3 = rv_wind_adUnits_3 * 0.0048828125
	tmp_celsius_1 = (0.005*(tmp_therm_adUnits_1*tmp_therm_adUnits_1)-(16.862*tmp_therm_adUnits_1)+9075.4)/100

		
	#print("rv_wind_volts_1: "+str(rv_wind_volts_1)+"\n")
	print("Pin 14: "+str(grovepi.analogRead(14)))
	print("Pin 15: "+str(grovepi.analogRead(15))+"\n")
	
		


	#csv_file = open("sensor_readings.csv", "a+")
	#csv_file.write(str(tmp)+","+str(rv_sensor_volts_1))
	#csv_file.close()	

        time.sleep(.5)

    except IOError:
        print ("Error")
