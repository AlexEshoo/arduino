import serial
import time
from pyhooked import Hook, KeyboardEvent, ID_TO_KEY

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

binds = []
	
class Bind(object):
	def __init__(self,trig,mods,handle):
		self.trigger_key = trig
		self.mod_keys = mods
		if trig not in self.mod_keys:
			self.mod_keys.append(trig)
		self.handler = handle
		binds.append(self)

def ctrlJ_func(key, key_up=False):
	print "crtlJ"
	if key_up:
		return
	sendColor(127,127,127)

save = Bind('J',['Lcontrol'],ctrlJ_func)

def goBind(event):
	for bind in binds:
		if event.current_key == bind.trigger_key and event.pressed_key == bind.mod_keys:
			return bind

	return None
	
def numberPress(num, key_up=False):
	if int(num) in range(0,10):
		if key_up:
			sendColor(0,0,0,led_ids = [int(num)])
		else:
			sendColor(127,127,127,led_ids = [int(num)])

def letterPress(l, key_up=False):
	if key_up:
		return
		
	sendColor(0,127,127)
	
def otherPress(key, key_up=False):
	if key_up: 
		return
	
	sendColor(0,0,127)

dispatch = {}
for key in ID_TO_KEY:
	item = ID_TO_KEY[key]
	if item.isalpha() and len(item) == 1:
		dispatch[item] = letterPress
	elif item in [str(s)for s in range(0,10)] or item in ['Numpad{}'.format(s) for s in range(0,10)]:
		dispatch[item] = numberPress
	else:
		dispatch[item] = otherPress
		
def handle_events(args):
	if isinstance(args, KeyboardEvent):
		try:
			goBind(args).handler(args.current_key)
		except AttributeError:
			if args.event_type == 'key down':
				dispatch[args.current_key](args.current_key)
			elif args.event_type == 'key up' and len(args.pressed_key) > 0:
				dispatch[args.current_key](args.current_key, key_up=True)
			else:
				sendColor(0,0,0)
			
hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook()  # hook into the events, and listen to the presses