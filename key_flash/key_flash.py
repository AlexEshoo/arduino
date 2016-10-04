import serial
import time
from pyhooked import Hook, KeyboardEvent

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
	
def handle_events(args):
	if isinstance(args, KeyboardEvent):
		if args.event_type == 'key down':
			sendColor(0,0,127)
		else:
			sendColor(0,0,0)
			time.sleep(0.01)

hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook()  # hook into the events, and listen to the presses