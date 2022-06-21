import pygame.midi
from fhui.surface import Surface

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


class LoggerSurface(Surface):
    pass


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

    midi_in = pygame.midi.Input(options.input_id, 512)
    
    midi_out = pygame.midi.Output(options.output_id, 512)

    surface = LoggerSurface(midi_input=midi_in, midi_output=midi_out)

    while True:
        surface.run()
        sleep(0.1)





