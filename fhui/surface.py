from pygame.midi import Input, Output
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
            message = midi2messages(m[0])
            messages.append(midi2messages(m[0]))
            print("Converted to: %s" % message)
        
        for message in messages:
            if type(message) is Ping:
                print("Received ping")
                self.reply_to_ping()

    def write_now(self, data):
        now = pygame.midi.time()
        self.midi_output.write([data, now])

    def ping_reply(self):
        # print("Replying to ping")
        m = message2midi(PingReply())
        self.write_now(m) 

