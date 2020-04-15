import workbench
from importlib import import_module

def mainmenu():
	"""
	Displays the main menu for the program with header and list of instruments.
	The instrument list is generated dynamically from a list of instruments that
	are known to the workbench.py module.
	"""
	print("\n")
	print("-" * 20, "OOI CGSN INSTRUMENT", "-" * 20)
	print(" " * 14, "AUTOMATED INSTRUMENT PROCEDURES")
	print(" " * 23, "Version 1.0a")
	print("-" * 61)
	print("Select an instrument:")
	menuid = []   # Dynamic menu. See workbench module...
	for i, inst in enumerate(workbench.known_inst):
		menuid.append(str(i+1))
		print("%s) %s" % (menuid[i], inst.upper()))
	print("Q) Quit")
	selection = input("Enter your selection: ")
	
	if selection.lower() == 'q':
		return None
	elif selection in menuid:
		return selection
	else:
		return 999
		
def main():
	while True:
		selection = mainmenu()
		if not selection:
			break
		elif selection == 999:
			input("\nError! Unrecognized entry [Press ENTER to continue]...")
			continue
		else:
			chosen_instrument = workbench.known_inst[int(selection)-1]
			print("\nI see you have selected %s" % chosen_instrument.upper())
			response = input("Is this correct? [y]/n ")
			if response.lower() == 'n':
				continue
			else:
				# Dynamic loading of the module for the selected instrument, then
				# defining 'instrument' as an instance of instrument Class
				# from that module. The Class name must be the Capitalized
				# module name. This must be defined in the relevant module.
				instmod = import_module('instruments.%s' % chosen_instrument)
				instrclass = getattr(instmod, chosen_instrument.capitalize())
				instrument = instrclass(chosen_instrument)
				
				# With an instrument defined, the available procedures will be
				# presented dynamically by the workshop module, where one will
				# be chosen by the user and further actions will happen...
				instrument.select_proc()
			
			
			
main()
print("Good bye!\n")