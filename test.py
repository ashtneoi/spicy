#!/usr/bin/env python3


import spicy


spicy.Emulator(spicy.PIC16F1454(), (
    # ssXXXXssssXXXX
    0b11000001111110,  # movlw 0x3E
    0b00011011110000,  # xorwf 0x70
    0b11001111111110,  # bra -2 (0x1FE)
)).run()
