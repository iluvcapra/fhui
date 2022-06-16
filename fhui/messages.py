from fhui.main_display import MainDisplay

class MessageUpdate:
    pass


class MessageConverter:
    
    def __init__(self):
        self.led_zone = None
    
    def sysex2update(self, *midi) -> List[MessageUpdate]:
        address = midi[0]
        if address == 0x10:
            #small display update
            pass
        elif address == 0x11:
            #timecode display update
            pass
        elif address == 0x12:
            return MainDisplay.Update.from_midi(midi[1:])

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
