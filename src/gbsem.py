#!/usr/bin/env python3

# Gameboy Assembler Program

# Constants
CONST_VERSION = 0.22

import sys

from gbsem_constants import *
from gbsem_common import *
from asm_instructions import *
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
			asm_db(params)
		elif instruction == 'dw': # dw nnnn - Define word - Writes 2 bytes to hex file
			asm_dw(params)
		elif instruction == 'include': # include file, currently not supported
			asm_include(params)
		elif instruction == 'section': # section, used to indicate address
			asm_section(params)
		elif instruction == 'nop': # No op
			writeIns([0x00])
		elif instruction == 'adc': # add n + carry flag to A
			ins_adc(params)
		elif instruction == 'add': # add n to A
			ins_add(params)
		elif instruction == 'and': # and n with A
			ins_generic_r(0xa0,'and',params)
		elif instruction == 'bit': # Test bit b in register r - bit b,r
			ins_bit(params)
		elif instruction == 'call': # call
			ins_call(params)
		elif instruction == 'ccf': # Complement Carry Flag
			writeIns([0x3f])
		elif instruction == 'cpl': # Complement A register
			writeIns([0x2f])
		elif instruction == 'cp': # cp r - Compare r with A
			ins_generic_r(0xb8,'cp',params)
		elif instruction == 'daa': # Decimal adjust register A
			writeIns([0x27])
		elif instruction == 'dec': # Decrement register r
			ins_dec(params)

		elif instruction == 'ret': # ret - Return from subroutine - 0xC9
			byte1 = 0xc9
			writeIns([byte1])
		elif instruction == 'reti': # ret - Return from interrupt - 0xD9
			byte1 = 0xd9
			writeIns([byte1])
		elif instruction == 'jp': #jump
			ins_jp(params)
		else:
			printError("Invalid instruction \"" + instruction + "\"")

	# Fill in the jump instructions with associated label addresses
	fillJumps()

	# Display errors or finalise the rom
	finalise_rom(filename_out)

	# Close infile
	infile.close()

