from fhui.main_display import MainDisplay
from fhui.time_display import TimeDisplay
from fhui.small_display import SmallDisplay
from typing import List


class MessageUpdate:
    pass


class MessageConverter:
    
    def __init__(self):
        self.led_zone = None
    
    def sysex2update(self, *sysex_payload) -> List[MessageUpdate]:
        
        address, data = sysex_payload[0], sysex_payload[1:]

        if address == 0x10:
            return SmallDisplay.Update.from_midi(data) 
        elif address == 0x11:
            return TimeDisplay.Update.from_midi(data)
        elif address == 0x12:
            return MainDisplay.Update.from_midi(data)

    def midi2update(self, *midi) -> object:
        status = midi[0]
        
        if status == 0xf7:
            #sysex        
            if midi[1:5] == [0x00, 0x00, 0x66, 0x05, 0x00]:
                 #addressed to us
                return self.sysex2update(midi[6:])
        elif status == 0x90:
            # ping 
            pass
        elif status == 0xa0:
            # vu update
            pass
        elif status == 0xb0:
            # led updates
            note = midi[1]
            if note & 0xf0 == 0x10: 
                pass
                #VPot.Update
            elif note & 0xf0 == 0x20:
                pass 
