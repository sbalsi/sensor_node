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
def data_smoothing(buffer_values, data_corr):
        if abs(100/float(buffer_values[0])*float(buffer_values[1])-100) <= data_corr:
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

data_corr = 10 #Data Correction Parameter in Percentage. 10% means that a data set n which differs more than 10% from a dataset n-1 will be sorted out.

#Data output
sensor_node_data = open("/home/pi/sensor_node/output/sensor_node_data.txt","a+")
sensor_node_log = open("/home/pi/sensor_node/output/sensor_node.log", "a+")
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

	    #Data output
	    sensor_node_data = open("/home/pi/sensor_node/output/sensor_node_data.txt","a+")
            sensor_node_log = open("/home/pi/sensor_node/output/sensor_node.log", "a+")

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
	    sensor_node_log.write("######################################################\n")	
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
	    if data_smoothing(temp_windSpeed_MPH_buffer, data_corr) == 1:
		print("Fluctuation of windsensor OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%")
                print("Windspeed in mph, measurement n "+str(time_buffer[0])+" "+str(temp_windSpeed_MPH_buffer[0]))
                print("Windspeed in mph, measurement n+1 "+str(time_buffer[1])+" "+str(temp_windSpeed_MPH_buffer[1]))

		print("Temperature in celsius, measurement n: "+str(time_buffer[0])+" "+str(tmp_celsius_buffer[0]))
		print("Temperature in celsius, measurement n+1: "+str(time_buffer[1])+" "+str(tmp_celsius_buffer[1]))

		#Write data
                sensor_node_data.write(str(time_buffer[0])+", "+str(temp_windSpeed_MPH_buffer[0])+", "+str(tmp_celsius_buffer[0])+"\n")
                sensor_node_data.write(str(time_buffer[1])+", "+str(temp_windSpeed_MPH_buffer[1])+", "+str(tmp_celsius_buffer[1])+"\n")
		
		#Write log
                sensor_node_log.write("Fluctuation of windsensor OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%\n")
                sensor_node_log.write("Windspeed in mph, measurement n "+str(time_buffer[0])+" "+str(temp_windSpeed_MPH_buffer[0])+"\n")
                sensor_node_log.write("Windspeed in mph, measurement n+1 "+str(time_buffer[1])+" "+str(temp_windSpeed_MPH_buffer[1])+"\n")	
 
	    else:
		 print("Fluctuation of windsensor NOT OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%")	 		


	    human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())



	    sensor_node_data.close()
	    sensor_node_log.close()
	except IOError:
	    print("Error")

arduino.close() 

	

