#!/usr/bin/env python3.10

# Gameboy Assembler Program
# Assembler Instructions

from gbsem_common import *

# Section, used to indicate address
# Syntax: 'Section "name",HOME[$address]'
def asm_section(params):
	section_addr_str = params[1]
	if section_addr_str[0:4] == 'home':
		s_addr = processNumber(section_addr_str[4:].strip('()'),16)
		if s_addr >= get_address():
			for i in range(get_address(), s_addr):
				writeIns([0xff])
		else:
			printError("Section address must occur after current address")
	return

# db n - Define byte - Writes single byte to hex file
def asm_db(params):
	# Loop through params as multiple words can be used on a single line
	for b in params:
		byte1 = processN(b,8)
		writeIns([byte1])
	return

# dw nn - Define word - Writes 2 bytes to hex file
def asm_dw(params):
	# Loop through params as multiple words can be used on a single line
	for w in params:
		int_str = w.replace("l","$") # replace l characters that appear in some disassemblies
		byte1 = processN(int_str,16) >> 8
		byte2 = processN(int_str,16) & 0xFF
		writeIns([byte1, byte2])
	return

# include file, currently not supported
def asm_include(params):
	file_name = params[0].strip('""')
	printWarning("Include not supported yet - \"" + file_name + "\" not added",True)
	return
