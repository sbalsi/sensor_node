import serial
import time

human_time = ""

#Open File
windsensor_data = open("windsensor_data.txt","a+")


arduino = serial.Serial("/dev/ttyACM0")
arduino.baudrate=57600


while True:
	try:
	    data = arduino.readline()
	    human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

	    print(human_time)
	    print(data)

	    windsensor_data.write(human_time+" ")
	    windsensor_data.write(data);

	except IOError:
	    print("Error")

arduino.close() 
windsensor_data.close()
