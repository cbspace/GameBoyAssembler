 # gbsem Gameboy Assembler in Python #

 A simple Gameboy DMG Assembler.

 Requirements:
 1. Python 3.10 or greater
 To install (Debian based distros): sudo apt-get install python3.10

 2. Files must be executable i.e.
 chmod 777 src/*

 Command line usage (Linux):
 ./src/gbsem.py path_to_input [path_to_output]

 Input file: Gameboy assembly code (usually .asm).
 Output file: Gameboy rom (.gb)

If output filename is not specified it will be the input filename with a .gb extension.
