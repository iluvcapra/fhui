from typing import List

class MainDisplay:
    display_cells: List[int]

    def __init__(self):
        display_zones = list()
        for i in range(0,80):
            display_cells[i] = 0x20

    def line1(self) -> str:
        retval = " " * 40
        for i in range(0,40):
            retval[i] = display_cells.get(i, " ")

        return retval

    def line2(self) -> str:
        retval = " " * 40
        for i in range(40,80):
            retval[i] = display_cells.get(i, " ")

        return retval

    def update(self, zone: int, chars: List[int]):
        if zone not in range(0,8) or len(chars) < 10:
            #fixme this is an error
            return
        
        for i in range(0,10):
            display_cells[zone*10 + i] = chars[i]



