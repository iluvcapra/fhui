from fhui.main_display import MainDisplay
from fhui.time_display import TimeDisplay
from fhui.small_display import SmallDisplay
from fhui.message_update import MessageUpdate

from typing import List


class MessageConverter:
    
    def __init__(self):
        self.led_zone = None
    
    def sysex2update(self, sysex_payload) -> List[MessageUpdate]:
        address, data = sysex_payload[0], sysex_payload[1:]

        if address == 0x10:
            return SmallDisplay.Update.from_midi(data) 
        elif address == 0x11:
            return TimeDisplay.Update.from_midi(data)
        elif address == 0x12:
            return MainDisplay.Update.from_midi(data)
        else:
            raise Exception("Unrecognized Sysex message")
    
    def parse_running_status(self, midi):
        
        words = iter(midi)
        retval = list()
        while True:
            note = next(words, None)
            if note is None:
                break
            
            try:
                if note & 0xf0 == 0x10: 
                    pass #VPot.Update
                elif note == 0x0c:
                    self.led_zone = next(words)
                elif note == 0x2c:
                    pass #led update
                elif (note & 0xf0 == 0x00) and (note & 0x0f < 0x08):
                    pass #fader update
            except StopIteration:
                raise Exception("Unexpected end of MIDI message")

        return retval

    def midi2update(self, midi) -> List[MessageUpdate]:
        status = midi[0]
        
        if status == 0xf0:
            #sysex        
            if midi[1:6] == [0x00, 0x00, 0x66, 0x05, 0x00]:
                 #addressed to us
                return self.sysex2update(midi[6:])

        elif status == 0x90:
            # ping 
            pass
        elif status == 0xa0:
            # vu update
            pass
        elif status == 0xb0:
            self.parse_running_status(midi[1:])
 
        else:
            raise Exeption("Unrecognized MIDI status word %x" % status)
