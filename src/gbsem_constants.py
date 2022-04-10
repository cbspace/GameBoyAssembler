#!/usr/bin/env python3.10

# Gameboy Assembler Program
# Constants

# Conditions
LIST_CONDITIONS = ['nz','z','nc','c']

# JP and CALL Opcodes for Conditions
LIST_JP_OPCODE = [0xc2,0xca,0xd2,0xda]
LIST_CALL_OPCODE = [0xc4,0xcc,0xd4,0xdc]

# Opcodes for Load Instructions
LIST_LD_AN_OPCODE = [0x78,0x79,0x7a,0x7b,0x7c,0x7d,0x0a,0x1a,0x7e]
LIST_LD_NA_OPCODE = [0x47,0x4f,0x57,0x5f,0x67,0x6f,0x02,0x12,0x77]

# Registers
LIST_PARAM = ['b','c','d','e','h','l','(hl)','a']
LIST_PARAM_LDA = ['b','c','d','e','h','l','(bc)','(de)','(hl)']
LIST_PARAM_REG_I = ['(bc)','(de)','(hl)']
LIST_PARAM_REG_S = ['bc','de','hl','sp']

# Simple Loads use list match
LIST_LD = [
[['ld','(hl-)','a'],0x32],
[['ld','(hld)','a'],0x32],
[['ldd','(hl)','a'],0x32],
[['ld','(hl+)','a'],0x22],
[['ld','(hli)','a'],0x22],
[['ldi','(hl)','a'],0x22],
[['ld','a','(hl-)'],0x3a],
[['ld','a','(hld)'],0x3a],
[['ldd','a','(hl)'],0x3a],
[['ld','a','(hl+)'],0x2a],
[['ld','a','(hli)'],0x2a],
[['ldi','a','(hl)'],0x2a],
[['ld','($ff00+c)','a'],0xe2],
[['ld','a','($ff00+c)'],0xf2],
[['ld','sp','hl'],0xf9],
]
