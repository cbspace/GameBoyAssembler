#!/usr/bin/env python3.10

# Gameboy Assembler Program

from gbsem_constants import *

# ---------------------------- Variables ---------------------------

# Define an array for the ROM
rom = []

# Interger used to store current line number of input file
line_number = 0

# Integer used to store address (program begins at 0x100)
address = 0x00

# Count number of errors
error_count = 0

# Dictionary used to store label names and addresses
labels = {}

# List of all instructions which use labels
# Structure: ('id,('address_hex_nnn','label_name','instruction_type'))
jump_table = []

# Dictionary used to store assembler constants (equ/= definitions)
assembler_constants = {}

# ----------------------- Common Functions --------------------------

# Get the current address
def get_address():
	return address

# Increase line counter
def inc_line_number():
	global line_number
	line_number += 1
	return

# Function to write instruction to rom
def writeIns(byte_array):
	global address

	for b in byte_array:
		if isinstance(b,int):
			#Write to file
			rom.append(b)
		else:
			printError("Error writing byte '" + str(b) + "' - not integer")
		
		# Increment address counter
		address += 1
	return

# Look for a constant definition and process it if found
# return 1 if found, 0 if not found and -1 on error
def checkForConstant(line_data):
	# Look for constants defined using 'EQU' or '='
	equ_count = line_data.count(' equ ')
	equ2_count = line_data.count(' = ')
	if equ_count + equ2_count > 1:
		printError("EQU or = can only be used once per line")
		return -1
	elif equ_count + equ2_count == 1:
		const_split = line_data.split()
		for item in const_split:
			item = item.strip() # remove spaces
		if (const_split[1] == 'equ' or const_split[1] == '=') and len(const_split) == 3:
			const_number = processNumber(const_split[2],16)
			if const_number != -1:
				defineConstant(const_split[0],const_number)
				return 1
			else:
				return -1
		else:
			printError("Too many parameters for constant definition")
			return -1
	return 0

# Function to validate and define a constant
def defineConstant(const_name,const_value):
	# Check if the constant name is valid
	# Must contain only alphanumic chars, _ and -
	# Cannot begin with number
	if labelValid(const_name) == True:
		if const_name in assembler_constants: # Check if constant aready exists
			printError("Constant " + const_name + " already exists!")
		else: # Add new constant to dictionary
			assembler_constants[const_name] = const_value
	else:
		printError("Invalid constant name, cannot begin with a number or contain invaid characters")
	return

# How labels are processed:
# Loop through the file and process instructions
# when labels are found: record address, instruction type and label name
# Loop through recorded labels and insert instruction with label address
# If there is a label with no address an error is raised

# Function to validate and define a label
def defineLabel(label_name):
	# Check if the label name is valid
	# Must contain only alphanumic chars, _ and -
	# Cannot begin with number
	if labelValid(label_name) == True:
		if label_name in labels: # Check if label aready exists
			printError("Label " + label_name + " already exists!")
		else: # Add new label to label dictionary
			labels[label_name] = address
	else:
		printError("Invalid label name, cannot begin with a number or contain invaid characters")
	return

# Function to validate label
# Return True if valid name, false otherwise
# also used to validate constant definitions
def labelValid(label_name):
	# Check if the label name is valid
	# Must contain only alphanumic chars, _ and -
	# Cannot begin with number
	test_string = label_name.replace('-','')
	test_string = test_string.replace('_','')
	if test_string.isalnum() == True:
		if test_string[0].isalpha() == True:
			return True
		else:
			return False
	else:
		return False
	return

# Input - number(str): String that is a hex, binary or decimal integer
#       - bits (int): size of integer in bits
#       - show_invalid_error(boolean): Print error message when True
# Hex numbers begin with $, binary begins with # and decimal is digits only
# return value is integer value of input string
# returns -1 on error
def processNumber(number,bits,show_invalid_error=True):
	if number.isdecimal() == True:                  # Decimal number detected
		n = check_number_size(int(number),bits)
		if n == -1:
			printError("Number must not be larger than " + str(bits) + " bits (max " + str(2**(bits)-1) + ")")
		return n
	elif number[0] == '$' or number[-1] == 'h':     # Hex number detected
		if number[0] == '$':
			n = string_to_number(number[1:],16)
		elif number[-1] == 'h':
			n = string_to_number(number[:-1],16)
		if n != -1:
			n = check_number_size(n,bits)
			if n == -1:
				printError("Number must not be larger than " + str(bits) + " bits (max " + "#%0.2X" % (2**(bits)-1) + ")")
		return n
	elif number[0] == '#' or number[0] == '%':      # Binary number detected
		# replace '.'s with zeros
		binary_string = number[1:].replace('.','0')
		n = string_to_number(binary_string,2)
		if n != -1:
			n = check_number_size(n,bits)
			if n == -1:
				printError("Number must not be larger than " + str(bits) + " bits")
		return n
	else:
		if show_invalid_error:
			printError("Invalid integer \'" + number + "\'")
		return -1

# Input - n_string(string): Can be either constant name or a number
#       - bits(int): Int size measured in bits
# output - Constant value or number value
def processN(n_string,bits):
		# Search constant dictionary for string
		if n_string in assembler_constants:
			n = check_number_size(assembler_constants.get(n_string),bits)
			if n == -1:
				printError("Number must not be larger than " + str(bits) + " bits (max " + str(2**(bits)-1) + ")")
			return n
		else:	# No constant found so look for number
			check_number = processNumber(n_string, bits, False)
			if check_number == -1:
				printError("Invalid number or constant \'" + n_string + "\'")
			return check_number

# Input - n(int): Number to test
#       - bits(int): Int size measured in bits
# output - The input n if in bouds or -1 if number too large
def check_number_size(n,bits):
	if int(n) < 2**(bits):
		return int(n)
	else:
		return -1

# Input - n_string(str): Number to convert
#       - base(int): Hex(16), decimal(10) or binary(2)
# output - The input n if valid or -1 if number invalid
def string_to_number(n_string,base):
	try:
		integer = int(n_string,base)
	except:
		printError("Invalid number representation")
		integer = -1
	return integer

# Check for valid address string or label
# when a label is found create jump table entry
# return values:
# for a valid address return the address
# return 0 when address is a label
# return -1 on error
def processAddress(address_string, instruction_type, instruction_param=''):
	# We need to know the current address
	global address

	if labelValid(address_string) == True:
		# A valid label name is found so store in jump table
		table_entry = []
		table_entry.append(address)
		table_entry.append(address_string) # label name
		table_entry.append(instruction_type)
		table_entry.append(instruction_param)
		jump_table.append(table_entry)
		return 0
	else:
		check_number = processNumber(address_string, 16)
		if check_number >= 0: # Valid number is found
			return check_number
		else:                 # No valid number found
			return -1

# Fill in all the jump statements that utilise labels
def fillJumps():
	global rom

	# Loop through all entries in jump table
	for entry in jump_table:
		# Get data from array
		addr = entry[0]
		label_name = entry[1]
		ins_type = entry[2]
		ins_param = entry[3]

		# Search label dictionary for current label
		if label_name in labels:
			label_addr = labels.get(label_name)

			# Fill in rom with instruction + label address
			if ins_type == 'jp': 		# jp nn - C3 nn
				if ins_param =='':
					byte1 = 0xc3
				else:		# conditional jump
					byte1 = LIST_JP_OPCODE[LIST_CONDITIONS.index(ins_param)]
			elif ins_type == 'ld': 		# ld n,a - EA nn
				if ins_param =='':
					byte1 = 0xea
				else:		# ld from LIST_PARAM_REG_S
					byte1 = LIST_LD_RS_OPCODE[LIST_PARAM_REG_S.index(ins_param)]
			elif ins_type == 'call':	# call nn - CD nn
				if ins_param =='':
					byte1 = 0xcd
				else:		# conditional call
					byte1 = LIST_CALL_OPCODE[LIST_CONDITIONS.index(ins_param)]
			else:
				printError('Invalid instruction found in jump table \'' + ins_type + '\'')

			# Write data to rom
			byte2 = label_addr & 0xFF
			byte3 = label_addr >> 8
			rom[addr] = byte1
			rom[addr+1] = byte2
			rom[addr+2] = byte3
		else:
			printError("Label '" + label_name + "' used but not defined", False)

# Print error message + line number
def printError(error_text, show_line_number = True):

	# Increase error count
	global error_count
	error_count += 1

	# Print error message
	if show_line_number == True:
		print("\tERROR on line " + str(line_number) + ": " + error_text)
	else:
		print("\tERROR: " + error_text)
	return

# Print warning message + line number
def printWarning(warning_text, show_line_number = True):

	# Print error message
	if show_line_number == True:
		print("\tWARNING on line " + str(line_number) + ": " + warning_text)
	else:
		print("\tWARNING: " + warning_text)
	return

# Display errors or finalise the rom
def finalise_rom(filename_out):

	# Assembly is successful
	if error_count == 0:
		# Open output file for binary writing
		outfile = open(filename_out, 'wb', buffering=0)

		# Write to file
		for x in range(0,len(rom)):
			outfile.write(bytes([rom[x]]))

		# Close outfile
		outfile.close()

		# We are done!
		print("\tAssembly complete")
	else:
		# Errors occured
		print("\t" + str(error_count) + " error(s) occurred")

	return
