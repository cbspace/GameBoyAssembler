; Test Program "Hello World"

; ROM Begins at $0100
section "ROM Begin", home($0100)
	nop
	jp start

; ROM Configuration Data
section "ROM Config", home($0134)
	; Game Title - "HELLO"
	db $48,$45,$4c,$4c,$4f,$00,$00,$00
	db $00,$00,$00,$00,$00,$00,$00,$00

; Beginning of Code
section "Code Begin", home($0150)

start:
	xor a
	
	
	
	

; Working RAM
section "WRAM", home($c000)

char_h: 
	db %.1....1.
	db %.1....1.
	db %.1....1.
	db %.111111.
	db %.1....1.
	db %.1....1.
	db %.1....1.
	db %........
	
char_e: 
	db %.111111.
	db %.1......
	db %.1......
	db %.111111.
	db %.1......
	db %.1......
	db %.111111.
	db %........
	
char_l: 
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.111111.
	db %........
	
char_o: 
	db %..1111..
	db %.1....1.
	db %.1....1.
	db %.1....1.
	db %.1....1.
	db %.1....1.
	db %..1111..
	db %........
	
char_bang: 
	db %.11.....
	db %.11.....
	db %.11.....
	db %.11.....
	db %.11.....
	db %........
	db %.11.....
	db %........
