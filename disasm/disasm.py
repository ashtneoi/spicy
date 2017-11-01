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
                                        0b0000: 'nop',
                                        0b0001: 'reset',
                                        0b1000: 'return',
                                        0b1001: 'retfie',
                                        0b1010: 'callw',
                                        0b1011: 'brw',
                                    }),
                                    0b1: (1, {  # 00 0000 0001
                                        0b0: 'moviw_nm',
                                        0b1: 'movwi_nm',
                                    }),
                                }),
                                0b1: 'movlb',
                            }),
                            0b1: (6, {
                                0b100010: 'option',
                                0b100011: 'sleep',
                                0b100100: 'clrwdt',
                                0b100101: 'trisa',
                                0b100110: 'trisb',
                                0b100111: 'trisc',
                            }),
                        }),
                        0b1: 'movwf',
                    }),
                    0b1: (1, {
                        0b0: 'clrw',
                        0b1: 'clrf',
                    }),
                }),
                0b1: (1, {
                    0b0: 'subwf',
                    0b1: 'decf',
                }),
            }),
            0b1: (2, {
                0b00: 'iorwf',
                0b01: 'andwf',
                0b10: 'xorwf',
                0b11: 'addwf',
            }),
        }),
        0b1: (3, {
            0b000: 'movf',
            0b001: 'comf',
            0b010: 'ncf',
            0b011: 'decfsz',
            0b100: 'rrf',
            0b101: 'rlf',
            0b110: 'swapf',
            0b111: 'incfsz',
        }),
    }),
    0b01: (2, {
        0b00: 'bcf',
        0b01: 'bsf',
        0b10: 'btfsc',
        0b11: 'btfss',
    }),
    0b10: (1, {
        0b0: 'call',
        0b1: 'goto',
    }),
    0b11: (1, {
        0b0: (1, {  # 11 0
            0b0: (1, {  # 11 00
                0b0: (1, {  # 11 000
                    0b0: 'movlw',
                    0b1: (1, {  # 11 0001
                        0b0: 'addfsr',
                        0b1: 'movlp',
                    }),
                }),
                0b1: 'bra',
            }),
            0b1: (2, {
                0b00: 'retlw',
                0b01: 'lslf',
                0b10: 'lsrf',
                0b11: 'asrf',
            }),
        }),
        0b1: (1, {
            0b0: (2, {
                0b00: 'iorlw',
                0b01: 'andlw',
                0b10: 'xorlw',
                0b11: 'subwfb',
            }),
            0b1: (2, {
                0b00: 'sublw',
                0b01: 'addwfc',
                0b10: 'addlw',
                0b11: (1, {
                    0b0: 'moviw_nk',
                    0b1: 'movwi_nk',
                }),
            }),
        }),
    }),
})


def get_opcode(insn):
    table = opcodes
    remain = 14
    while isinstance(table, tuple):
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
