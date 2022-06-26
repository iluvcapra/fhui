import pygame.midi
# from fhui.surface import Surface

import mido

from optparse import OptionParser, OptionGroup
import sys
import re
from time import sleep

import codecs

DEFAULT_MIDI_IN_RX=r'^.*HUI In$'
DEFAULT_MIDI_OUT_RX=r'^.*HUI Out$'


if not pygame.midi.get_init():
    pygame.midi.init()


def iterate_endpoints():
    for i in range(pygame.midi.get_count()):
        f, n, xi, xo, op = pygame.midi.get_device_info(i)
        yield (i, codecs.decode(f, 'utf8'), codecs.decode(n, 'utf8'), xi, xo, op)

def list_endpoints():
    print("Inputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_input == 1:
            print("%i - %s : %s" % (index, interface, name))

    print("")
    print("Outputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_output == 1:
            print("%i - %s : %s" % (index, interface, name))

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


class LoggerSurface():
    def __init__(self, midi_input, midi_output):
        self.midi_in = midi_input
        self.midi_out = midi_output
        self.parser = mido.Parser() 

    def run(self):

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
                    print("responding to ping")
                    self.midi_out.write_short(0x90, 0x00, 0x7f)
                else:
                    print(message)

            elif message.type == 'control_change':
                if message.control == 0x0c:
                    print("Zone Select %x" % message.value)
                elif message.control == 0x2c:
                    if message.value & 0xf0 == 0x40:
                        print("Port %x new state ON" % (message.value & 0x0f))
                    elif message.value & 0xf0 == 0x00:
                        print("Port %x new state OFF" % (message.value & 0x0f))
                else:
                    print(message)
 
            else:
                print(message)




if __name__ == '__main__':

    (options, args) = parser.parse_args()
    
    if options.list_endpoints:
        list_endpoints()
        exit(0)

    if options.input_id is None:
        print("FATAL: MIDI Input port not selected")
        exit(-1)

    if options.output_id is None:
        print("FATAL: MIDI Output port not selected")
        exit(-1)

    midi_in = pygame.midi.Input(options.input_id)
    midi_out = pygame.midi.Output(options.output_id)
    surface = LoggerSurface(midi_input=midi_in, midi_output=midi_out)
    
    midi_out.write([ [[0xff, 0xff, 0xff], pygame.midi.time()] ] )
    
    while True:
        surface.run()
        sleep(0.05)





