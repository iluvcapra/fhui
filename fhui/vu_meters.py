from enum import Enum
from dataclasses import dataclass

class VuMeterSide(Enum):
    LEFT = 0
    RIGHT = 1

class VuMeterLevel(Enum):
    OFF      = 0x00
    GREEN_60 = 0x01
    GREEN_50 = 0x02
    GREEN_40 = 0x03
    GREEN_30 = 0x04
    GREEN_20 = 0x05
    GREEN_14 = 0x06
    GREEN_10 = 0x07
    GREEN_8  = 0x08
    YELLOW_6 = 0x09
    YELLOW_4 = 0x0a
    YELLOW_2 = 0x0b
    RED_CLIP = 0x0c


