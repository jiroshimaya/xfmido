import pytest
import io
from mido import MidiFile
from xfmido.xfmido import XFMidiFile, extract_xf_karaoke_info

def create_mock_midi() -> io.BytesIO:
    # Create a mock MIDI file in bytes
    # MIDI Header Chunk: 'MThd' + header length (6) + format type (1) + number of tracks (1) + ticks per beat (480)
    header = b'MThd' + (6).to_bytes(4, byteorder='big') + (1).to_bytes(2, byteorder='big') \
                + (1).to_bytes(2, byteorder='big') + (480).to_bytes(2, byteorder='big')
    
    # MIDI Track Chunk: 'MTrk' + length + track data
    track_data = (
        b'\x00\x90\x3C\x64'  # Note On: delta time (0), status (0x90), note (60), velocity (100)
        b'\x83\x60\x80\x3C\x40'  # Note Off: delta time (480), status (0x80), note (60), velocity (64)
        b'\x00\xFF\x05\x0B\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'  # Lyric: delta time (0), status (0xFF), type (0x05), length (11), "Hello World"
        b'\x00\xFF\x2F\x00'  # End of Track: delta time (0), status (0xFF), type (0x2F), length (0)
    )
    track_length = len(track_data).to_bytes(4, byteorder='big')
    track = b'MTrk' + track_length + track_data
    
    # XFIH Chunk: 'XFIH' + length + XFIH data
    xfih_data = (
        b'\x00\xFF\x01\x0C\x58\x46\x20\x56\x65\x72\x73\x69\x6F\x6E\x20\x31'  # Text Event: delta time (0), status (0xFF), type (0x01), length (12), "XF Version 1"
        b'\x00\xFF\x2F\x00'  # End of Track: delta time (0), status (0xFF), type (0x2F), length (0)
    )
    xfih_length = len(xfih_data).to_bytes(4, byteorder='big')
    xfih = b'XFIH' + xfih_length + xfih_data
    
    # XFKM Chunk: 'XFKM' + length + XFKM data
    xfkm_data = (
        b'\x00\xFF\x07\x0E$Lyrc:1:312:JP'  # XF Karaoke info: delta time (0), status (0xFF), type (0x07), length (14), "$Lyrc:1:312:JP"
        b'\x00\xFF\x05\x05Hello'  # Lyric: delta time (0), status (0xFF), type (0x05), length (5), "Hello"
        b'\x83\x60\xFF\x05\x05World'  # Lyric: delta time (480), status (0xFF), type (0x05), length (5), "World"
        b'\x00\xFF\x05\x0B\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'  # Lyric: delta time (0), status (0xFF), type (0x05), length (11), "Hello World"
        b'\x00\xFF\x2F\x00'  # End of Track: delta time (0), status (0xFF), type (0x2F), length (0)
    )
    xfkm_length = len(xfkm_data).to_bytes(4, byteorder='big')
    xfkm = b'XFKM' + xfkm_length + xfkm_data
    # Combine header and track to form a complete MIDI file
    return io.BytesIO(header + track + xfih + xfkm)

def test_init_with_mock_midi():
    # Initialize XFMidiFile with the mocked file
    xfmidi = XFMidiFile(file=create_mock_midi(), charset="cp932")
    midi = MidiFile(file=create_mock_midi(), charset="cp932")
    
    # Assertions to verify correct initialization
    assert xfmidi.type == midi.type
    assert xfmidi.ticks_per_beat == midi.ticks_per_beat
    assert len(xfmidi.tracks) == len(midi.tracks)
    
    # Verify track contents
    for xf_track, midi_track in zip(xfmidi.tracks, midi.tracks):
        assert len(xf_track) == len(midi_track)
        
        for xf_msg, midi_msg in zip(xf_track, midi_track):
            assert xf_msg.type == midi_msg.type
            assert xf_msg.dict() == midi_msg.dict()

    # Check XF chunks
    assert xfmidi.xfih is not None
    assert xfmidi.xfkm is not None
    # Check XFIH chunk contents
    assert len(xfmidi.xfih) == 2  # XFIH should contain one message
    xfih_msg = xfmidi.xfih[0]
    assert xfih_msg.type == 'text'
    assert xfih_msg.text == 'XF Version 1'
    # Check end_of_track message
    xfih_end_of_track = xfmidi.xfih[1]
    assert xfih_end_of_track.type == 'end_of_track'
    assert xfih_end_of_track.time == 0
    # Check XFKM chunk contents
    assert len(xfmidi.xfkm) == 5  # XFKM should contain 4 messages

    # Check XF Karaoke info message
    xfkm_info = xfmidi.xfkm[0]
    assert xfkm_info.type == 'cue_marker'
    assert xfkm_info.text == '$Lyrc:1:312:JP'

    # Check lyric messages
    lyric1, lyric2, lyric3 = xfmidi.xfkm[1:4]
    
    assert lyric1.type == 'lyrics'
    assert lyric1.text == 'Hello'
    assert lyric1.time == 0

    assert lyric2.type == 'lyrics'
    assert lyric2.text == 'World'
    assert lyric2.time == 480

    assert lyric3.type == 'lyrics'
    assert lyric3.text == 'Hello World'
    assert lyric3.time == 0

    # Check end_of_track message
    xfkm_end_of_track = xfmidi.xfkm[4]
    assert xfkm_end_of_track.type == 'end_of_track'
    assert xfkm_end_of_track.time == 0

def test_init_with_mock_midi_and_filename():
    import os
    import uuid
    # Create a mock MIDI file and save it to a temporary file
    mock_midi = create_mock_midi()
    temp_midi_filename = f"temp_mock_midi_{uuid.uuid4().hex}.mid"
    with open(temp_midi_filename, "wb") as f:
        f.write(mock_midi.getbuffer())

    try:
        # Initialize XFMidiFile using the file name
        xfmidi_from_file = XFMidiFile(temp_midi_filename)

        # Initialize XFMidiFile using the file stream
        xfmidi_from_stream = XFMidiFile(file=mock_midi)

        # Check if both initializations result in the same data
        assert xfmidi_from_file.tracks == xfmidi_from_stream.tracks
        assert xfmidi_from_file.xfih == xfmidi_from_stream.xfih
        assert xfmidi_from_file.xfkm == xfmidi_from_stream.xfkm
    finally:
        # Delete the temporary file
        os.remove(temp_midi_filename)


def test_extract_xf_karaoke_info():
    info = extract_xf_karaoke_info(file=create_mock_midi())
    assert info['song_id'] == '$Lyrc'
    assert info['melody_channel'] == 1
    assert info['time_offset'] == 312
    assert info['language'] == 'JP'

def test_extract_xf_karaoke_info_with_filename():
    import os
    import uuid
    # Create a mock MIDI file and save it to a temporary file
    mock_midi = create_mock_midi()
    temp_midi_filename = f"temp_mock_midi_{uuid.uuid4().hex}.mid"
    with open(temp_midi_filename, "wb") as f:
        f.write(mock_midi.getbuffer())

    try:
        # Extract XF Karaoke info using the file name
        info_from_file = extract_xf_karaoke_info(temp_midi_filename)

        info_from_stream = extract_xf_karaoke_info(file=mock_midi)

        # Check if both results are the same
        assert info_from_file == info_from_stream
    finally:
        # Delete the temporary file
        os.remove(temp_midi_filename)
