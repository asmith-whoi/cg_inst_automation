from common.seabird_common import Seabird_instrument
from . import retire, qct

class Ctdmo(Seabird_instrument):
	# class variables common to all DUMMY
	proctypes = ['qct', 'retire']
	name = "CTDMO"
	
	def __init__(self):
		# Initialize shared superclass attributes...
		super().__init__()

	# these first definitions are for launching available procedures and should
	# match the above proctypes
	def retire(self):
		retire.proc_retire(self)
		
	def qct(self):
		qct.proc_qct(self)
	# --------------------------
	
	