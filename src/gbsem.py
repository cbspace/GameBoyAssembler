#!/usr/bin/env python3

# Gameboy Assembler Program

# Constants
CONST_VERSION = 0.2

import sys

from gbsem_constants import *
from gbsem_common import *
from gb_instructions import *

# --------------------------------- Program Start ----------------------------------

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
		inc_line_number()
		
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
			asm_section(params)
		elif instruction == 'nop': # No op
			byte1 = 0x00
			writeIns([byte1])
		elif instruction == 'adc': # add n + carry flag to A - A , n
			ins_adc(params)
		elif instruction == 'add': # add n to A - A , n
			ins_add(params)
		elif instruction == 'ret': # ret - Return from subroutine - 0xC9
			byte1 = 0xc9
			writeIns([byte1])
		elif instruction == 'reti': # ret - Return from interrupt - 0xD9
			byte1 = 0xd9
			writeIns([byte1])
		elif instruction == 'jp': #jump
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
		elif instruction == 'call': # call
			ins_call(params)
		else:
			printError("Invalid instruction \"" + instruction + "\"")

	# Fill in the jump instructions with associated label addresses
	fillJumps()

	# Display errors or finalise the rom
	finalise_rom(filename_out)

	# Close infile
	infile.close()

