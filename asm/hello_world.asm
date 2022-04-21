; Test Program "Hello World"
; Used to test the gbsem assembler
;
; Display the message on the screen using background tiles.
; Then clear the screen and display the message again using sprites.

; Constants - Addresses
A_TDT1    =  $8000      ; Tile Data Table 1 start address (Sprite, BG, Window: 0->255)
A_BGTM1   =  $9800      ; Background Tile Map 1 start address
A_WRAM    =  $c000      ; Working RAM

; Constants - Registers
R_LCDC    =  $ff40      ; LCD Control
R_LCDSTAT =  $ff41      ; LCD Status
R_SCY     =  $ff42      ; Scroll Y
R_SCX     =  $ff43      ; Scroll X
R_LY      =  $ff44      ; LCD Y coordinate
R_LYC     =  $ff45      ; LY Compare
R_DMA     =  $ff46      ; Direct Memory Access

; ROM Begins at $0100
section "ROM Begin", home($0100)
	nop
	jp  start

; ROM Configuration Data
section "ROM Config", home($0134)
	; Game Title - "HELLO"
	db $48,$45,$4c,$4c,$4f,$00,$00,$00
	db $00,$00,$00,$00,$00,$00,$00,$00

; Beginning of Code
section "Code Begin", home($0150)

start:
	ld  hl , A_TDT1
	
	
	
	

; Working RAM
section "WRAM", home(A_WRAM)

; Tile Data Table Data for background (32x32)
; Middle 2 rows shown - h = 1, e = 2 etc
tdt_data:
	db 0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0	
	db 0,0,0,0,0,0,0,0,0,0,0,0,0,5,4,6,3,7,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0

; The below characters represent the outlines.
; Each byte is doubled to make the 1's 3's (darkest colour)
char_blank:
	dw 0,0,0,0,0,0,0,0

char_h: 
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1111111
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %........
	
char_e: 
	db %.1111111
	db %.1......
	db %.1......
	db %.1111111
	db %.1......
	db %.1......
	db %.1111111
	db %........
	
char_l: 
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.1......
	db %.1111111
	db %........
	
char_o: 
	db %..11111.
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %..11111.
	db %........

char_w: 
	db %.1..1..1
	db %.1..1..1
	db %.1.1.1.1
	db %.1.1.1.1
	db %.1.1.1.1
	db %.1.1.1.1
	db %..1...1.
	db %........

char_r: 
	db %..11111.
	db %.1.....1
	db %.1.....1
	db %.111111.
	db %.1...1..
	db %.1....1.
	db %.1.....1
	db %........

char_d: 
	db %.111111.
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.111111.
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

tile_bg: 
	db %.111111.
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.1.....1
	db %.111111.
	db %........