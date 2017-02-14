import serial
import time
#import smbus
#import RPi.GPIO as GPIO
#from grove_i2c_barometic_sensor_BMP180 import BMP085

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
#bmp = BMP085(0x77,3)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode

#rev = GPIO.RPI_REVISION
#if rev == 2 or rev == 3:
#    bus = smbus.SMBus(1)
#else:
#    bus = smbus.SMBus(0)


#################################################################
#Functions
#################################################################
def remove_extr_values_tmp(buffer_values, data_corr_tmp):
        if abs(float(buffer_values[0])-float(buffer_values[1])) <= data_corr_tmp:
                return 1
        else:
                return 0

def remove_extr_values_wind(buffer_values, data_corr_wind):
        if abs(float(buffer_values[0])-float(buffer_values[1])) <= data_corr_wind:
                return 1
        else:
                return 0

###############################################################

human_time = ""
tmp_volts_buffer = []
tmp_celsius_buffer = []
rv_volts_buffer = []
zeroWind_volts_buffer = []
windSpeed_MPH_buffer = []

data_corr_tmp = 10 #Data Correction Parameter in Celsius. 5 means that a data set n which differs more than 5 grades celsius from a dataset n-1 will be sorted out.
data_corr_wind = 20 

#Data output
sensor_node_data_file = "/home/pi/sensor_node/output/sensor_node_data.txt"
sensor_node_log_file = "/home/pi/sensor_node/output/sensor_node.log"
sensor_node_data_fh = open(sensor_node_data_file,"a+")
sensor_node_log_fh = open(sensor_node_log_file, "a+")

#Serial connection to arduino
arduino = serial.Serial("/dev/ttyACM0",timeout=3)
arduino.baudrate=57600

#Preheat sensor
print("Preheat Sensor")
i = 10
while (i >0):
	try:
		arduino.readline()
		print(i)
		time.sleep(1)
		i = i-1
	except serial.serialutil.SerialException:
		pass

		
print("Start data gathering")
while True:
	try:


	    #Clear buffer
#	    tmp_celsius_bmp_buffer = []
	    tmp_volts_buffer = []
	    tmp_celsius_buffer = []
	    rv_volts_buffer = []
 	    zeroWind_volts_buffer = []
 	    windSpeed_MPH_buffer = []
	    time_buffer = []
	    data_buffer_count = 0
	    


	    print("######################################################")
	    
	    sensor_node_log_fh = open(sensor_node_log_file, "a+")
            sensor_node_log_fh.write("######################################################\n")
	    sensor_node_log_fh.close()
	
	    while (data_buffer_count <2):
		
		data = arduino.readline()
		human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
		time_buffer.append(human_time)		

		#Temperature sensor groovepi
#		tmp_celsius_bmp = bmp.readTemperature()
		
		#Windsensor
            	data_set = data.split(',')
		#Sort out bad data sets
		if int(len(data_set)) == 5:
            		tmp_volts = data_set[0]
            		tmp_celsius = data_set[1]
            		rv_volts = data_set[2]
            		zeroWind_volts = data_set[3]
            		windSpeed_MPH = data_set[4].rstrip('\n')
		else:
			print("Error reading sensor")
			tmp_volts = 999999999
			tmp_celsius = 999999999
			rv_volts = 999999999
			zeroWind_volts = 999999999
			windSpeed_MPH = 999999999

#		tmp_celsius_bmp_buffer.append(tmp_celsius_bmp)
		tmp_volts_buffer.append(tmp_volts)
		tmp_celsius_buffer.append(tmp_celsius)
		rv_volts_buffer.append(rv_volts)
		zeroWind_volts_buffer.append(zeroWind_volts)
		windSpeed_MPH_buffer.append(windSpeed_MPH)		
		
		data_buffer_count = data_buffer_count +1

		

	    temp_windSpeed_MPH_buffer = windSpeed_MPH_buffer
	    temp_tmp_celsius_buffer =  tmp_celsius_buffer
	    
	    if remove_extr_values_wind(temp_windSpeed_MPH_buffer, data_corr_wind) == 1 and remove_extr_values_tmp(temp_tmp_celsius_buffer, data_corr_tmp) == 1:
		print("Fluctuation of wind sensor OK: "+ str(abs(float(temp_windSpeed_MPH_buffer[0])-float(temp_windSpeed_MPH_buffer[1]))))
		print("Fluctuation of temperature sensor OK: "+ str(abs(float(temp_tmp_celsius_buffer[0])-float(temp_tmp_celsius_buffer[1]))))

		#Write data
		sensor_node_data_fh = open(sensor_node_data_file, "a+")
                sensor_node_data_fh.write(str(time_buffer[0])+", "+str(temp_windSpeed_MPH_buffer[0])+", "+str(tmp_celsius_buffer[0])+"\n")
                sensor_node_data_fh.write(str(time_buffer[1])+", "+str(temp_windSpeed_MPH_buffer[1])+", "+str(tmp_celsius_buffer[1])+"\n")
		sensor_node_data_fh.close()

		#Write log
		sensor_node_log_fh = open(sensor_node_log_file, "a+")
		sensor_node_log_fh.write("Fluctuation of temperature sensor OK: "+ str(abs(float(temp_tmp_celsius_buffer[0])-float(temp_tmp_celsius_buffer[1]))))
		sensor_node_log_fh.write("Temperature in celsius, measurement n: "+str(time_buffer[0])+" "+str(temp_tmp_celsius_buffer[0]))
		sensor_node_log_fh.write("Temperature in celsius, measurement n+1: "+str(time_buffer[1])+" "+str(temp_tmp_celsius_buffer[1]))
				
                sensor_node_log_fh.write("Fluctuation of windsensor OK: "+ str(abs(float(temp_windSpeed_MPH_buffer[0])-float(temp_windSpeed_MPH_buffer[1]))))
                sensor_node_log_fh.write("Windspeed in mph, measurement n "+str(time_buffer[0])+" "+str(temp_windSpeed_MPH_buffer[0])+"\n")
                sensor_node_log_fh.write("Windspeed in mph, measurement n+1 "+str(time_buffer[1])+" "+str(temp_windSpeed_MPH_buffer[1])+"\n")	
		
		sensor_node_log_fh.close()	
 
	    else:
		"Sensor error: fluctuation to high"

#	    human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())



	except IOError:
	    print("Error")

arduino.close() 

	

