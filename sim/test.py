#!/usr/bin/env python3


import sim


def test_init():
    d = spicy.PIC16F1454()
    d.por()
    print(' '.join('{:02X}'.format(x) for x in d.datamem[0x00:0x0C]))

def test_simple_loop():
    dev = spicy.PIC16F1454((
        # ssXXXXssssXXXX
        0b11000001111110,  # movlw 0x3E
        0b00011011110000,  # xorwf 0x70
        0b11001111111110,  # bra -2 (0x1FE)
    ))
    spicy.Emulator(dev).run()

test_simple_loop()
