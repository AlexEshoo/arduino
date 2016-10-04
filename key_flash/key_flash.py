import serial
import time
import msvcrt

arduino = serial.Serial('COM3' , 115200, timeout=.1)
time.sleep(1)
flag = False

def sendColor(R,G,B):
	l = [R,G,B]
	for c in l:
		if c > 127 or c < 0:
			return None
			print "Invalid Color, Message Not Sent!"
	msg = ""
	msg += str(R).zfill(3)
	msg += str(G).zfill(3)
	msg += str(B).zfill(3)
	msg += "?"
	
	arduino.write(msg)

while True:
	while msvcrt.kbhit():
		x = msvcrt.getch()
		sendColor(0,0,127)
		#arduino.write("000000127?")
		flag = True
		data = arduino.readline()

		if data:
			print data
	
	if flag: 
		arduino.write("000000000?") #Write no light if there is no key press
		flag = False
	time.sleep(0.01)
	
