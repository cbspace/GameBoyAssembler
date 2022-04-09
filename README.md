 #H1 gbsem Gameboy ROM Assembler

 A simple Gameboy DMG ROM Assembler written in Python3.

 #H3 Features

 * Wide variey of asm sytax accepted
 * Descriptive error messages when errors are found

 #H3 Requirements

 1. Python 3.10 or greater
 To install (Debian based distros): sudo apt-get install python3.10

 2. Files must be executable i.e.
 `chmod 777 src/*`

 #H3 Command line usage (Linux):

Input file: Gameboy assembly code (usually .asm).
Output file: Gameboy rom (.gb)

`./src/gbsem.py path_to_input [path_to_output]`
eg. `./src/gbsem.py ~/gb/mygame.asm ~/gb/rom/mygamerom.gb`

If output filename is not specified it will be the input filename with a .gb extension in the same directory as the input.
