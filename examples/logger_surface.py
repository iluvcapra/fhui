import pygame.midi

import sys
sys.path.insert(0, '.')

from enum import Enum

from fhui.charsets import LargeDisplayCharSet, SmallDisplayCharSet
from fhui.zones import ZonePort
from fhui.vpot import VPotIdent, VPotRingAspect

import mido

from optparse import OptionParser, OptionGroup
import sys
import re
from time import sleep, monotonic as now, strftime
import codecs

import fileinput

DEFAULT_MIDI_IN_RX=r'^.*HUI In$'
DEFAULT_MIDI_OUT_RX=r'^.*HUI Out$'

if not pygame.midi.get_init():
    pygame.midi.init()

script_start = now()

def log_out(m):
    print("%s (%f): %s" % (strftime("%H:%M:%S"), now() - script_start, m))


def print_endpoint(index: int):
    f, n, xi, xo, op = pygame.midi.get_device_info(index)
    dirn = None
    if xi > 0:
        dirn = "IN"
    else:
        dirn = "OUT"

    log_out("%i - %s : %s (%s)" % (index, codecs.decode(f, 'utf8'), codecs.decode(n, 'utf8'), dirn))

def iterate_endpoints():
    for i in range(pygame.midi.get_count()):
        f, n, xi, xo, op = pygame.midi.get_device_info(i)
        yield (i, codecs.decode(f, 'utf8'), codecs.decode(n, 'utf8'), xi, xo, op)

def list_endpoints():
    log_out("Inputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_input == 1:
            print("%i - %s : %s" % (index, interface, name))

    log_out("")
    log_out("Outputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_output == 1:
            log_out("%i - %s : %s" % (index, interface, name))

def get_default_input():
    port = None
    for i, _, name, xi, _, _ in iterate_endpoints():
        if xi == 1 and re.fullmatch(DEFAULT_MIDI_IN_RX, name) is not None:
            port = i
            break
    return port


def get_default_output():
    port = None
    for i, _, name, _, xo, _ in iterate_endpoints():
        if xo == 1 and re.match(DEFAULT_MIDI_OUT_RX, name) is not None:
            port = i
            break
    return port


class LogLevels(Enum):
    DEBUG = 5
    NORMAL = 3
    ERRORS = 1


parser = OptionParser()


group = OptionGroup(parser, "MIDI Input-Output Selection", 
        "Select MIDI Input and Output ports for the virtual surface. "
        "By default the ports are scanned by name and ports with names "
        "matching %s and %s are selected. Use the -l option to list ports "
        "by their IDs if you need to override this." 
        % (DEFAULT_MIDI_IN_RX, DEFAULT_MIDI_OUT_RX))

group.add_option("-l", "--list", dest="list_endpoints", action="store_true", 
        help="List MIDI endpoints")

group.add_option("-i", "--input-id", dest="input_id",
        default=get_default_input(),
        help="Select input by PyGame MIDI ID (Default=%default)")
group.add_option("-o", "--output-id", dest="output_id",
        default=get_default_output(),
        help="Select output by PyGame MIDI ID (Default=%default)")

parser.add_option_group(group)

parser.add_option("-p", dest="print_pings", action='store_true', 
        help="Report ping responses", 
        default=False)


class LoggerSurface():
    def __init__(self, midi_input, midi_output, print_ping):
        self.midi_in = midi_input
        self.midi_out = midi_output
        self.parser = mido.Parser()
        self.since_last_ping = now()
        self.ping_timeout = 2.0
        self.led_zone = None
        self.fader_state = [[None,None]] * 8
        self.print_ping = print_ping

    def _update_fader_state(self, order: str, fader_id: int, value: int):
        if order == 'hi':
            self.fader_state[fader_id][0] = value & 0x7f
        elif order == 'lo':
            self.fader_state[fader_id][1] = value & 0x7f

        for e in range(len(self.fader_state)):
            if self.fader_state[e][0] and self.fader_state[e][1]:
                position = (self.fader_state[e][0] << 7) ^ (self.fader_state[e][1])
                log_out("Fader 0x%x set to new position 0x%x" % (e, position))
                self.fader_state[e] = [None, None]

    def _handle_control_change_message(self, message):
        if message.control == 0x0c:
            self.led_zone = message.value
        elif message.control == 0x2c:
            zoneport = ZonePort.from_zone_port(self.led_zone, message.value & 0x0f)
            if zoneport is None:
                log_out("Unrecognized zone 0x%x port 0x%x" % (self.led_zone, message.value & 0x0f))
            elif message.value & 0xf0 == 0x40:
                log_out("LED %s new state ON" % (zoneport, ))
            elif message.value & 0xf0 == 0x00:
                log_out("LED %s new state OFF" % (zoneport, ))
            else:
                log_out("Unregonzied control change message: %s" % message)
        elif message.control & 0xf0 == 0x10:
            vpot_ident = VPotIdent(message.control & 0x0f)
            vpot_value = VPotRingAspect(message.value)
            log_out("VPot %s %s " % 
                    (vpot_ident , vpot_value.led_string()))
        elif message.control & 0x0f < 0x08:
            fader_id = message.control & 0x0F
            if message.control & 0xf0 == 0x00:
                self._update_fader_state('hi', fader_id, message.value)
            elif message.control & 0xf0 == 0x20:
                self._update_fader_state('lo', fader_id, message.value)
            else:
                log_out(message)

        else: 
            log_out(message)


    def _handle_sysex(self, message):
        if message.data[0:5] != (0x00, 0x00, 0x66, 0x05, 0x00):
            print(message.data[0:5])
            log_out("Non-HUI Sysex message: %s" % message)        
        elif message.data[5] == 0x10:
            text = SmallDisplayCharSet.decode(message.data[7:])
            log_out("Small display update Zone 0x%x \"%s\"" % (message.data[6], text))
        elif message.data[5] == 0x11:
            log_out("Timecode update")
        elif message.data[5] == 0x12:
            text = LargeDisplayCharSet.decode(message.data[7:])
            log_out("Large display update Zone 0x%x \"%s\"" % (message.data[6], text))
        else:
            log_out("Unrecognized HUI sysex: %s" % message)


    def _handle_vu(self, message):
        channel = message.channel & 0xf0
        side = (message.value & 0xf0) >> 8
        value = message.value & 0x0f
        log_out("VU Meter update, zone 0x%x side 0x%x value 0x%x" % (channel, side, value))

    def run(self) -> bool:
        if now() - self.since_last_ping > self.ping_timeout:
            log_out("Host ping not received within timeout (%f secs). Going OFFLINE." % (self.ping_timeout))
            return False

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
                    if self.print_ping:
                        log_out("Responding to host ping")
                    self.since_last_ping = now()
                    self.midi_out.write_short(0x90, 0x00, 0x7f)
                else:
                    log_out(message)

            elif message.is_cc():
                self._handle_control_change_message(message)
 
            elif message.type == 'sysex':
                self._handle_sysex(message)

            elif message.type == 'polytouch':
                self._handle_vu(message)
            else:
                log_out(message)

        return True

if __name__ == '__main__':

    (options, args) = parser.parse_args()
    
    if options.list_endpoints:
        list_endpoints()
        exit(0)

    if options.input_id is None:
        log_out("FATAL: MIDI Input port not selected")
        exit(-1)

    if options.output_id is None:
        log_out("FATAL: MIDI Output port not selected")
        exit(-1)

    log_out("Beginning run %s" % strftime("%a, %d %b %Y %H:%M:%S"))

    log_out("Creating MIDI connections...")
    log_out("MIDI input:")
    print_endpoint(options.input_id)
    log_out("MIDI Out:")
    print_endpoint(options.output_id)
    
    midi_in = pygame.midi.Input(options.input_id)
    midi_out = pygame.midi.Output(options.output_id)
    
    surface = LoggerSurface(midi_input=midi_in, midi_output=midi_out, 
            print_ping= options.print_pings)
    
    log_out("Sending system reset '0xFF'")
    midi_out.write([ [[0xff], pygame.midi.time()] ] )
    
    sleep_factor = 0.05

    log_out("Establishing run loop. Sleep factor %f." % (sleep_factor))
    while surface.run():
        sleep(sleep_factor)

    log_out("Exiting...")
    midi_in.close()
    midi_out.close()




