from . import common
from datetime import datetime as dt

class Qct:
	def __init__(self):
		self.header = {}
		self.results_text = {}
		self.results_pass = {}
	
	def init_header(self, formnumber, docnumber, username):
		self.header['username'] = username
		self.header['formnumber'] = formnumber
		self.header['docname'] = "%s-%s" % (docnumber, formnumber)
		self.header['testdate'] = dt.today().strftime("%Y-%m-%d")

