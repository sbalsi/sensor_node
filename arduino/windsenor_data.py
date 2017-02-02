import serial
import time

#TODO Anpassen
arduino = serial.Serial("/dev/ttyACMO")
arduino.baudrate=9600

while True:
   try:
	data = arduino.readline()
	pieces = data.split("\t")

	tmp_therm_volts = pieces[0]
	tmp_celsius = pieces[1]
	rv_wind_volts = pieces[2]
	zeroWind_volts = pieces[3]
	windSpeed_MPH = pieces[4]

	print("Temperatur Sensor Volt: "+ str(tmp_therm_volts))
	print("Temperatur Sensor Celsius: "+ str(tmp_celsius))
	print("Wind Sensor Volt: "+str(rv_wind_volts))
	print("ZeroWind Volt: "+str(zeroWind_volts))
	print("WindSpeed MPH: "+str(windSpeed_MPH))

	time.sleep(.5)

   except IOError:
	print("Error")

