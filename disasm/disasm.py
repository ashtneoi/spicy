opcodes = (2, {
    0b00: (1, {
        0b0: (1, {  # 00 0
            0b0: (1, {  # 00 00
                0b0: (1, {  # 00 000
                    0b0: (1, {  # 00 0000
                        0b0: (1, {  # 00 0000 0
                            0b0: (1, {  # 00 0000 00
                                0b0: (1, {  # 00 0000 000
                                    0b0: (4, {  # 00 0000 0000
                                        0b0000: ('nop', 'E'),
                                        0b0001: ('reset', 'E'),
                                        0b1000: ('return', 'E'),
                                        0b1001: ('retfie', 'E'),
                                        0b1010: ('callw', 'E'),
                                        0b1011: ('brw', 'E'),
                                    }),
                                    0b1: (1, {  # 00 0000 0001
                                        0b0: ('moviw_nm', 'NM'),
                                        0b1: ('movwi_nm', 'NM'),
                                    }),
                                }),
                                0b1: ('movlb', 'K5'),
                            }),
                            0b1: (6, {
                                0b100010: ('option', 'E'),
                                0b100011: ('sleep', 'E'),
                                0b100100: ('clrwdt', 'E'),
                                0b100101: ('trisa', 'E'),
                                0b100110: ('trisb', 'E'),
                                0b100111: ('trisc', 'E'),
                            }),
                        }),
                        0b1: ('movwf', 'F'),
                    }),
                    0b1: (1, {
                        0b0: ('clrw', 'X2'),
                        0b1: ('clrf', 'F'),
                    }),
                }),
                0b1: (1, {
                    0b0: ('subwf', 'DF'),
                    0b1: ('decf', 'DF'),
                }),
            }),
            0b1: (2, {
                0b00: ('iorwf', 'DF'),
                0b01: ('andwf', 'DF'),
                0b10: ('xorwf', 'DF'),
                0b11: ('addwf', 'DF'),
            }),
        }),
        0b1: (3, {
            0b000: ('movf', 'DF'),
            0b001: ('comf', 'DF'),
            0b010: ('incf', 'DF'),
            0b011: ('decfsz', 'DF'),
            0b100: ('rrf', 'DF'),
            0b101: ('rlf', 'DF'),
            0b110: ('swapf', 'DF'),
            0b111: ('incfsz', 'DF'),
        }),
    }),
    0b01: (2, {
        0b00: ('bcf', 'BF'),
        0b01: ('bsf', 'BF'),
        0b10: ('btfsc', 'BF'),
        0b11: ('btfss', 'BF'),
    }),
    0b10: (1, {
        0b0: ('call', 'K11'),
        0b1: ('goto', 'K11'),
    }),
    0b11: (1, {
        0b0: (1, {  # 11 0
            0b0: (1, {  # 11 00
                0b0: (1, {  # 11 000
                    0b0: ('movlw', 'K8'),
                    0b1: (1, {  # 11 0001
                        0b0: ('addfsr', 'NK'),
                        0b1: ('movlp', 'K7'),
                    }),
                }),
                0b1: ('bra', 'K9'),
            }),
            0b1: (2, {
                0b00: ('retlw', 'K8'),
                0b01: ('lslf', 'DF'),
                0b10: ('lsrf', 'DF'),
                0b11: ('asrf', 'DF'),
            }),
        }),
        0b1: (1, {
            0b0: (2, {
                0b00: ('iorlw', 'K8'),
                0b01: ('andlw', 'K8'),
                0b10: ('xorlw', 'K8'),
                0b11: ('subwfb', 'DF'),
            }),
            0b1: (2, {
                0b00: ('sublw', 'K8'),
                0b01: ('addwfc', 'DF'),
                0b10: ('addlw', 'K8'),
                0b11: (1, {
                    0b0: ('moviw_nk', 'NK'),
                    0b1: ('movwi_nk', 'NK'),
                }),
            }),
        }),
    }),
})


def get_opcode(insn):
    table = opcodes
    remain = 14
    while isinstance(table[0], int):
        width, segs = table
        remain -= width
        table = segs[insn >> remain]
        insn = insn & ((1 << remain) - 1)
    return table


def test_opcodes():
    prev = None
    for insn in range(0, 1<<14):
        try:
            o = get_opcode(insn)
            if o != prev:
                print(o)
                prev = o
        except KeyError:
            pass

test_opcodes()
