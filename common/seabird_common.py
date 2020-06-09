from .serial_common import Serial_instrument

class Seabird_instrument(Serial_instrument):
	def __init__(self):
		# Initialize shared Instrument superclass attributes...
		super().__init__()

	def imm_timedout(self):
		if not self.buffer_empty():
			self.cap_buf()
			if "TIMEOUT" in self.buf:
				return True
		else:
			return False
	
	def imm_poweron(self):
		self.cap_cmd('')
		if "S>" in self.buf:
			return True
		elif "IMM>" in self.buf:
			return True
		else: return False
		
	def imm_setconfigtype(self, configtype, **kwargs):
	"""
	Check the configtype of the IMM and set to the desired configtype if not already
	set. The first param must be the desired configtype. This will reinitialize the
	IMM. Any additional configurations desired may be passed in as optional keyword
	value pairs.
	
	Example: instrument.imm_setconfigtype(configtype='1', setenablebinarydata='0')
	"""
		# Determine the currently set configtype of the imm...
		while True:
			print("Verifying IMM configuration...")
			self.imm_cmd('getcd')
			configtypestr = "ConfigType='"
			i = self.buf.find(configtypestr) + len(configtypestr)
			current_configtype = self.buf[i]
		
			# If different from intended configtype, change it...
			if configtype != current_configtype:
				print("Configuring IMM...")
				self.cap_cmd('*INIT')
				self.cap_cmd('*INIT')
				self.imm_poweron()
				self.cap_cmd('setconfigtype=%s' % configtype)
				self.cap_cmd('setconfigtype=%s' % configtype)
				self.imm_poweron()
				for name, value in kwargs.items():
					self.imm_cmd("%s=%s" % (name, value))
				continue
			return True

	def imm_cmd(self, cmd):
		if self.imm_timedout():
			self.imm_poweron()
		self.cap_cmd(cmd)
		
	def imm_remote_wakeup(self):
		pass
		
	def imm_remote_cmd(self, cmd):
		pass
