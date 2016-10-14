import serial
import time
from pyhooked import Hook, KeyboardEvent, ID_TO_KEY

arduino = serial.Serial('COM3' , 115200, timeout=.1)
time.sleep(1)
flag = False

def sendColor(R,G,B, led_ids = None):
	"""
	Sends a message over serial to the connected Arduino with RGB 
	information and addresses of LEDs (optionally).
	
	Parameters:
	R: Red value (from 0 to 127)
	G: Green Value (from 0 to 127)
	B: Blue value (from 0 to 127)
	led_ids: A list of LEDs to be addressed.
	
	Returns: None.
	"""
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
	
# ################################################################################# #
# Define the Multikey Binds. These are binds that involve multiple simultaneous 
# Keypresses. Bind Objects are created and mapped to callback handlers. All objects 
# are stored in the binds list on __init__. 
# ################################################################################# #

binds = []
	
class Bind(object):
	"""
	Container class for keybinds.
	
	Parameters:
	trig: The trigger key to activate the keybind. This is the last key pressed 
		  in the sequence.
	mods: List of modifier keys that need to be held down when trigger key is 
		  pressed.
	handle: Callback function for the keybind. Executes if the keybind is 
			recognized.
	"""
	def __init__(self,trig,mods,handle):
		self.trigger_key = trig
		self.mod_keys = mods
		if trig not in self.mod_keys:
			self.mod_keys.append(trig)
		self.handler = handle
		binds.append(self)

def getBind(event):
	"""
	Get the bind on a keypress if there is one.
	"""
	for bind in binds:
		if event.current_key == bind.trigger_key and event.pressed_key == bind.mod_keys:
			return bind

	return None

# Keybind Callback Functions #
	
def ctrlJ_func(key, key_up=False):
	print "crtlJ"
	if key_up:
		return
	sendColor(127,127,127)

save = Bind('J',['Lcontrol'],ctrlJ_func)

# ############################################################################################# #
# Callback functions for individual keycode presses follow. These are stored in a dispatcher    #
# dictionary named `dispatch`. Note: It would be possible to define single keypresses as a      #
# Bind object with empty mod_keys list, however speed is key, so we want to keep the number of  #
# objects that getBind() iterates over to a minimum. Therfore a dispatcher is ideal since it    #
# will know the callback to use for a given key without need to check all of them.              #
# ############################################################################################# #
	
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
	
	sendColor(42,8,71)

def enterPress(key, key_up=False):
	if key_up:
		return
	
	sendColor(0,127,0)
	
def escapePress(key, key_up=False):
	if key_up:
		return
	
	sendColor(127,0,0)

def wasd(key, key_up=False):
	if key_up:
		return
	
	sendColor(127,0,0)

dispatch = {}
for key in ID_TO_KEY:
	item = ID_TO_KEY[key]
	if item in [str(s)for s in range(0,10)] or item in ['Numpad{}'.format(s) for s in range(0,10)]:
		dispatch[item] = numberPress
	elif item == 'Return':
		dispatch[item] = enterPress
	elif item == 'Escape':
		dispatch[item] = escapePress
	elif item in ['W','A','S','D']:
		dispatch[item] = wasd
	elif item.isalpha() and len(item) == 1:
		dispatch[item] = letterPress
	else:
		dispatch[item] = otherPress

def handle_events(args):
	"""
	Main Handler Function. First checks for keybinds, then failing results in dispatching 
	the handler for a 'key down' event, followed by a 'key up', and finally simply sending 
	a message to turn off the LEDs.
	
	Parameters: PyHooked::KeyboardEvent object
	"""
	if isinstance(args, KeyboardEvent):
		try:
			getBind(args).handler(args.current_key)
		except AttributeError:
			if args.event_type == 'key down':
				dispatch[args.current_key](args.current_key)
			elif args.event_type == 'key up' and len(args.pressed_key) > 0:
				dispatch[args.current_key](args.current_key, key_up=True)
			else:
				sendColor(0,0,0)
			
hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events
hk.hook()  # hook into the events, and listen to the presses