import serial
import time
import msvcrt

arduino = serial.Serial('COM3' , 115200, timeout=.1)
time.sleep(1)

while True:
	while msvcrt.kbhit():
		x = msvcrt.getch()
		arduino.write(x)
		data = arduino.readline()
		
		if data:
			print data
	
	arduino.write(0)