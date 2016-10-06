import serial
import time
from pyhooked import Hook, KeyboardEvent

arduino = serial.Serial('COM3' , 115200, timeout=.1)
time.sleep(1)
flag = False

def sendColor(R,G,B, led_ids = None):
	l = [R,G,B]
	for c in l:
		if c > 127 or c < 0:
			return None
			print "Invalid Color, Message Not Sent!"
	msg = ""
	msg += str(R).zfill(3)
	msg += str(G).zfill(3)
	msg += str(B).zfill(3)
	if led_ids:
		addrs = [0]*32
		for id in led_ids:
			if id not in range(0,32):
				addrs = "" # Act as if nothing was addressed.
				print "Address out of bounds!"
				break
			else:
				addrs[id] = 1
		msg += ''.join(str(e) for e in addrs)
	
	msg += "?"
	arduino.write(msg)
	
def numberPress(num):
	if num in range(0,10):
		sendColor(127,127,127,led_ids = [num])
	else:
		return

def handle_events(args):
	if isinstance(args, KeyboardEvent):
		if args.event_type == 'key down':
			if args.key_code in range(65,91):
				sendColor(0,127,127)
			elif args.current_key in [str(s)for s in range(0,10)] or args.current_key in ['Numpad{}'.format(s) for s in range(0,10)]:
				numberPress(int(args.current_key[-1]))
			elif args.current_key == 'Escape':
				sendColor(127,0,0)
			else:
				sendColor(0,0,127)
		elif args.event_type == 'key up' and len(args.pressed_key) == 0:
			sendColor(0,0,0)

hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook()  # hook into the events, and listen to the presses