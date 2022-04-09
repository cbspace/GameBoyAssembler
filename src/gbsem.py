#!/usr/bin/env python3.10

# Gameboy Assembler Program

# Constants
CONST_VERSION = 0.25

import sys

from gbsem_constants import *
from gbsem_common import *
from asm_instructions import *
from gb_instructions import *

# ------------------------- Program Start -----------------------------

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
			params = []
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
		match instruction:
			case "db": # db n - Define byte - Writes single byte to hex file
				asm_db(params)
			case '.db':
				asm_db(params)
			case 'dw': # dw nnnn - Define word - Writes 2 bytes to hex file
				asm_dw(params)
			case 'include': # include file, currently not supported
				asm_include(params)
			case 'section': # section, used to indicate address
				asm_section(params)
			case 'nop': # No op
				writeIns([0x00])
			case 'adc': # add r + carry flag to A
				ins_adc(params)
			case 'add': # add r to A
				ins_add(params)
			case 'and': # and r with A
				ins_generic_r(0xa0,'and',params)
			case 'bit': # Test bit b in register r - bit b,r
				ins_bit(params)
			case 'call': # call
				ins_call(params)
			case 'ccf': # Complement Carry Flag
				writeIns([0x3f])
			case 'cpl': # Complement A register
				writeIns([0x2f])
			case 'cp': # cp r - Compare r with A
				ins_generic_r(0xb8,'cp',params)
			case 'daa': # Decimal adjust register A
				writeIns([0x27])
			case 'dec': # Decrement register r
				ins_dec_inc(0x05,0x0b,'dec',params)
			case 'di': # Disable Interrupts
				writeIns([0xf3])
			case 'ei': # Enable Interrupts
				writeIns([0xfb])
			case 'halt': # Halt
				writeIns([0x76])
			case 'inc': # Increment register r
				ins_dec_inc(0x04,0x03,'inc',params)
			case 'jp': # Jump
				ins_jp(params)
			case 'ld': # Load
				ins_ld(params,'ld')
			case 'ldd': # Load and decrement
				ins_ld(params,'ldd')
			case 'ldh': # Load high
				ins_ldh(params)
			case 'ldi': # Load and increment
				ins_ld(params,'ldi')
			case 'ldhl': # Put sp + n effective address into hl (n=d8) - 0xf8
				ins_ldhl(params)
			case 'nop': # No op
				writeIns([0x00])
			case 'or': # Or r with A
				ins_generic_r(0xb0,'or',params)
			#case 'pop': # Pop from stack
			#case 'push': # Push to stack
			#case 'res': # Reset bit b in register r - res b,r
			case 'ret': # ret - Return from subroutine - ret or ret cc
				ins_ret(params)
			case 'reti': # ret - Return from interrupt - 0xD9
				writeIns([0xd9])

			case _:
				printError("Invalid instruction '" + instruction + "'")

	# Fill in the jump instructions with associated label addresses
	fillJumps()

	# Display errors or finalise the rom
	finalise_rom(filename_out)

	# Close infile
	infile.close()

