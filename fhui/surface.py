from pygame.midi import Input as MidiInput, Output as MidiOutput, time as midi_time
import mido

from fhui.zones import ZonePort
from fhui.vpot import VPotRingAspect, VPotIdent
from fhui.main_display import MainDisplay
from fhui.small_display import SmallDisplayTarget
from fhui.time_display import TimeDisplay
from fhui.charsets import SmallDisplayCharSet, LargeDisplayCharSet

from time import monotonic

class SurfaceDelegate:
    def go_offline(self, surface):
        pass

    def go_online(self, surface):
        pass
    
    def ping_received(self, surface):
        pass

    def fader_moved(self, surface, fader_id: int, new_value: int):
        pass

    def led_changed(self, surface, led: ZonePort, new_state: bool):
        pass
    
    def vpot_changed(self, surface, ident: VPotIdent, new_state: VPotRingAspect):
        pass

    def time_display_changed(self, surface, new_value: TimeDisplay):
        pass

    def small_display_changed(self, surface, ident: SmallDisplayTarget, text: str):
        pass

    def main_display_changed(self, surface, zone: int, text: str):
        pass

    def unrecognized_message(self, surface, message: mido.Message):
        pass


class Surface:
    def __init__(self, midi_input: MidiInput, midi_output: MidiOutput, 
            delegate: SurfaceDelegate):
        self.midi_in = midi_input
        self.midi_out = midi_output
        self.delegate = delegate

        self.since_last_ping = monotonic()
        self.parser = mido.Parser()
        self.ping_timeout = 2.0

        self.online = True
        self.led_zone = None
        self.fader_state = [[None,None]] * 8

        self.time_display = TimeDisplay()
        self.main_display = MainDisplay()

    def _update_fader_state(self, order: str, fader_id: int, value: int):
        if order == 'hi':
            self.fader_state[fader_id][0] = value & 0x7f
        elif order == 'lo':
            self.fader_state[fader_id][1] = value & 0x7f

        for e in range(len(self.fader_state)):
            if self.fader_state[e][0] and self.fader_state[e][1]:
                position = (self.fader_state[e][0] << 7) ^ (self.fader_state[e][1])
                self.delegate.fader_moved(self, fader_id, position)
                self.fader_state[e] = [None, None]

    def _handle_control_change_message(self, message):
        if message.control == 0x0c:
            self.led_zone = message.value

        elif message.control == 0x2c:
            zoneport = ZonePort.from_zone_port(self.led_zone, message.value & 0x0f)
            if zoneport is None:
                self.delegate.unrecognized_message(self, message)
            elif message.value & 0xf0 == 0x40:
                self.delegate.led_changed(self, zoneport, True)
            elif message.value & 0xf0 == 0x00:
                self.delegate.led_changed(self, zoneport, False)
            else:
                self.delegate.unrecognized_message(self, message)

        elif message.control & 0xf0 == 0x10:
            vpot_ident = VPotIdent(message.control & 0x0f)
            vpot_value = VPotRingAspect(message.value)
            self.delegate.vpot_changed(self, vpot_ident, vpot_value)
 
        elif message.control & 0x0f < 0x08:
            fader_id = message.control & 0x0F
            if message.control & 0xf0 == 0x00:
                self._update_fader_state('hi', fader_id, message.value)
            elif message.control & 0xf0 == 0x20:
                self._update_fader_state('lo', fader_id, message.value)
            else:
                self.delegate.unrecognized_message(self, message)
        else: 
            self.delegate.unrecognized_message(self, message)

    def _handle_sysex(self, message):
        if message.data[0:5] != (0x00, 0x00, 0x66, 0x05, 0x00):
            self.delegate.unrecognized_message(self, message) 

        elif message.data[5] == 0x10:
            text = SmallDisplayCharSet.decode(message.data[7:])
            ident = SmallDisplayTarget(message.data[6])
            self.delegate.small_display_changed(self, ident, text)

        elif message.data[5] == 0x11:
            self.time_display.update(message.data[6:])
            self.delegate.time_display_changed(self, self.time_display)

        elif message.data[5] == 0x12:
            text = LargeDisplayCharSet.decode(message.data[7:])
            zone = message.data[6]
            self.main_display.update(zone, text)
            self.delegate.main_display_changed(self, zone, text)

        else:
            self.delegate.unrecognized_message(self, message)

    def run(self):

        if self.online and (monotonic() - self.since_last_ping > self.ping_timeout):
            self.online = False
            self.delegate.go_offline(self)
            return

        packets = []
        if self.midi_in.poll():
            packets = self.midi_in.read(1024)

        for packet in packets:
            event = packet[0]
            at_time = packet[1] 
            self.parser.feed(event)

        for message in self.parser:
            if message.type == 'note_off':
                if message.channel == 0 and message.velocity == 0x40:
                    self.delegate.ping_received(self)
                    if self.online == False:
                        self.online = True
                        self.delegate.go_online(self)
                    self.since_last_ping = monotonic()
                    self.midi_out.write_short(0x90, 0x00, 0x7f)
                else:
                    self.delegate.unrecognized_message(self, message)

            elif message.is_cc():
                self._handle_control_change_message(message)
 
            elif message.type == 'sysex':
                self._handle_sysex(message)

            elif message.type == 'polytouch':
                self._handle_vu(message)
            else:
                self.delegate.unrecognized_message(self,message)

    def send_reset(self):
        self.midi_out.write([ [[0xff], midi_time()] ] )


