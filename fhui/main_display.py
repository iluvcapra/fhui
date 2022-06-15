from typing import List
from dataclasses import dataclass 


@dataclass
class MainDisplayUpdate:
    zone: int
    chardata: List[int]


@dataclass
class MainDisplay:
    display_cells: List[int]

    def __init__(self):
        self.display_zones = list()
        for i in range(0,80):
            display_cells[i] = 0x20

    def line1(self) -> List[int]:
        retval = " " * 40
        for i in range(0,40):
            retval[i] = display_cells.get(i, 0x20)

        return retval

    def line2(self) -> List[int]:
        retval = " " * 40
        for i in range(40,80):
            retval[i] = display_cells.get(i, 0x20)

        return retval
    
    def update(self, updates: List[MainDisplayUpdate]):
        for update in updates:
            if update.zone not in range(0,8) or len(update.chardata) < 10:
                #fixme this is an error
                return
            
            for i in range(0,10):
                display_cells[update.zone*10 + i] = update.chardata[i]



