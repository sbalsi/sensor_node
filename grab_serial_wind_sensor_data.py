import serial
import time


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
sensor_node_data = open("sensor_node_data.txt","a+")
sensor_node_log = open("sensor_node.log", "a+")
#Serial connection to arduino
arduino = serial.Serial("/dev/ttyACM0")
arduino.baudrate=57600

#Preheat sensor
print("Preheat Sensor")
i = 10
while (i >0):
	print(i)
	arduino.readline()
	time.sleep(1)
	i = i-1

		
print("Start data gathering")
while True:
	try:

	    #Data output
	    sensor_node_data = open("sensor_node_data.txt","a+")
            sensor_node_log = open("sensor_node.log", "a+")

	    #Clear buffer
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

            	data_set = data.split(',')

            	tmp_volts = data_set[0]
            	tmp_celsius = data_set[1]
            	rv_volts = data_set[2]
            	zeroWind_volts = data_set[3]
            	windSpeed_MPH = data_set[4]

		tmp_volts_buffer.append(tmp_volts)
		tmp_celsius_buffer.append(tmp_celsius)
		rv_volts_buffer.append(rv_volts)
		zeroWind_volts_buffer.append(zeroWind_volts)
		windSpeed_MPH_buffer.append(windSpeed_MPH)		
		
		data_buffer_count = data_buffer_count +1

		
#	    print("Data smoothing with data_corr: "+str(data_corr)+" and tmp_volts_buffer: "+tmp_volts_buffer[0]+" "+tmp_volts_buffer[1]+" -->"+ str(data_smoothing(tmp_volts_buffer, data_corr)))	

#	    temp_tmp_volts_buffer = tmp_volts_buffer		
#	    temp_rv_volts_buffer = rv_volts_buffer

#	    if data_smoothing(temp_tmp_volts_buffer, data_corr) == 1 and data_smoothing(temp_rv_volts_buffer, data_corr) == 1:
#		print("Fluctuation of tmp thermistor OK: "+ str(abs(100/float(temp_tmp_volts_buffer[0])*float(temp_tmp_volts_buffer[1])-100))+"%")
#		print("tmp thermistor value in volts of measurement n "+str(time_buffer[0])+" "+str(temp_tmp_volts_buffer[0]))
#		print("tmp thermistor value in volts of measurement n+1 "+str(time_buffer[1])+" "+str(temp_tmp_volts_buffer[1]))
#	 
#		sensor_node_data.write(str(time_buffer[0])+", "+str(temp_tmp_volts_buffer[0])+", "+str(temp_rv_volts_buffer[0])+"\n")
#		sensor_node_data.write(str(time_buffer[1])+", "+str(temp_tmp_volts_buffer[1])+", "+str(temp_rv_volts_buffer[1])+"\n")
	
#		sensor_node_log.write("Fluctuation of tmp thermistor OK: "+ str(abs(100/float(temp_tmp_volts_buffer[0])*float(temp_tmp_volts_buffer[1])-100))+"%\n") 
#		sensor_node_log.write("tmp thermistor value in volts of measurement n "+str(time_buffer[0])+" "+str(temp_tmp_volts_buffer[0])+"\n") 
#		sensor_node_log.write("tmp thermistor value in volts of measurement n+1 "+str(time_buffer[1])+" "+str(temp_tmp_volts_buffer[1])+"\n")


#		print("Fluctuation of rv sensor in volts OK: "+ str(abs(100/float(temp_rv_volts_buffer[0])*float(temp_rv_volts_buffer[1])-100))+"%")
#               print("measurement n of rv sensor in volts "+str(time_buffer[0])+" "+str(temp_rv_volts_buffer[0]))
#               print("measurement n+1 of rv sensor in volts "+str(time_buffer[1])+" "+str(temp_rv_volts_buffer[1]))


#               sensor_node_log.write("Fluctuation of rv sensor in volts OK: "+ str(abs(100/float(temp_rv_volts_buffer[0])*float(temp_rv_volts_buffer[1])-100))+"%\n")
#               sensor_node_log.write("measurement n of rv sensor in volts "+str(time_buffer[0])+" "+str(temp_rv_volts_buffer[0])+"\n")
#               sensor_node_log.write("measurement n+1 of rv sensor in volts "+str(time_buffer[1])+" "+str(temp_rv_volts_buffer[1])+"\n")

	    temp_windSpeed_MPH_buffer = windSpeed_MPH_buffer
	    if data_smoothing(temp_windSpeed_MPH_buffer, data_corr) == 1:
		print("Fluctuation of windsensor OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%")
                print("Windspeed in mph, measurement n "+str(time_buffer[0])+" "+str(temp_windSpeed_MPH_buffer[0]))
                print("Windspeed in mph, measurement n+1 "+str(time_buffer[1])+" "+str(temp_windSpeed_MPH_buffer[1]))

                sensor_node_data.write(str(time_buffer[0])+", "+str(temp_windSpeed_MPH_buffer[0]))
                sensor_node_data.write(str(time_buffer[1])+", "+str(temp_windSpeed_MPH_buffer[1]))

                sensor_node_log.write("Fluctuation of windsensor OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%\n")
                sensor_node_log.write("Windspeed in mph, measurement n "+str(time_buffer[0])+" "+str(temp_windSpeed_MPH_buffer[0])+"\n")
                sensor_node_log.write("Windspeed in mph, measurement n+1 "+str(time_buffer[1])+" "+str(temp_windSpeed_MPH_buffer[1])+"\n")	
 
	    else:
		 print("Fluctuation of windsensor NOT OK: "+ str(abs(100/float(temp_windSpeed_MPH_buffer[0])*float(temp_windSpeed_MPH_buffer[1])-100))+"%")	 		


	    human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	    #Buffer data remove data errors
		
#	    windsensor_data.write(human_time+" ")
#	    windsensor_data.write(data);

	    sensor_node_data.close()
	    sensor_node_log.close()
	except IOError:
	    print("Error")

arduino.close() 

	

