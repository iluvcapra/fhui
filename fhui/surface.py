from pygame.midi import Input, Output
from pygame.midi import time as midi_time
from fhui.message import *

class Surface:

    def __init__(self, midi_input: Input, midi_output: Output):
        self.timecode_display_f = None
        self.port_display_f = None
        self.midi_input = midi_input
        self.midi_output = midi_output
        
        self.reset_state()
    
    def reset_state(self):
        self.port_zone = None
        self.fader_pos_state = None


    def run(self):
        if not self.midi_input.poll():
            return 

        midis = self.midi_input.read(512)
        messages = list()

        for m in midis:
            print("Received midi: status=%0x, byte1=%0x, byte2=%0x" % 
                    (m[0][0], m[0][1], m[0][2]))
            if m[0][0] == 0xf0:
                continue

            message = midi2messages(m[0][0:3])
            if len(message) > 0:
                messages.append(message[0])

            print("Converted to: %s" % message)
        
        for message in messages:
            if type(message) is Ping:
                print("Received ping")
                self.ping_reply()

    def write_now(self, data : List[int]):
        now = midi_time()
        self.midi_output.write([[data, now]])

    def ping_reply(self):
        # print("Replying to ping")
        m = message2midi(PingReply())
        self.write_now(m) 

