# XFMIDO

XFMIDO is a Python library for processing XF (eXtended Format) MIDI data.
This library is Based on the [mido](https://github.com/mido/mido) library.

#### English | [日本語](https://github.com/jiroshimaya/xfmido/blob/main/README.ja.md)

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

## Background
The XF format is an extension of the standard MIDI file format developed by Yamaha Corporation and is widely used in Japan. Most MIDI files available for purchase on Yamaha's website conform to this specification. Detailed specifications of the XF format can be found at the following link: https://jp.yamaha.com/files/download/other_assets/7/321757/xfspc.pdf

Since mido does not read the dedicated chunks of the XF specification, if lyrics information, etc., is written there, it cannot be retrieved. If it can be retrieved, it is expected to be convenient for the development of various applications, as lyrics, timing, and melody can be obtained. Therefore, I wanted to extend mido to read chunks with XF-specific XFIH and XFKM headers.


# For Developers

- This project uses [uv](https://github.com/astral-sh/uv) for package management.
- This project uses [taskipy](https://github.com/taskipy/taskipy) for command management.

```
uv run task test
uv run task lint
uv run task format
```
