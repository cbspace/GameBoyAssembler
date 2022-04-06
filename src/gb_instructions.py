#!/usr/bin/env python3

# Gameboy Assembler Program

from gbsem_constants import *
from gbsem_common import *

# section, used to indicate address
def asm_section(params):
	section_addr_str = params[1]
	if section_addr_str[0:4] == 'home':
		s_addr = processNumber(section_addr_str[4:].strip('[]'),16)
		if s_addr >= get_address():
			for i in range(get_address(), s_addr):
				writeIns([0xff])
		else:
			printError("Section address must occur after current address")
	return

 # add n + carry flag to A - A , n
def ins_adc(params):
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
	return

# add n to A - A , n
def ins_add(params):
	if params[0] =='a':
		base_opcode = 0x80
		n = params[1]
		if n in LIST_PARAM:
			writeIns([base_opcode + LIST_PARAM.index(n)])
		else: #number
			n_value = processN(n,8)
			if n_value == -1:
				printError("Immediate value is invalid")
			else:
				writeIns([base_opcode + 0x46,n_value])
	elif params[0] == 'hl':
		base_opcode = 0x09
		n = params[1]
		if n in LIST_PARAM_REG:
			writeIns([base_opcode + 0x10 * LIST_PARAM_REG.index(n)])
		else: #error
			printError("Register '" + params[1] + "' is invalid")
	elif params[0] == 'sp':
		n = params[1]
		n_value = processN(n,8)
		if n_value == -1:
			printError("Immediate value is invalid")
		else:
			writeIns([0xe8,n_value])
	else:
		printError("Invalid use of instruction - ADD a,n")
	return

# jump
def ins_jp(params):

	return

# call
def ins_call(params):
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
	return
