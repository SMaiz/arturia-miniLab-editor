This repo contains a GUI to edit Arturia's MiniLab mkII
It is in very early stage, and needs a lot more polish, but it works
You'll need python bindings for Gtk4, libadwaita and rtmidi

For now, the device is hard-coded to port 1 in the function connectToDevice, so change this if you need to.
Use
```
from rtmidi.midiutil import list_input_ports, list_output_ports
list_input_ports()
list_output_ports()
```
to get the correct port numbers. If I find some time I might add a popup to select the device from a list.

The code is far from perfect, I wrote this in a week-end and it started as a simple script, so it might need a big refactor (it whould be better to use classes to define a lot of elements). It's also my first Python project, so I might have done a lot of things incorrectly.
Obviously, it's open-source so if you want to use it you can, and if you fix some bug I would love to have a MR.
