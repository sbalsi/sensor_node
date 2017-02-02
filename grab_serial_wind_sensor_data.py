import serial
import time

arduino = serial.Serial("/dev/ttyACM0")
arduino.baudrate=57600


while True:
	try:
	    data = arduino.readline()
	    print(data)

	except IOError:
	    print("Error") 
