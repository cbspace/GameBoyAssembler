#!/usr/bin/env python3

# Gameboy Assembler Program

# Constants
CONST_VERSION = 0.1

LIST_CONDITIONS = ['nz','z','nc','c']
LIST_JP_OPCODE = [0xc2,0xca,0xd2,0xda]
LIST_CALL_OPCODE = [0xc4,0xcc,0xd4,0xdc]
LIST_PARAM = ['b','c','d','e','h','l','(hl)','a']

import sys

# Function to write instruction to rom
def writeIns(byte_array):
	global address

	for b in byte_array:
		#Write to file
		rom.append(b)
		# Increment address counter
		address += 1

	return

# Function to write bytes to output file
def writeBytes(byte_array):
#	global address	# We need to access address as global
	# Write to file
	outfile.write(bytes(byte_array))
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
				printError("Invalid constant value")
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
# Hex numbers begin with $, binary begins with # and decimal is digits only
# return value is integer value of input string
# returns -1 on error
def processNumber(number,bits):
	if number.isdecimal() == True:                 # Decimal number detected
		if int(number) < 2**(bits):
			return int(number)
		else:
			printError("Number must not be larger than " + str(bits) + " bits (max " + str(2**(bits)-1) + ")")
			return -1
	elif number[0] == '$' or number[-1] == 'h':   # Hex number detected
		if int(number[1:], 16) < 2**bits:
			return int(number[1:], 16)
		else:
			printError("Number must not be larger than " + str(bits) + " bits (max " + "#%0.2X" % (2**(bits)-1) + ")")
			return -1
	elif number[0] == '#':                         # Binary number detected
		# replace '.'s with zeros
		binary_string = number[1:].replace('.','0')
		try:
			binary_integer = int(binary_string,2)
		except:
			printError("Invalid binary representation (only 1,0 and . allowed)")		
			return -1
		if binary_integer < 2**bits:
			return binary_integer
		else:
			printError("Number must not be larger than " + str(bits) + " bits")
			return -1
	else:
		printError("Invalid integer \'" + number + "\'")
		return -1
		
# Input - n_string(string): Can be either constant name or a number
#       - bits(int): Int size measured in bits
# output - Constant value or number value
def processN(n_string,bits):
		# Search constant dictionary for string
		if n_string in assembler_constants:
			return assembler_constants.get(n_string)
		else:	# No constant found so look for number
			check_number = processNumber(n_string, bits)		
			if check_number >= 0: # Valid number is found
				return check_number
			else: # No valid number found
				printError("Invalid number or constant \'" + n_string + "\'")
				return -1

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
					byte1 = LIST_JP_OPCODE[LIST_CONDITIONS.index(cc)]
			elif ins_type == 'call':	# call nn - CD nn
				if ins_param =='':
					byte1 = 0xcd
				else:		# conditional call
					byte1 = LIST_CALL_OPCODE[LIST_CONDITIONS.index(cc)]
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
		print("\tError on line " + str(line_number) + ": " + error_text)
	else:
		print("\tError: " + error_text)
	return
	
# --------------------------------- Variables ----------------------------------
	
# Define an array for the ROM
rom = []
	
# Interger used to store current line number of input file
line_number = 0
	
# Integer used to store address (program begins at 0x100)
address = 0x00

# Count number of errors
error_count = 0

# List of parameters in a line of code
params = []

# Dictionary used to store label names and addresses
labels = {}

# List of all instructions which use labels
# Structure: ('id,('address_hex_nnn','label_name','instruction_type'))
jump_table = []

# Dictionary used to store assembler constants (equ/= definitions)
assembler_constants = {}

# --------------------------------- Program ----------------------------------

# Display Welcome Message
print("    Gameboy Assembler V" + str(CONST_VERSION))

# Check the command line arguments
if not (2 <= len(sys.argv) <= 3):
	print("\n\tAssembler Usage:")
	print("\t\"gbsem.py SourceFilePath [RomFilePath]\"\n")
	print("\tSourceFilePath: Gameboy source file, usually a .asm file extension")
	print("\t [RomFilePath]: Optional parameter used to specify output ROM file name.")
	print("\t                If omitted, the ROM file name is the input file name with .gb extension\n")
	print("\te.g \"gbsem.py source/test.asm roms/test_rom.gb\"\n")
else:
	# Store file names from command line
	filename_in = str(sys.argv[1])
	
	# Determine out file name based on command line
	if len(sys.argv) == 3:    # Out file name was provided
		filename_out = str(sys.argv[2])
	else:                     # Out file name not provided
		if filename_in.find('.') > 0:
			filename_out = filename_in[:filename_in.rfind('.')] + '.gb'
		else:
			filename_out = filename_in + '.gb'

	# Open input file readonly
	infile = open(filename_in, 'r')

	# Main loop
	for line in infile.readlines():
		# Read a line from the file and strip whitespaces and cr + lf
		data = line.strip()
		
		# Increase line counter
		line_number += 1
		
		# Strip away comments
		data = data.split(';')[0]
		data = data.strip()
		
		# If line is empty then move on
		if len(data) == 0: continue
		
		# Make line lowercase to remove any case issues
		data = data.lower()
		
		# Replace tabs with spaces to simplify parsing
		data = data.replace('\t',' ')
		
		# Look for label delimiter
		label_count = data.count(':')
		
		# If a lablel is found process it then move on to next line
		if label_count > 1:
			printError("Invalid label definition (':' can only occur once per line)")
		elif label_count == 1:
			defineLabel(data.split(':')[0])
			continue
		
		# Look for constants defined using 'EQU' or '='
		const_check = checkForConstant(data)
		if const_check == 1 or const_check == -1:
			continue
		
		#Separate instruction from parameters
		space_count = data.count(' ')

		# Find the instruction
		if space_count == 0:
			instruction = data
		elif space_count > 0:
			first_space_split = data.split(' ',1)
			instruction = first_space_split[0]	
			param_string = first_space_split[1].strip()
			# Find parameters (separated by commas)
			params = param_string.split(',')
		
		# Get rid of any pesky spaces, tabs, etc
		for i in range(len(params)):
			params[i] = params[i].strip()
		
		# Process the instruction
		if instruction == 'db' or instruction == '.db': # db n - Define byte - Writes single byte to hex file
			# Loop through params as multiple words can be used on a single line
			for b in params:
				byte1 = processN(b,8)
				writeIns([byte1])
		elif instruction == 'dw': # dw nnnn - Define word - Writes 2 bytes to hex file
			# Loop through params as multiple words can be used on a single line
			for w in params:
				byte1 = processN(w,16) >> 8
				byte2 = processN(w,16) & 0xFF
				writeIns([byte1, byte2])
		elif instruction == 'include': # include file, currently not supported
			file_name = params[0].strip('""')
			print("\t** WARNING on line " + str(line_number) + ": Include not supported yet - \"" + file_name + "\" not added **")
		elif instruction == 'section': # section, used to indicate address
			section_addr_str = params[1]
			if section_addr_str[0:4] == 'home':
				s_addr = processNumber(section_addr_str[4:].strip('[]'),16)
				if s_addr >= address:
					for i in range(address, s_addr):
						writeIns([0xff])
				else:
					printError("Section address must occur after current address")
		elif instruction == 'nop': # No op
			byte1 = 0x00
			writeIns([byte1])
		elif instruction == 'adc': # add n + carry flag to A - A , n
			base_opcode = 0x88
			if params[0] =='a':
				n = params[1]
				if n in LIST_PARAM:
					writeIns([base_opcode + LIST_PARAM.index(n)])
				else: #number
					n_value = processN(n,8)
					if n_value == -1:
						printError("Immediate value is invalid")
					else:
						writeIns([base_opcode + 0x46,n_value])
			else:
				printError("Invalid use of instruction - ADC a,n")
		elif instruction == 'ret': # ret - Return from subroutine - 0xC9
			byte1 = 0xc9
			writeIns([byte1])
		elif instruction == 'reti': # ret - Return from interrupt - 0xD9
			byte1 = 0xd9
			writeIns([byte1])
		elif instruction == 'jp':
			if len(params) == 1:
				if params[0] == '(hl)':  # jp (HL) - Jump to address in HL register
					byte1 = 0xe9
					writeIns[byte1]
					continue  # we are done here, continue loop to skip 'nn' processing below
				else:    # jp nn - Jump to address nn
					nn = processAddress(params[0],'jp')
					byte1 = 0xc3
			elif len(params) == 2: # jp cc,nn conditional jump to address nn (cc=nz,z,nc,c)
				cc = params[0]
				if cc in LIST_CONDITIONS:
					nn = processAddress(params[1],'jp',cc)
					byte1 = LIST_JP_OPCODE[LIST_CONDITIONS.index(cc)]
				else:
					printError("Jump condition is not valid (cc=nz,z,nc,c)")
			if nn == -1: # Error
				printError("Invalid address or label")
			elif nn == 0: # Label is found so leave instruction blank
				writeIns([0x00, 0x00, 0x00])
			else:          # Address is found so write the bytes
				byte3 = nn >> 8
				byte2 = nn & 0xFF
				writeIns([byte1, byte2, byte3])
		elif instruction == 'call':
			if len(params) == 1:  # call nn - Call subroutine at address nn
				nn = processAddress(params[0],'call')
				byte1 = 0xcd
			elif len(params) == 2: # call cc,nn conditional call to address nn (cc=nz,z,nc,c)
				cc = params[0]
				if cc in LIST_CONDITIONS:
					nn = processAddress(params[1],'call',cc)
					byte1 = LIST_CALL_OPCODE[LIST_CONDITIONS.index(cc)]
				else:
					printError("Call condition is not valid (cc=nz,z,nc,c)")
			if nn == -1: # Error
				printError("Invalid address or label")
			elif nn == 0: # Label is found so leave instruction blank
				writeIns([0x00, 0x00, 0x00])
			else:          # Address is found so write the bytes
				byte3 = nn >> 8
				byte2 = nn & 0xFF
				writeIns([byte1, byte2, byte3])
		else:
			printError("Invalid instruction \"" + instruction + "\"")

	# Fill in the jump instructions with associated label addresses
	fillJumps()

	# Assembly is successful
	if error_count == 0:
		# Open output file for binary writing
		outfile = open(filename_out, 'wb', buffering=0)

		# Write to file
		for x in range(0,len(rom)):
			writeBytes([rom[x]])

		# Close outfile
		outfile.close()
			
		# We are done!
		print("\tAssembly complete")
	else:
		# Errors occured
		print("\t" + str(error_count) + " error(s) occurred")

	# Close infile
	infile.close()

