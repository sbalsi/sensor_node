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
windsensor_data = open("windsensor_data.txt","a+")

#Serial connection to arduino
arduino = serial.Serial("/dev/ttyACM0")
arduino.baudrate=57600

print("Start data gathering")

while True:
	try:

	    #Clear buffer
	    tmp_volts_buffer = []
	    tmp_celsius_buffer = []
	    rv_volts_buffer = []
 	    zeroWind_volts_buffer = []
 	    windSpeed_MPH_buffer = []
	    data_buffer_count = 0
	    print("######################################################")	
	    while (data_buffer_count <2):
		
		data = arduino.readline()
            	data_set = data.split(',')

            	tmp_volts = data_set[0]
            	tmp_celsius = data_set[1]
            	rv_volts = data_set[2]
            	zeroWind_volts = data_set[3]
            	windSpeed_MPH = data_set[4]

		tmp_volts_buffer.append(tmp_volts)
		print(str(tmp_volts)+"-->"+tmp_volts_buffer[data_buffer_count] +" added to tmp_volts_buffer. data_buffer_count= "+str(data_buffer_count))
		tmp_celsius_buffer.append(tmp_celsius)
		rv_volts_buffer.append(rv_volts)
		zeroWind_volts_buffer.append(zeroWind_volts)
		windSpeed_MPH_buffer.append(windSpeed_MPH)		
		
		data_buffer_count = data_buffer_count +1

	    print("After while test")
	    print(str(tmp_volts_buffer[0]))
	    print(str(tmp_volts_buffer[1]))
	    
		
	    print("Data smoothing with data_corr: "+str(data_corr)+" and tmp_volts_buffer: "+tmp_volts_buffer[0]+" "+tmp_volts_buffer[1]+" -->"+ str(data_smoothing(tmp_volts_buffer, data_corr)))	

	    temp_tmp_volts_buffer = tmp_volts_buffer		
	    if data_smoothing(temp_tmp_volts_buffer, data_corr) == 1:
		print("Abweichung OK")
		print("tmp_volts_buffer at index 0 "+str(tmp_volts_buffer[0]))
		print("tmp_volts_buffer at index 1 "+str(tmp_volts_buffer[1]))
	   
#	    if(abs(100/data_buffer[0]*data_buffer[1]-100)<=data_corr):
		 		
	    print("######################################################")	


	    human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	    #Buffer data remove data errors
		
#	    windsensor_data.write(human_time+" ")
#	    windsensor_data.write(data);

	except IOError:
	    print("Error")

arduino.close() 
windsensor_data.close()

	

