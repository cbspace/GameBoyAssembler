#!/usr/bin/env python3.10

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

# Instructions inc r and dec r with r parameter (r=LIST_PARAM)
# dec r - decrement register r
# inc r - increment register r
def ins_generic_decn_incn(base_opcode,ins_name,params):
	if len(params) == 1:
		r = params[0]
		if r in LIST_PARAM:
			writeIns([base_opcode + 0x08 * LIST_PARAM.index(r)])
		else:
			printError("Invalid use of '" + ins_name + " r' - incorrect parameter")
	else:
		printError("Invalid use of - " + ins_name + " r - too many parameters")
	return

# Load instructions
# ------ Simple Loads use list match ------
# ld (hl-),a  - SAME AS LDD (HL),A - 0x32
# ld (hld),a  - SAME AS LDD (HL),A - 0x32
# ldd (hl),a  - Put a into address (hl) and decrement hl - 0x32
# ld (hl+),a  - SAME AS LDI (HL),A - 0x22
# ld (hli),a  - SAME AS LDI (HL),A - 0x22
# ldi (hl),a  - Put a into address (hl) and increment hl - 0x22
# ld a,(hl-)  - SAME AS LDD A,(HL) - 0x3a
# ld a,(hld)  - SAME AS LDD A,(HL) - 0x3a
# ldd a,(hl)  - Put calue at address (hl) into a and decrement hl - 0x3a
# ld a,(hl+)  - SAME AS LDI (HL),A - 0x2a
# ld a,(hli)  - SAME AS LDI (HL),A - 0x2a
# ldi a,(hl)  - Put calue at address (hl) into a and increment hl - 0x2a
# ld sp,hl    - Put hl into stack pointer - 0xf9
# ------ Loads using registers and immediates------
# ld (c),a    - Put A into address $FF00 + reg c - 0xe2
# ld a,(c)    - Put value at $FF00 + reg c into A - 0xf2
# ld a,n      - n= abcdehl(bc)(de)(hl)(d16)d8
# ld n,a      - n= abcdehl(bc)(de)(hl)(d16)
# ld r1,r2    - r1 and r2 in LIST_PARAM --& (hl),n w n=8bit Immediate
# ------ 16 Bit Loads ------
# ld n,nn     - Put nn into n (n=LIST_PARAM_REG_S),(nn=d16)
# ld nn,n     - nn = bcdehl , n = 8bit Immediate
# ld hl,sp+n  - SAME AS LDHL SP,N - 0xf8
# ld (nn),sp  - Put stack pointer at address (nn) nn=d16 - 0x08
def ins_ld(params,ins_name):
	if len(params) == 2:
		match_result = ins_ld_match(params,ins_name)
		if match_result != -1: # found a match
			writeIns([match_result])
		else: # not found keep processing
			printError("ld not found")
	else:
		printError("Invalid use of instruction '" + ins_name + "' - only allowed 2 parameters")
	return

# Test for simple ld commands and match to opcode
# Returns -1 for no match and returns opcode for a match (8bit integer)
def ins_ld_match(params,ins_name):
	for i in LIST_LD:
		if ins_name == i[0][0] and params[0] == i[0][1] and params[1] == i[0][2]:
			return i[1]
		else:
			return -1

# ldh (n),a   - Put a into memory address $FF00 + n (8bit immediate) - 0xe0
# ldh a,(n)   - Put address $FF00 + n (8bit immediate) into a - 0xf0
def ins_ldh(params):
	printError("ldh not implemented")
	return

# ldhl sp,n   - Put sp + n effective address into hl (n=d8) - 0xf8
def ins_ldhl(params):
	printError("ldhl not implemented")
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
	if len(params) == 2:
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
			if n in LIST_PARAM_REG_S:
				writeIns([base_opcode + 0x10 * LIST_PARAM_REG_S.index(n)])
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
	else:
		printError("Invalid use of instruction 'add a,n' - only allowed 2 parameters")
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

# Decrement register r or
# Increment register r
def ins_dec_inc(base_opcode_r,base_opcode_rr,ins_name,params):
	if len(params) == 1:
		r = params[0]
		if r in LIST_PARAM_REG_S:
			writeIns([base_opcode_rr + 0x10 * LIST_PARAM_REG_S.index(r)])
		else:
			ins_generic_decn_incn(base_opcode_r,ins_name,params)
	else:
		printError("Invalid use of '"+ ins_name + " r' - too many parameters")
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

# ret or ret cc - Return from subroutine or retun conditional (cc=LIST_CONDITIONS)
def ins_ret(params):
	if len(params) == 0: # ret unconditional
		writeIns([0xc9])
	elif len(params) == 1: # ret conditional (cc=nz,z,nc,c)
		cc = params[0]
		if cc in LIST_CONDITIONS:
			byte1 = 0xc0 + 0x08 * LIST_CONDITIONS.index(cc)
			writeIns([byte1])
		else:
			printError("Ret condition is not valid (cc=nz,z,nc,c)")
	else:
		printError("Invalid use of 'ret' - 0 or 1 parameters only")
	return
