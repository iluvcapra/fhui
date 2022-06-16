from fhui.messages import MessageConverter
from fhui.main_display import MainDisplay

class TestMessageConverter:
    
    def setup(self):
        self.converter = MessageConverter()
    
    def teardown(self):
        self.converter = None

    def test_main_display_message(self):

        m = self.converter.midi2update([0xf0, 0x00, 0x00, 0x66, 0x05, 0x00,
            0x12, 0x00, 
            ord("H"), ord("e"), ord("l"), ord("l"), ord("o"),
            ord(","), ord(" "), ord("W"), ord("o"), ord("r"),
            0xf7])

        assert type(m) == MainDisplay.Update 
        
