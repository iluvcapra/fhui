from Enum import IntFlag

class VPotRingAspect(IntFlag):
    ABS_EMPTY = 0x0
    ABS_L5 = 0x1
    ABS_L4 = 0x2
    ABS_L3 = 0x3
    ABS_L2 = 0x4
    ABS_L1 = 0x5
    ABS_CENTER = 0x6
    ABS_R1 = 0x7
    ABS_R2 = 0x8
    ABS_R3 = 0x9
    ABS_R4 = 0xa
    ABS_R5 = 0xb
    REL_EMPTY = 0x10
    REL_L5 = 0x11
    REL_L4 = 0x12
    REL_L3 = 0x13
    REL_L2 = 0x14
    REL_L1 = 0x15
    REL_CENTER = 0x16
    REL_R1 = 0x17
    REL_R2 = 0x18
    REL_R3 = 0x19
    REL_R4 = 0x1a
    REL_R5 = 0x1b
    MAG_EMPTY = 0x20
    MAG_1 = 0x21
    MAG_2 = 0x22
    MAG_3 = 0x23
    MAG_4 = 0x24
    MAG_5 = 0x25
    MAG_6 = 0x26
    MAG_7 = 0x27
    MAG_8 = 0x28
    MAG_9 = 0x29
    MAG_10 = 0x2a
    MAG_11 = 0x2b
    Q_EMPTY = 0x30
    Q_V1 = 0x31
    Q_V2 = 0x32
    Q_V3 = 0x33
    Q_V4 = 0x34
    Q_V5 = 0x35
    Q_V6 = 0x37
    Q_V7 = 0x38
    Q_V8 = 0x39
    Q_V9 = 0x3a
    Q_V10 = 0x3b



class VPotDisplay:
    ring_aspect : VPotRingAspect
    encoder_led : bool

    def __init__(self):
        ring_leds = VPotRingAspect.ABS_EMPTY
        encoder_led = False

    def update_raw(self, value):
        self.encoder_led = value & 0x40
        value &= 0x3f


