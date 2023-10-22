#!/usr/bin/env python

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio
import rtmidi
import time

buttons = {
	1: {
		"type": "knob",
		"position": 2,
		"index": 1,
	},
	2: {
		"type": "knob",
		"position": 3,
		"index": 2,
	},
	3: {
		"type": "knob",
		"position": 10,
		"index": 3,
	},
	4: {
		"type": "knob",
		"position": 11,
		"index": 4,
	},
	5: {
		"type": "knob",
		"position": 13,
		"index": 5,
	},
	6: {
		"type": "knob",
		"position": 14,
		"index": 6,
	},
	7: {
		"type": "knob",
		"position": 15,
		"index": 7,
	},
	8: {
		"type": "knob",
		"position": 16,
		"index": 8,
	},
	9: {
		"type": "knob",
		"position": 4,
		"index": 9,
	},
	10: {
		"type": "knob",
		"position": 12,
		"index": 10,
	},
	11: {
		"type": "knob",
		"position": 5,
		"index": 11,
	},
	12: {
		"type": "knob",
		"position": 6,
		"index": 12,
	},
	13: {
		"type": "knob",
		"position": 7,
		"index": 13,
	},
	14: {
		"type": "knob",
		"position": 8,
		"index": 14,
	},
	48: {
		"type": "knob",
		"position": 1,
		"index": 48,
		"shift": 50,
		"linked": 49,
	},
	49: {
		"type": "switch",
		"position": 1,
		"index": 49,
	},
	50: {
		"type": "knob",
		"position": 1,
		"index": 50,
	},
	51: {
		"type": "knob",
		"position": 9,
		"index": 51,
		"shift": 53,
		"linked": 52,
	},
	52: {
		"type": "switch",
		"position": 9,
		"index": 52,
	},
	53: {
		"type": "knob",
		"position": 9,
		"index": 53,
	},
	64: {
		"type": "mod",
		"position": 0,
		"index": 64,
	},
	65: {
		"type": "bend",
		"position": 0,
		"index": 65,
	},
	80: {
		"type": "switch",
		"position": 0,
		"index": 80,
	},
	112: {
		"type": "pad",
		"position": 1,
		"index": 112,
		"shift": 120,
	},
	113: {
		"type": "pad",
		"position": 2,
		"index": 113,
		"shift": 121,
	},
	114: {
		"type": "pad",
		"position": 3,
		"index": 114,
		"shift": 122,
	},
	115: {
		"type": "pad",
		"position": 4,
		"index": 115,
		"shift": 123,
	},
	116: {
		"type": "pad",
		"position": 5,
		"index": 116,
		"shift": 124,
	},
	117: {
		"type": "pad",
		"position": 6,
		"index": 117,
		"shift": 125,
	},
	118: {
		"type": "pad",
		"position": 7,
		"index": 118,
		"shift": 126,
	},
	119: {
		"type": "pad",
		"position": 8,
		"index": 119,
		"shift": 127,
	},
	120: {
		"type": "pad",
		"position": 9,
		"index": 120,
	},
	121: {
		"type": "pad",
		"position": 10,
		"index": 121,
	},
	122: {
		"type": "pad",
		"position": 11,
		"index": 122,
	},
	123: {
		"type": "pad",
		"position": 12,
		"index": 123,
	},
	124: {
		"type": "pad",
		"position": 13,
		"index": 124,
	},
	125: {
		"type": "pad",
		"position": 14,
		"index": 125,
	},
	126: {
		"type": "pad",
		"position": 15,
		"index": 126,
	},
	127: {
		"type": "pad",
		"position": 16,
		"index": 127,
	},
}

buttonsMap = [
		[ 80,  0,  48,   1,   2,   9,  11,  12,  13,  14, ],
		[ 65, 64,  51,   3,   4,  10,   5,   6,   7,   8, ],
		[  0,  0, 112, 113, 114, 115, 116, 117, 118, 119, ],
]
colors = [
	"No Color",
	"Red",
	"Blue",
	"Green",
	"Purple",
	"Cyan",
	"Yellow",
	"White",
]
knobModes = [
	"Control",
	"NRPN/RPN",
]
padModes = [
	"MMC",
	"Switched Control",
	"MIDI Note",
	"Patch Change",
]
bendModes = [
	"Pitch Bend",
]
switchModes = [
	"Off",
	"Switched Control",
	"MIDI Note",
]
channels = [
	"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
	"Keyboard",
]
controlOptions = [
	"Absolute",
	"Relative #1",
	"Relative #2",
	"Relative #3",
]
ccNumbers = []
for n in range(127):
	ccNumbers.append(str(n))
nrpnOptions = [
	"NRPN",
	"RPN",
]
nrpnNumbers = [
	"1:128 (coarse)",
	"1:64",
	"1:32",
	"1:16",
	"1:8",
	"1:4",
	"1:2",
	"1:1 (fine)",
]
noteOptions = [
	"Toggle",
	"Gate",
]
rawNotes = [
	"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
]
rawHeights = [
	"-2", "-1", "0", "1", "2", "3", "4", "5", "6", "7", "8"
]
notes = []
for h in rawHeights:
	for n in rawNotes:
		notes.append(n + h)
mmcCommands = [
	"Stop",
	"Play",
	"Deferred Play",
	"Fast Forward",
	"Rewind",
	"Record Strobe",
	"Record Exit",
	"Record Ready",
	"Pause",
	"Eject",
	"Chase",
	"inLine Reset",
]
pitchBendOptions = [
	"Standard",
	"Hold",
]

header = [ 0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42 ]

connected = False
sync = False
midiout = None
midiin = None
deviceButtonBox = None
connectButton = None
disconnectButton = None
portsList = None
memorySelect = None

def openPort(midi, portname):
	for portno, name in enumerate(midi.get_ports()):
		if portname == name:
			midi.open_port(portno, portname)
			return True
	print("Port {} was not found".format(portname))
	return False

def connectToDevice(b):
	global connected, midiout, midiin
	print("connectToDevice")
	if connected:
		connected = False
		deviceButtonBox.set_sensitive(False)
		connectButton.set_visible(True)
		disconnectButton.set_visible(False)
		midiin.close_port()
		midiin = None
		midiout.close_port()
		midiout = None
	else:
		portname = portsList.get_selected_row().get_child().get_label()
		print(portname)
		if not openPort(midiout, portname) or not openPort(midiin, portname):
			print("Error opening port {}".format(portname))
			return

		print("Port {} opened".format(portname))
		midiin.ignore_types(sysex=False)
		midiin.set_callback(gotPacket)
		connected = True
		deviceButtonBox.set_sensitive(True)
		connectButton.set_visible(False)
		disconnectButton.set_visible(True)

setCurrentMemoryMessage = [ 0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42, 0x05, 0x00, 0xF7 ]

def setCurrentMemory(write=False):
	tmp, memory = memorySelect.get_selected_item().get_string().split()
	print("Setting current memory to {}".format(memory))
	setCurrentMemoryMessage[6] = 6 if write else 5
	setCurrentMemoryMessage[7] = int(memory)
	midiout.send_message(setCurrentMemoryMessage)

def getFromDevice(x):
	print("getFromDevice")
	setCurrentMemory()
	for bi in buttons:
		b = buttons[bi]
		for i in range(6):
			midiout.send_message(bytearray.fromhex("F0 00 20 6B 7F 42 01 00 {:02X} {:02X} F7".format(i + 1, b["index"])))
			time.sleep(0.001)
		if b["type"] == "pad":
			midiout.send_message(bytearray.fromhex("F0 00 20 6B 7F 42 01 00 11 {:02X} F7".format(b["index"])))
			time.sleep(0.001)

def gotPacket(e, data=None):
	d, timestamp = e
	for i in range(len(header)):
		if d[i] != header[i]:
			print("Incorrect packet header")
			return
	if d[-1] != 0xF7:
		print("Incorrect packet footer")
		return
	if d[6] != 0x02:
		print("Incorrect packet command {}".format(d[6]))
		return
	if d[7] != 0:
		print("Incorrect packet value at index 7: {}".format(d[7]))
		return
	prop = d[8]
	button = d[9]
	value = d[10]
	buttons[button][prop] = value

def sendMidiSetValue(control, param, value):
	midiout.send_message(bytearray.fromhex("F0 00 20 6B 7F 42 02 00 {:02X} {:02X} {:02X} F7".format(param, control, value)))

def saveToDevice(x):
	print("saveToDevice")
	if not sync:
		# We need to send everything
		for bi in buttons:
			b = buttons[bi]
			for i in range(6):
				sendMidiSetValue(b["index"], i + 1, b[i + 1])
				time.sleep(0.001)
			if b["type"] == "pad":
				sendMidiSetValue(b["index"], Properties.Color, b[Properties.Color])
				time.sleep(0.001)
	setCurrentMemory(True)

def updateSync(b):
	global sync
	sync = b.get_active()

def readFromFile(b):
	dialog = Gtk.FileDialog()
	dialog.open(callback=readFromFileCallback)

def readFromFileCallback(dialog, res):
	result = dialog.open_finish(res)
	print("Reading file {}".format(result.get_path()))
	with open(result.get_path(), "r") as f:
		lines = f.readlines()

		for line in lines:
			line = line.replace("\n", "")
			if line == "{" or line == "" or line == "}" or line == "	\"device\": \"MiniLab mkII\",":
				continue
			tmp, value = line.replace('"','').replace(',','').replace(':','').split()
			button, prop = tmp.split('_');
			button = int(button)
			prop = int(prop)
			value = int(value)
			buttons[button][prop] = value

def saveToFile(b):
	dialog = Gtk.FileDialog()
	dialog.save(callback=saveToFileCallback)

def saveToFileCallback(dialog, res):
	result = dialog.save_finish(res)
	print("Writing to file {}".format(result.get_path()))
	with open(result.get_path(), "w") as f:
		f.write("{\n\t\"device\": \"MiniLab mkII\",\n")
		for bi in buttons:
			b = buttons[bi]
			initFields(b) # We need to ensure every field has a value
			for i in range(6):
				f.write("\t\"{}_{}\": {},\n".format(b["index"], i + 1, b[i + 1]))
			if b["type"] == "pad":
				f.write("\t\"{}_17\": {},\n".format(b["index"], b[Properties.Color]))
		f.write("\n}\n")
class Modes:
	Off = 0
	Control = 1
	NrpnRpn = 4
	Mmc = 7
	SwitchedControl = 8
	MidiNote = 9
	PatchChange = 11
	PitchBend = 16

def modeValueToString(mode):
	match mode:
		case Modes.Off:
			return "Off"
		case Modes.Control:
			return "Control"
		case Modes.NrpnRpn:
			return "NRPN/RPN"
		case Modes.Mmc:
			return "MMC"
		case Modes.SwitchedControl:
			return "Switched Control"
		case Modes.MidiNote:
			return "MIDI Note"
		case Modes.PatchChange:
			return "Patch Change"
		case Modes.PitchBend:
			return "Pitch Bend"
		case _:
			print("modeValueToString: Unknown mode {}".format(mode))
			return "Off"

def modeStringToValue(mode):
	match mode:
		case "Off":
			return Modes.Off
		case "Control":
			return Modes.Control
		case "NRPN/RPN":
			return Modes.NrpnRpn
		case "MMC":
			return Modes.Mmc
		case "Switched Control":
			return Modes.SwitchedControl
		case "MIDI Note":
			return Modes.MidiNote
		case "Patch Change":
			return Modes.PatchChange
		case "Pitch Bend":
			return Modes.PitchBend
		case _:
			print("modeStringToValue: Unknown mode {}".format(mode))
			return 0

def channelValueToString(channel):
	if channel == 65:
		return "Keyboard"
	if channel >= 0 and channel <= 16:
		return str(channel)
	print("channelValueToString: Unknown channel {}".format(channel))
	return "0"

def channelStringToValue(channel):
	if channel == "Keyboard":
		return 65
	c = int(channel)
	if c >= 0 and c <= 16:
		return c
	print("channelStringToValue: Unknown channel {}".format(channel))
	return 0

def checkNumber(number):
	if number >= 0 and number <= 127:
		return number
	print("checkNumber: Incorrect Number {}".format(ccNumber))
	return 0

class Colors:
	NoColor = 0
	Red = 1
	Green = 4
	Yellow = 5
	Blue = 16
	Purple = 17
	Cyan = 20
	White = 127

def colorValueToString(color):
	match color:
		case Colors.NoColor:
			return "No Color"
		case Colors.Red:
			return "Red"
		case Colors.Green:
			return "Green"
		case Colors.Yellow:
			return "Yellow"
		case Colors.Blue:
			return "Blue"
		case Colors.Purple:
			return "Purple"
		case Colors.Cyan:
			return "Cyan"
		case Colors.White:
			return "White"
		case _:
			print("colorValueToString: Unknown color {}".format(color))
			return "No Color"

def colorStringToValue(color):
	match color:
		case "No Color":
			return Colors.NoColor
		case "Red":
			return Colors.Red
		case "Green":
			return Colors.Green
		case "Yellow":
			return Colors.Yellow
		case "Blue":
			return Colors.Blue
		case "Purple":
			return Colors.Purple
		case "Cyan":
			return Colors.Cyan
		case "White":
			return Colors.White
		case _:
			print("colorStringToValue: Unknown color {}".format(color))
			return 0

def noteValueToString(note):
	if note >= 0 and note < len(notes):
		return notes[note]
	print("noteValueToString: Unknown note {}".format(note))
	return 64

def noteStringToValue(note):
	for i in range(len(notes)):
		if note == notes[i]:
			return i
	print("noteStringToValue: Unknown note {}".format(note))
	return "C2"

class NoteOptions:
	Toggle = 0
	Gate = 1

def noteOptionValueToString(option):
	match option:
		case NoteOptions.Toggle:
			return "Toggle"
		case NoteOptions.Gate:
			return "Gate"
	print("noteOptionValueToString: Unknown noteOption {}".format(option))
	return "Gate"

def noteOptionStringToValue(option):
	match option:
		case "Toggle":
			return NoteOptions.Toggle
		case "Gate":
			return NoteOptions.Gate
	print("noteOptionValueToString: Unknown noteOption {}".format(option))
	return NoteOptions.Gate

class ControlOptions:
	Absolute = 0
	Relative1 = 1
	Relative2 = 2
	Relative3 = 3

def controlOptionValueToString(option):
	match option:
		case ControlOptions.Absolute:
			return "Absolute"
		case ControlOptions.Relative1:
			return "Relative #1"
		case ControlOptions.Relative2:
			return "Relative #2"
		case ControlOptions.Relative3:
			return "Relative #3"
		case _:
			print("controlOptionValueToString: Unknown noteOption {}".format(option))
			return "Absolute"

def controlOptionStringToValue(option):
	match option:
		case "Absolute":
			return ControlOptions.Absolute
		case "Relative #1":
			return ControlOptions.Relative1
		case "Relative #2":
			return ControlOptions.Relative2
		case "Relative #3":
			return ControlOptions.Relative3
		case _:
			print("controlOptionStringToValue: Unknown noteOption {}".format(option))
			return ControlOptions.Absolute

class NrpnOptions:
	Nrpn = 0
	Rpn = 1

def nrpnRpnOptionValueToString(option):
	match option:
		case NrpnOptions.Nrpn:
			return "NRPN"
		case NrpnOptions.Rpn:
			return "RPN"
		case _:
			print("nrpnRpnOptionValueToString: Unknown noteOption {}".format(option))
			return "NRPN"

def nrpnRpnOptionStringToValue(option):
	match option:
		case "NRPN":
			return NrpnOptions.Nrpn
		case "RPN":
			return NrpnOptions.Rpn
		case _:
			print("nrpnRpnOptionStringToValue: Unknown noteOption {}".format(option))
			return NrpnOptions.Nrpn

class MmcOptions:
	Stop = 0
	Play = 1
	DeferredPlay = 2
	FastForward = 3
	Rewind = 4
	RecordStrobe = 5
	RecordExit = 6
	RecordReady = 7
	Pause = 8
	Eject = 9
	Chase = 10
	InLineReset = 11

def mmcValueToString(option):
	match option:
		case MmcOptions.Stop:
			return "Stop"
		case MmcOptions.Play:
			return "Play"
		case MmcOptions.DeferredPlay:
			return "Deferred Play"
		case MmcOptions.FastForward:
			return "Fast Forward"
		case MmcOptions.Rewind:
			return "Rewind"
		case MmcOptions.RecordStrobe:
			return "Record Strobe"
		case MmcOptions.RecordExit:
			return "Record Exit"
		case MmcOptions.RecordReady:
			return "Record Ready"
		case MmcOptions.Pause:
			return "Pause"
		case MmcOptions.Eject:
			return "Eject"
		case MmcOptions.Chase:
			return "Chase"
		case MmcOptions.InLineReset:
			return "inLine Reset"
		case _:
			print("mmcValueToString: Unknown MMC option {}".format(option))
			return "Stop"

def mmcStringToValue(option):
	match option:
		case "Stop":
			return MmcOptions.Stop
		case "Play":
			return MmcOptions.Play
		case "Deferred Play":
			return MmcOptions.DeferredPlay
		case "Fast Forward":
			return MmcOptions.FastForward
		case "Rewind":
			return MmcOptions.Rewind
		case "Record Strobe":
			return MmcOptions.RecordStrobe
		case "Record Exit":
			return MmcOptions.RecordExit
		case "Record Ready":
			return MmcOptions.RecordReady
		case "Pause":
			return MmcOptions.Pause
		case "Eject":
			return MmcOptions.Eject
		case "Chase":
			return MmcOptions.Chase
		case "inLine Reset":
			return MmcOptions.InLineReset
		case _:
			print("mmcStringToValue: Unknown MMC option {}".format(option))
			return MmcOptions.Stop

class PitchBendOptions:
	Standard = 0
	Hold = 1

def pitchBendOptionValueToString(option):
	match option:
		case PitchBendOptions.Standard:
			return "Standard"
		case PitchBendOptions.Hold:
			return "Hold"
		case _:
			print("pitchBendOptionValueToString: Unknown Pitch Bend option {}".format(option))
			return "Standard"

def pitchBendOptionStringToValue(option):
	match option:
		case "Standard":
			return PitchBendOptions.Standard
		case "Hold":
			return PitchBendOptions.Hold
		case _:
			print("pitchBendOptionStringToValue: Unknown Pitch Bend option {}".format(option))
			return PitchBendOptions.Standard

def optionStringToValue(option, mode):
	match mode:
		case Modes.Off:
			return 0 # No options when Off
		case Modes.Control:
			return controlOptionStringToValue(option)
		case Modes.NrpnRpn:
			return nrpnRpnOptionStringToValue(option)
		case Modes.Mmc:
			return mmcStringToValue(option)
		case Modes.SwitchedControl:
			return noteOptionStringToValue(option)
		case Modes.MidiNote:
			return noteOptionStringToValue(option)
		case Modes.PatchChange:
			print("I'm too lazy")
			return 0
		case Modes.PitchBend:
			return pitchBendOptionStringToValue(option)
		case _:
			print("Unknown mode {}".format(mode))
			return 0

class Properties:
	Mode = 1
	Channel = 2
	CcNumber = 3
	Min = 4
	Max = 5
	Option = 6
	Color = 17

def on_activate(app):
	global deviceButtonBox, connectButton, disconnectButton, portsList, memorySelect
	win = Gtk.ApplicationWindow(application=app)
	nb = Gtk.Notebook()
	btnGrid = Gtk.Grid()

	i = 0
	for row in buttonsMap:
		j = 0
		for cell in row:
			if cell == 0:
				j += 1
				continue
			k = buttons[cell]
			label = str(k["position"])
			if k["type"] == "switch":
				label = "Ped"
			elif k["type"] == "mod":
				label = "Mod"
			elif k["type"] == "bend":
				label = "Bend"
			btn = Gtk.Button(label=label)
			btn.connect('clicked', lambda x, k=k: btnClicked(k, nb))
			height = 1
			if k["type"] == "mod" or k["type"] == "bend":
				height = 2
			btnGrid.attach(btn, j, i, 1, height)
			j += 1
		i += 1

	box = Gtk.Box()
	box.set_orientation(Gtk.Orientation.VERTICAL)
	box.append(btnGrid)
	box.append(nb)
	mainBox = Gtk.Box()
	sideBox = Gtk.Box()
	sideBox.set_orientation(Gtk.Orientation.VERTICAL)
	readFromFileBtn = Gtk.Button(label="Read from file")
	readFromFileBtn.connect('clicked', readFromFile)
	sideBox.append(readFromFileBtn)
	saveToFileBtn = Gtk.Button(label="Save to file")
	saveToFileBtn.connect('clicked', saveToFile)
	sideBox.append(saveToFileBtn)

	connectPopover = Gtk.Popover()
	popoverBox = Gtk.Box()
	connectPopover.set_child(popoverBox)
	connectPopover.set_autohide(True)
	popoverBox.set_orientation(Gtk.Orientation.VERTICAL)
	portsList = Gtk.ListBox()
	for port in midiout.get_ports():
		portsList.append(Gtk.Label(label=port))
	popoverBox.append(portsList)
	realConnectButton = Gtk.Button(label="Connect")
	realConnectButton.connect('clicked', connectToDevice)
	popoverBox.append(realConnectButton)
	connectButton = Gtk.MenuButton(label="Connect to device", popover=connectPopover)
	sideBox.append(connectButton)
	disconnectButton = Gtk.Button(label="Disconnect")
	disconnectButton.connect('clicked', connectToDevice)
	disconnectButton.set_visible(False)
	sideBox.append(disconnectButton)

	deviceButtonBox = Gtk.Box()
	deviceButtonBox.set_orientation(Gtk.Orientation.VERTICAL)
	deviceButtonBox.set_sensitive(False)
	sideBox.append(deviceButtonBox)
	syncDeviceBtn = Gtk.CheckButton(label="Sync with device")
	syncDeviceBtn.connect('toggled', updateSync)
	deviceButtonBox.append(syncDeviceBtn)
	
	memoryLegend = Gtk.Label(label="Memory")
	deviceButtonBox.append(memoryLegend)
	model = Gtk.StringList()
	for i in range(8):
		model.append("memory {}".format(i + 1))
	memorySelect = Gtk.DropDown(model=model)
	deviceButtonBox.append(memorySelect)
	readWriteBox = Gtk.Box()
	getFromDeviceBtn = Gtk.Button(label="Read")
	getFromDeviceBtn.connect('clicked', getFromDevice)
	readWriteBox.append(getFromDeviceBtn)
	saveToDeviceBtn = Gtk.Button(label="Write")
	saveToDeviceBtn.connect('clicked', saveToDevice)
	readWriteBox.append(saveToDeviceBtn)
	deviceButtonBox.append(readWriteBox)

	mainBox.append(sideBox)
	mainBox.append(box)
	win.set_child(mainBox)
	win.present()

def initFields(k):
	if not Properties.Mode in k:
		k[Properties.Mode] = Modes.Off
	if not Properties.Channel in k:
		k[Properties.Channel] = 1
	if not Properties.CcNumber in k:
		k[Properties.CcNumber] = 0
	if not Properties.Option in k:
		k[Properties.Option] = 0
	if not Properties.Min in k:
		k[Properties.Min] = 0
	if not Properties.Max in k:
		k[Properties.Max] = 127
	if k["type"] == "pad":
		if not Properties.Color in k:
			k[Properties.Color] = Colors.NoColor

def btnClicked(k, nb):
	while nb.get_pages().get_n_items() > 0:
		nb.remove_page(nb.get_pages().get_n_items() - 1)
	page = Gtk.FlowBox()
	page.set_orientation(Gtk.Orientation.VERTICAL)
	page.set_min_children_per_line(3)
	page.set_selection_mode(Gtk.SelectionMode.NONE)
	nb.append_page(page, Gtk.Label(label="{} {}".format(k["type"], k["index"])))
	initFields(k)
	draw(k, page)
	if "shift" in k:
		# There is an option for this key+shift, display it
		kk = buttons[k["shift"]]
		page = Gtk.FlowBox()
		page.set_orientation(Gtk.Orientation.VERTICAL)
		page.set_min_children_per_line(3)
		page.set_selection_mode(Gtk.SelectionMode.NONE)
		nb.append_page(page, Gtk.Label(label="{} {} + shift".format(kk["type"], kk["index"])))
		initFields(kk)
		draw(kk, page)
	if "linked" in k:
		# This key has an other one linked to it, display it
		kk = buttons[k["linked"]]
		page = Gtk.FlowBox()
		page.set_orientation(Gtk.Orientation.VERTICAL)
		page.set_min_children_per_line(3)
		page.set_selection_mode(Gtk.SelectionMode.NONE)
		nb.append_page(page, Gtk.Label(label="{} {}".format(kk["type"], kk["index"])))
		initFields(kk)
		draw(kk, page)

def modeSelected(dropDown, k, page):
	k[Properties.Mode] = modeStringToValue(dropDown.get_selected_item().get_string())
	draw(k, page)
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Mode, k[Properties.Mode])

def channelSelected(dropDown, k, page):
	k[Properties.Channel] = channelStringToValue(dropDown.get_selected_item().get_string())
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Channel, k[Properties.Channel])

def colorSelected(dropDown, k, page):
	k[Properties.Color] = colorStringToValue(dropDown.get_selected_item().get_string())
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Color, k[Properties.Color])

def optionSelected(dropDown, k, page):
	k[Properties.Option] = optionStringToValue(dropDown.get_selected_item().get_string(), k[Properties.Mode])
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Option, k[Properties.Option])

def ccNumberSelected(dropDown, k, page):
	k[Properties.CcNumber] = int(dropDown.get_selected_item().get_string())
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.CcNumber, k[Properties.CcNumber])

def minValueChanged(spinButton, k, page):
	k[Properties.Min] = spinButton.get_value()
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Min, k[Properties.Min])

def maxValueChanged(spinButton, k, page):
	k[Properties.Max] = spinButton.get_value()
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.Max, k[Properties.Mode])

def mmcSelected(dropDown, k, page):
	k[Properties.CcNumber] = mmcStringToValue(dropDown.get_selected_item().get_string())
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.CcNumber, k[Properties.CcNumber])

def noteSelected(dropDown, k, page):
	k[Properties.CcNumber] = noteStringToValue(dropDown.get_selected_item().get_string())
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.CcNumber, k[Properties.CcNumber])

def programChanged(spinButton, k, page):
	k[Properties.CcNumber] = spinButton.get_value()
	if sync and connected:
		sendMidiSetValue(k["index"], Properties.CcNumber, k[Properties.CcNumber])

def draw(k, page):
	page.remove_all()
	#Mode
	modeList = [ "Off" ]
	if k["type"] == "knob" or k["type"] == "mod":
		modeList += knobModes
	elif k["type"] == "pad":
		modeList += padModes
	elif k["type"] == "bend":
		modeList += bendModes
	elif k["type"] == "switch":
		modeList += switchModes
	else:
		print("ERROR, unknwn button type {}".format(k["type"]))
		return
	modeSelect = addBoxWithLabelAndOptions(page, "Mode", modeList)
	setMatchingOption(modeSelect, modeValueToString(k[Properties.Mode]))
	modeSelect.connect('notify::selected-item', lambda x, y: modeSelected(x, k, page))
	
	# color
	if k["type"] == "pad":
		colorSelect = addBoxWithLabelAndOptions(page, "Color", colors)
		colorSelect.connect('notify::selected-item', lambda x, y: colorSelected(x, k, page))
		setMatchingOption(colorSelect, colorValueToString(k[Properties.Color]))
	
	# channel
	channelSelect = addBoxWithLabelAndOptions(page, "Channel", channels)
	channelSelect.connect('notify::selected-item', lambda x, y: channelSelected(x, k, page))
	setMatchingOption(channelSelect, channelValueToString(k[Properties.Channel]))
	
	if k[Properties.Mode] == Modes.Off:
		return
	match k["type"]:
		case "knob":
			match k[Properties.Mode]:
				case Modes.Control:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", controlOptions)
					setMatchingOption(optionSelect, controlOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					ccSelect = addBoxWithLabelAndOptions(page, "CC Number", ccNumbers)
					setMatchingOption(ccSelect, str(k[Properties.CcNumber]))
					ccSelect.connect('notify::selected-item', lambda x, y: ccNumberSelected(x, k, page))
					minSpin = addSpinButton(page, "Min Value")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "Max Value")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
				case Modes.NrpnRpn:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", nrpnOptions)
					setMatchingOption(optionSelect, nrpnRpnOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					minSpin = addSpinButton(page, "RPN/NRPN LSB")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "RPN/NRPN MSB")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
					ccSelect = addBoxWithLabelAndOptions(page, "Data entry", nrpnNumbers)
					setMatchingOption(ccSelect, str(k[Properties.CcNumber]))
					ccSelect.connect('notify::selected-item', lambda x, y: ccNumberSelected(x, k, page))
		case "pad":
			match k[Properties.Mode]:
				case Modes.Mmc:
					mmcSelect = addBoxWithLabelAndOptions(page, "MMC", mmcCommands)
					setMatchingOption(mmcSelect, mmcValueToString(k[Properties.Option]))
					mmcSelect.connect('notify::selected-item', lambda x, y: mmcSelected(x, k, page))
				case Modes.SwitchedControl:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", noteOptions)
					setMatchingOption(optionSelect, noteOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					ccSelect = addBoxWithLabelAndOptions(page, "CC Number", ccNumbers)
					setMatchingOption(ccSelect, str(k[Properties.CcNumber]))
					ccSelect.connect('notify::selected-item', lambda x, y: ccNumberSelected(x, k, page))
					minSpin = addSpinButton(page, "Off Value")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "On Value")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
				case Modes.MidiNote:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", noteOptions)
					setMatchingOption(optionSelect, noteOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					noteSelect = addBoxWithLabelAndOptions(page, "Note", notes)
					setMatchingOption(noteSelect, noteValueToString(k[Properties.CcNumber]))
					noteSelect.connect('notify::selected-item', lambda x, y: noteSelected(x, k, page))
				case Modes.PatchChange:
					programSpin = addSpinButton(page, "Program Number")
					programSpin.set_value(k[Properties.CcNumber])
					programSpin.connect('notify::value', lambda x, y: programChanged(x, k, page))
					minSpin = addSpinButton(page, "Bank LSB")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "Bank MSB")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
		case "switch":
			match k[Properties.Mode]:
				case Modes.SwitchedControl:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", noteOptions)
					setMatchingOption(optionSelect, noteOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					ccSelect = addBoxWithLabelAndOptions(page, "CC Number", ccNumbers)
					setMatchingOption(ccSelect, str(k[Properties.CcNumber]))
					ccSelect.connect('notify::selected-item', lambda x, y: ccNumberSelected(x, k, page))
					minSpin = addSpinButton(page, "Off Value")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "On Value")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
				case Modes.MidiNote:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", noteOptions)
					setMatchingOption(optionSelect, noteOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					noteSelect = addBoxWithLabelAndOptions(page, "Note", notes)
					setMatchingOption(noteSelect, noteValueToString(k[Properties.CcNumber]))
					noteSelect.connect('notify::selected-item', lambda x, y: noteSelected(x, k, page))
		case "mod":
			match k[Properties.Mode]:
				case Modes.Control:
					# The modwheel in control mode doesn't have an option field
					ccSelect = addBoxWithLabelAndOptions(page, "CC Number", ccNumbers)
					setMatchingOption(ccSelect, str(k[Properties.CcNumber]))
					ccSelect.connect('notify::selected-item', lambda x, y: ccNumberSelected(x, k, page))
					minSpin = addSpinButton(page, "Min Value")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "Max Value")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
				case Modes.NrpnRpn:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", nrpnOptions)
					setMatchingOption(optionSelect, nrpnRpnOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))
					minSpin = addSpinButton(page, "RPN/NRPN LSB")
					minSpin.set_value(k[Properties.Min])
					minSpin.connect('notify::value', lambda x, y: minValueChanged(x, k, page))
					maxSpin = addSpinButton(page, "RPN/NRPN MSB")
					maxSpin.set_value(k[Properties.Max])
					maxSpin.connect('notify::value', lambda x, y: maxValueChanged(x, k, page))
					# The modwheel in control mode doesn't have a "data entry" field
		case "bend":
			if k[Properties.Mode] == Modes.PitchBend:
					optionSelect = addBoxWithLabelAndOptions(page, "Option", pitchBendOptions)
					setMatchingOption(optionSelect, pitchBendOptionValueToString(k[Properties.Option]))
					optionSelect.connect('notify::selected-item', lambda x, y: optionSelected(x, k, page))

def setMatchingOption(dropdown, value):
	i = 0
	for option in dropdown.get_model():
		if value == option.get_string():
			dropdown.set_selected(i)
		i += 1

def addBoxWithLabelAndOptions(widget, label, options):
	box = Gtk.Box()
	label = Gtk.Label(label=label)
	model = Gtk.StringList()
	for option in options:
		model.append(option)
	select = Gtk.DropDown(model=model)
	box.append(label)
	box.append(select)
	widget.append(box)
	return select

def addSpinButton(widget, label, minVal = 0, maxVal = 127):
	box = Gtk.Box()
	label = Gtk.Label(label=label)
	btn = Gtk.SpinButton(adjustment=Gtk.Adjustment(value=0, lower=minVal, upper=maxVal, step_increment=1))
	box.append(label)
	box.append(btn)
	widget.append(box)
	return btn

midiout = rtmidi.MidiOut(rtmidi.API_UNSPECIFIED)
midiin = rtmidi.MidiIn(rtmidi.API_UNSPECIFIED)
app = Adw.Application(application_id='fr.smaiz.miniLab2UI')
app.connect('activate', on_activate)
app.run(None)
