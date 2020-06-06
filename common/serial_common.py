from serial import Serial
from serial.tools import list_ports
from workbench import Instrument
from . import common

class Serial_instrument(Instrument):
	def __init__(self):
		# Initialize shared Instrument superclass attributes...
		super().__init__()

		self.ser = Serial()
		self.ser.baudrate = self.baudrate
		self.ser.timeout = self.timeout
		self.port = None
		self.capfile = "Serial_instrument.log"	# Default should be overridden in instrument-specific module

	def set_serialport(self):
		ports = [port for port in list_ports.comports()]
		portmenu = ["%s - %s" % (port.device, port.description) for port in ports]

		# Present port selection menu to user...
		userselection = common.dynamicmenu_get("Select an available port", portmenu, lastitem=('C', 'Cancel'))
		if not userselection:
			# Cancelled by user...
			return False
		
		port_id = int(userselection)
		self.port = ports[port_id]
		self.ser.port = self.port[0]
		return True

	def serialport_open(self):
		"""Open connection to a serial port and start logging to a file."""
		while not self.port:
			# No port chosen, try to choose one...
			if not self.set_serialport():
				again = input("Would you like to try to connect again? y/[n] ")
				if again.lower() != "y":
					# Cancelled by user...
					return False
		try:
			self.ser.open()
		except BaseException as msg:
			input("\nError! %s [Press ENTER to continue]..." % msg)
			return False
		print("Connected to %s." % self.port)
		return True

	def cap_cmd(self, cmd):
		"""
		Send a single commmand cmd to an instrument. Write the reply to the
		capture file. If instrument echoes the command, the command will also
		be captured.
		"""
		self.ser.reset_input_buffer()
		self.ser.write((cmd + '\r\n').encode('ascii'))
		buf = self.ser.read(self.ser.in_waiting).decode('ascii')
		while True:
			cur = buf
			buf += self.ser.read(1).decode('ascii')
			if cur == buf:
				with open(self.capfile, 'a') as capfile:
					capfile.write(buf)
					return True

	def cap_cmd_forceecho(self, cmd):
		"""
		Send a single commmand cmd to an instrument. Write the command and the
		reply to the capture file separately. If instrument echoes the command,
		the command be captured twice.
		"""
		with open(self.capfile, 'a') as capfile:
			capfile.write(cmd + '\r\n')
		self.ser.reset_input_buffer()
		self.ser.write((cmd + '\r\n').encode('ascii'))
		buf = self.ser.read(self.ser.in_waiting).decode('ascii')
		while True:
			cur = buf
			buf += self.ser.read(1).decode('ascii')
			if cur == buf:
				with open(self.capfile, 'a') as capfile:
					capfile.write(buf)
					return True

	def connect(self):
		return self.serialport_open()
	
	def connected(self):
		return self.ser.is_open
	
	def disconnect(self):
		self.ser.close()
		return not self.ser.is_open