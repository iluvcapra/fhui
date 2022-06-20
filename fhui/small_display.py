from enum import IntEnum

from dataclasses import dataclass
from typing import List

class SmallDisplayTarget(IntEnum):
    STRIP_1 = 0x00
    STRIP_2 = 0x01
    STRIP_3 = 0x02
    STRIP_4 = 0x03
    STRIP_5 = 0x04
    STRIP_6 = 0x05
    STRIP_7 = 0x06
    STRIP_8 = 0x07
    SELECT_ASSIGN = 0x08


