# Mackie HUI Emulation for Pro Tools

These are some experiments I did while trying to create a "virtual" or 
programmtic Mackie HUI surface, to allow external scriptable control of
Pro Tools from Python or another scripting interface.

I'm stuck on it at the moment because several of the buttons on the HUI
I was looking at emulating don't appear to be supported, though it's possible
the engineering document I have is out-of-date (and I don't have a HUI to 
debug the protocol). I may come back to it in the future if I have an epiphany
or I can get ahold of more up-to-date information on the HUI/Pro Tools 
protocol.

In the [examples](examples) folder there are two scripts which mostly work: the
[logger_surface.py](examples/logger_surface.py) script creates a synthetic HUI
surface which reads all of the messages from Pro Tools, parses them and prints
them to the screen. 

The [monitor.py](examples/monitor.py) script creates a software HUI and allows
you to read data from Pro Tools and send commands to it.
