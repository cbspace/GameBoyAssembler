#!/usr/bin/env python3

# Gameboy Assembler Program
# Gameboy Instructions

from gbsem_constants import *
from gbsem_common import *

# Instruction with r parameter (r=LIST_PARAM)
# and r - and r with A
# cp r - Compare r with A
def ins_generic_r(base_opcode,ins_name,params):
	if len(params) == 1:
		r = params[0]
		if r in LIST_PARAM:
			writeIns([base_opcode + LIST_PARAM.index(r)])
		else: #number
			n_value = processN(r,8)
			if n_value == -1:
				printError("Immediate value is invalid")
			else:
				writeIns([base_opcode + 0x46,n_value])
	else:
		printError("Invalid use of instruction - " + ins_name + " r")
	return

 # adc - add n + carry flag to A
def ins_adc(params):
	base_opcode = 0x88
	if len(params) == 2 and params[0] =='a':
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

# add n to A
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

 # Test bit b in register r - bit b,r
def ins_bit(params):
	base_opcode = 0x40
	if len(params) == 2 and len(params[0]) == 1 and params[0].isdigit():
		b = int(params[0])
		r = params[1]
		if b <= 7:
			if r in LIST_PARAM:
				writeIns([0xcb,base_opcode + 0x08 * b + LIST_PARAM.index(r)])
		else:
			printError("Invalid bit number, must be 0 - 7")
	else:
		printError("Invalid use of instruction - bit b,r")
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
	write_nn(byte1, nn)
	return

# jump
def ins_jp(params):
	if len(params) == 1:
		if params[0] == '(hl)':  # jp (HL) - Jump to address in HL register
			writeIns([0xe9])
		else:    # jp nn - Jump to address nn
			nn = processAddress(params[0],'jp')
			write_nn(0xc3, nn)
	elif len(params) == 2: # jp cc,nn conditional jump to address nn (cc=nz,z,nc,c)
		cc = params[0]
		if cc in LIST_CONDITIONS:
			nn = processAddress(params[1],'jp',cc)
			byte1 = LIST_JP_OPCODE[LIST_CONDITIONS.index(cc)]
			write_nn(byte1, nn)
		else:
			printError("Jump condition is not valid (cc=nz,z,nc,c)")
	return

# Write ROM data for instruction with nn parameter
# Input: byte1 - the first byte (opcode)
#           nn - The processed integer
def write_nn(byte1, nn):
	if nn == -1: # Error
		printError("Invalid address or label")
	elif nn == 0: # Label is found so leave instruction blank
		writeIns([0x00, 0x00, 0x00])
	else:          # Address is found so write the bytes
		byte3 = nn >> 8
		byte2 = nn & 0xFF
		writeIns([byte1, byte2, byte3])
	return
