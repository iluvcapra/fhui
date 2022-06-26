from enum import IntFlag, IntEnum
from typing import List
from dataclasses import dataclass


class VPotIdent(IntEnum):
    STRIP_1 = 0x0
    STRIP_2 = 0x1
    STRIP_3 = 0x2
    STRIP_4 = 0x3
    STRIP_5 = 0x4
    STRIP_6 = 0x5
    STRIP_7 = 0x6
    STRIP_8 = 0x7
    PARAM_1 = 0x8
    PARAM_2 = 0x9
    PARAM_3 = 0xa
    PARAM_4 = 0xb


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
    Q_V6 = 0x36
    Q_V7 = 0x37
    Q_V8 = 0x38
    Q_V9 = 0x39
    Q_V10 = 0x3a
    Q_V11 = 0x3b

    def center_led_value(self):
        return self & 0x40 == 0x40

    def led_values(self):
        arc_leds = self & 0x3f
        if arc_leds in [VPotRingAspect.ABS_EMPTY, VPotRingAspect.REL_EMPTY, 
                VPotRingAspect.MAG_EMPTY, VPotRingAspect.Q_EMPTY]:
            return 0b00000000000
        elif arc_leds in [VPotRingAspect.ABS_L5, VPotRingAspect.MAG_1]:
            return 0b10000000000
        elif arc_leds == VPotRingAspect.ABS_L4:
            return 0b01000000000
        elif arc_leds == VPotRingAspect.ABS_L3:
            return 0b00100000000
        elif arc_leds == VPotRingAspect.ABS_L2:
            return 0b00010000000
        elif arc_leds == VPotRingAspect.ABS_L1:
            return 0b00001000000
        elif arc_leds in [VPotRingAspect.ABS_CENTER, 
                VPotRingAspect.REL_CENTER, 
                VPotRingAspect.Q_V1]:
            return 0b00000100000
        elif arc_leds == VPotRingAspect.ABS_R1:
            return 0b00000010000
        elif arc_leds == VPotRingAspect.ABS_R2:
            return 0b00000001000
        elif arc_leds == VPotRingAspect.ABS_R3:
            return 0b00000000100
        elif arc_leds == VPotRingAspect.ABS_R4:
            return 0b00000000010
        elif arc_leds == VPotRingAspect.ABS_R5:
            return 0b00000000001
        elif arc_leds in [VPotRingAspect.REL_L5, VPotRingAspect.MAG_6]:
            return 0b11111100000
        elif arc_leds == VPotRingAspect.REL_L4:
            return 0b01111100000
        elif arc_leds == VPotRingAspect.REL_L3:
            return 0b00111100000
        elif arc_leds == VPotRingAspect.REL_L2:
            return 0b00011100000
        elif arc_leds == VPotRingAspect.REL_L1:
            return 0b00001100000
        elif arc_leds == VPotRingAspect.REL_R1:
            return 0b00000110000
        elif arc_leds == VPotRingAspect.REL_R2:
            return 0b00000111000
        elif arc_leds == VPotRingAspect.REL_R3:
            return 0b00000111100
        elif arc_leds == VPotRingAspect.REL_R4:
            return 0b00000111110
        elif arc_leds == VPotRingAspect.REL_R5:
            return 0b00000111111
        elif arc_leds == VPotRingAspect.MAG_2:
            return 0b11000000000
        elif arc_leds == VPotRingAspect.MAG_3:
            return 0b11100000000
        elif arc_leds == VPotRingAspect.MAG_4:
            return 0b11110000000
        elif arc_leds == VPotRingAspect.MAG_5:
            return 0b11111000000
        elif arc_leds == VPotRingAspect.MAG_7:
            return 0b11111110000
        elif arc_leds == VPotRingAspect.MAG_8:
            return 0b11111111000
        elif arc_leds == VPotRingAspect.MAG_9:
            return 0b11111111100
        elif arc_leds == VPotRingAspect.MAG_10:
            return 0b11111111110
        elif arc_leds in [VPotRingAspect.MAG_11,VPotRingAspect.Q_V6, 
                VPotRingAspect.Q_V7, VPotRingAspect.Q_V8, VPotRingAspect.Q_V9, 
                VPotRingAspect.Q_V10, VPotRingAspect.Q_V11]:
            return 0b11111111111
        elif arc_leds == VPotRingAspect.Q_V2:
            return 0b00001110000
        elif arc_leds == VPotRingAspect.Q_V3:
            return 0b00011111000
        elif arc_leds == VPotRingAspect.Q_V4:
            return 0b00111111100
        elif arc_leds == VPotRingAspect.Q_V5:
            return 0b01111111110

    def led_string(self):
        leds = self.led_values()
        

        rep = "|"
        for i in reversed(range(11)):
            mask = 0x01 << i
            if (leds & mask > 0x00):
                rep += "*"
            else:
                rep += " "

        rep += "|"

        if self.center_led_value():
            rep += " (*)"
        else:
            rep += " ( )"

        return rep



