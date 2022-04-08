#!/usr/bin/env python3.10

# Gameboy Assembler Program

# Constants
LIST_CONDITIONS = ['nz','z','nc','c']
LIST_JP_OPCODE = [0xc2,0xca,0xd2,0xda]
LIST_CALL_OPCODE = [0xc4,0xcc,0xd4,0xdc]
LIST_PARAM = ['b','c','d','e','h','l','(hl)','a']
LIST_PARAM_REG = ['bc','de','hl','sp']
