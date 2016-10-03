import serial
import time
import msvcrt

arduino = serial.Serial('COM3' , 115200, timeout=.1)
time.sleep(1)

while True:
	while msvcrt.kbhit():
		x = msvcrt.getch()
		arduino.write("!000000127?")
		data = arduino.readline()

		if data:
			print data
	
	arduino.write("!000000000?") #Write no light if there is no key press
	time.sleep(0.01)