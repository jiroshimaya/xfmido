# XFMIDO

XFMIDO is a Python library for processing XF (eXtended Format) MIDI data.

## Features

- Reading XF-compliant headers (XFIH) and karaoke information (XFKM) chunks
- Can also read standard MIDI files (SMF)

## Usage

```
pip install xfmido
```


```python
from xfmido import XFMidiFile

# Load a sample MIDI file
xfmidifile = XFMidiFile("sample/sample.mid", charset="cp932")

# Display the information of the loaded MIDI file
print("MIDI file information:")
print(xfmidifile)

# Display XF-compliant header information
print("\nXF header information:")
print(xfmidifile.xfih)

# Display karaoke information
print("\nKaraoke information:")
print(xfmidifile.xfkm)
```

```
MIDI file information:
XFMidiFile(type=1, ticks_per_beat=480, tracks=[
  MidiTrack([
    Message('note_on', channel=0, note=60, velocity=100, time=0),
    Message('note_off', channel=0, note=60, velocity=64, time=480),
    MetaMessage('lyrics', text='Hello World', time=0),
    MetaMessage('end_of_track', time=0)])
])

XF header information:
MidiTrack([
  MetaMessage('text', text='XF Version 1', time=0),
  MetaMessage('end_of_track', time=0)])

Karaoke information:
MidiTrack([
  MetaMessage('cue_marker', text='$Lyrc:1:312:JP', time=0),
  MetaMessage('lyrics', text='Hello', time=0),
  MetaMessage('lyrics', text='World', time=480),
  MetaMessage('lyrics', text='Hello World', time=0),
  MetaMessage('end_of_track', time=0)])
```
