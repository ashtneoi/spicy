#!/usr/bin/env python3


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
                                        0b0: ('moviw', 'NM'),
                                        0b1: ('movwi', 'NM'),
                                    }),
                                }),
                                0b1: ('movlb', 'K5'),
                            }),
                            0b1: (6, {
                                0b100010: ('option', 'E'),
                                0b100011: ('sleep', 'E'),
                                0b100100: ('clrwdt', 'E'),
                                0b100101: ('tris TRISA', 'E'),
                                0b100110: ('tris TRISB', 'E'),
                                0b100111: ('tris TRISC', 'E'),
                            }),
                        }),
                        0b1: ('movwf', 'F'),
                    }),
                    0b1: (1, {
                        0b0: (5, {
                            0b00000: ('clrw', 'X2'),
                        }),
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
                    0b0: ('moviw', 'NK'),
                    0b1: ('movwi', 'NK'),
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


def twos_comp(x, n):
    if x >= (1 << (n - 1)):
        return -((1 << n) - (x & ((1 << n) - 1)))
    else:
        return x


def disasm_insn(insn):
    opc, fmt = get_opcode(insn)

    if fmt == 'E' or fmt == 'X2':
        return opc
    elif fmt == 'K5':
        k = insn & ((1 << 5) - 1)
        return opc + ' 0x{:02X}'.format(k)
    elif fmt == 'K7' or fmt == 'F':
        k = insn & ((1 << 7) - 1)
        return opc + ' 0x{:02X}'.format(k)
    elif fmt == 'K8':
        k = insn & ((1 << 8) - 1)
        return opc + ' 0x{:02X}'.format(k)
    elif fmt == 'K9':
        k = twos_comp(insn & ((1 << 9) - 1), 9)
        return opc + ' {}0x{:03X}'.format('-' if k < 0 else '', abs(k))
    elif fmt == 'K11':
        k = insn & ((1 << 11) - 1)
        return opc + ' 0x{:03X}'.format(k)
    elif fmt == 'DF':
        d = (insn & (1 << 7)) >> 7
        f = insn & ((1 << 7) - 1)
        return opc + ' 0x{:02X}{}'.format(f, ', W' if d == 1 else '')
    elif fmt == 'BF':
        b = (insn & (0b111 << 7)) >> 7
        f = insn & ((1 << 7) - 1)
        return opc + ' 0x{:02X}, {}'.format(f, b)
    elif fmt == 'NM':
        n = (insn & (1 << 2)) >> 2
        m = insn & ((1 << 2) - 1)
        if m == 0:
            a = '++FSR{}'
        elif m == 1:
            a = '--FSR{}'
        elif m == 2:
            a = 'FSR{}++'
        else:
            a = 'FSR{}--'
        return opc + ' ' + a.format(n)
    elif fmt == 'NK':
        n = (insn & (1 << 6)) >> 6
        k = twos_comp(insn & ((1 << 6) - 1), 6)
        return opc + ' {}{}[FSR{}]'.format('-' if k < 0 else '', abs(k), n)
    else:
        raise Exception('Unrecognized format {}'.format(fmt))


def disasm_bin(f):
    while True:
        b = f.read(2)
        if len(b) == 0:
            break
        elif len(b) == 1:
            raise Exception("Odd file size")
        insn = b[0] | ((b[1] & ((1 << 6) - 1)) << 8)
        print(disasm_insn(insn))


def print_all_opcodes():
    prev = None
    for insn in range(0, 1<<14):
        try:
            o = get_opcode(insn)
            if o != prev:
                print(o)
                prev = o
        except KeyError:
            pass


def print_all_insns():
    prev = None
    for insn in range(0, 1<<14):
        try:
            print(disasm_insn(insn))
        except KeyError:
            pass


if __name__ == '__main__':
    from sys import argv, stderr

    if len(argv) != 2:
        print("Usage: {} FILENAME".format(argv[0]))
        exit(1)
    with open(argv[1], 'rb') as f:
        disasm_bin(f)
