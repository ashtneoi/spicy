from random import randrange

from utils import Constant


MOVLW = Constant('MOVLW')
XORWF = Constant('XORWF')
BRA = Constant('BRA')


class Device(object):
    pass


class PIC16F1454(Device):
    PCH = 0

    # POR/BOR, all other resets
    meminit = [None] * 0x1000
    meminit[0x000] = 'xxxx xxxx'
    meminit[0x001] = 'xxxx xxxx'
    meminit[0x002] = '0000 0000'
    meminit[0x003] = '---1 1000 ---q quuu'
    meminit[0x004] = '0000 0000 uuuu uuuu'
    meminit[0x005] = '0000 0000'
    meminit[0x006] = '0000 0000 uuuu uuuu'
    meminit[0x007] = '0000 0000'
    meminit[0x008] = '---0 0000'
    meminit[0x009] = '0000 0000 uuuu uuuu'
    meminit[0x00A] = '-000 0000'
    meminit[0x00B] = '0000 0000'

    def __init__(self):
        self.datamem = [0] * 0x1000
        for i in range(0x1000):
            self.datamem[i] = randrange(0x00, 0x100)

    # `a` is a traditional address
    def rw(self, a, d=None):
        if a >= 0x80:
            a2 = a & 0x7F
            if 0x00 <= a2 <= 0x0B or 0x70 <= a2 <= 0x7F:
                a = a2
        d0 = self.datamem[a]
        if d is not None:
            self.datamem[a] = d
        return d0

    def por(self):
        self.PCH = 0

        for a, init in enumerate(self.meminit):
            if init is not None:
                porbor = init[0:4] + init[5:9]
                val = self.datamem[a]
                for n, spec in enumerate(porbor):
                    if spec == 'x':
                        bit = randrange(0, 2)
                    elif spec == 'u':
                        continue
                    elif spec == 'q':
                        continue  # ??
                    elif spec == '-':
                        val = 0
                    elif spec == 'r':
                        raise Exception("eh?")
                    elif spec == '0':
                        val = 0
                    elif spec == '1':
                        val = 1
                    else:
                        raise Exception("eh?")
                    val = (val & (0xFF ^ (1 << n))) | (bit << n)
                self.datamem[a] = val

    def do(self, insn):
        three = insn >> 11
        rest = insn & ((1 << 11) - 1)
        if three == 0b110:
            if (rest >> 8) == 0b000:
                op = MOVLW
            elif (rest >> 9) == 0b01:
                op = BRA
            else:
                raise Exception("eh?")
        elif three == 0b000:
            if (rest >> 8) == 0b110:
                op = XORWF
            else:
                raise Exception("eh?")
        else:
            raise Exception("eh?")

        print(op)


class Emulator(object):
    def __init__(self, device, progmem):
        self.device = device
        self.progmem = progmem

    def run(self):
        self.device.por()

        while True:
            a = (self.device.PCH << 8) | self.device.rw(0x02)
            self.device.do(self.progmem[a])
            a += 1
            self.device.PCH = a >> 8
            self.device.rw(0x02, a & 0xFF)
