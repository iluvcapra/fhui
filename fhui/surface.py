from pygame.midi import Input, Output

class Surface:

    def __init__(self, midi_input: Input, midi_output: Output):
        self.timecode_display_f = None
        self.midi_input = midi_input
        self.midi_output = midi_output

    def run(self):
        if not self.midi_input.poll():
            return 

        events = self.midi_input.read()

