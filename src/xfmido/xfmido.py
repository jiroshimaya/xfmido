from typing import Optional, Union, BinaryIO, Dict
from mido.midifiles.midifiles import (
    MidiTrack,
    MidiFile,
    read_chunk_header,
    read_variable_int,
    read_byte,
    read_meta_message,
    read_sysex,
    read_message,
    DebugFileWrapper,
    _dbg
)
from mido.midifiles.meta import meta_charset


def read_xf_track(infile, debug=False, clip=False):
    # This function is identical to read_track, except it expects XFIH or XFKM headers
    # instead of MTrk. The rest of the processing remains the same.
    track = MidiTrack()

    name, size = read_chunk_header(infile)

    #if name != b'MTrk':
    if name not in (b'XFIH', b'XFKM'):# ヘッダーの条件を書き換え
        #raise IOError('no MTrk header at start of track')
        raise IOError('no XF header at start of track')# メッセージを変更

    if debug:
        _dbg('-> size={}'.format(size))
        _dbg()

    start = infile.tell()
    last_status = None

    while True:
        # End of track reached.
        if infile.tell() - start == size:
            break

        if debug:
            _dbg('Message:')

        delta = read_variable_int(infile)

        if debug:
            _dbg('-> delta={}'.format(delta))

        status_byte = read_byte(infile)

        if status_byte < 0x80:
            if last_status is None:
                raise IOError('running status without last_status')
            peek_data = [status_byte]
            status_byte = last_status
        else:
            if status_byte != 0xff:
                # Meta messages don't set running status.
                last_status = status_byte
            peek_data = []

        if status_byte == 0xff:
            msg = read_meta_message(infile, delta)

        elif status_byte in [0xf0, 0xf7]:
            # TODO: I'm not quite clear on the difference between
            # f0 and f7 events.
            msg = read_sysex(infile, delta, clip)
        else:
            msg = read_message(infile, status_byte, peek_data, delta, clip)

        track.append(msg)

        if debug:
            _dbg('-> {!r}'.format(msg))
            _dbg()

    return track


def extract_xf_karaoke_info(filename: Optional[str] = None, file: Optional[BinaryIO] = None) -> Dict[str, Union[str, int]]:
    if file is not None:
        file_content = file.read()
    elif filename is not None:
        with open(filename, "rb") as file:
            file_content = file.read()
    else:
        raise ValueError("Either filename or file must be provided")
    
    # Get XF Karaoke Message chunk
    xfkm_marker = b'XFKM'
    xfkm_start_index = file_content.index(xfkm_marker)
    xfkm_content = file_content[xfkm_start_index:]
    
    info_header_marker = b'\xff\x07'
    info_header_start = xfkm_content.index(info_header_marker)
    info_header_length = xfkm_content[info_header_start + 2]  # FF 07 len text structure
    info_header_end = info_header_start + 3 + info_header_length
    info_header = xfkm_content[info_header_start:info_header_end]
    
    # Extract information (assuming no asian characters, so we can decode without considering encoding)
    song_id, melody_channel, time_offset, language = info_header[3:].decode().split(":")
    return {
        "song_id": song_id,
        "melody_channel": int(melody_channel),
        "time_offset": int(time_offset),
        "language": language
    }
    
class XFMidiFile(MidiFile):
    def __init__(self, filename: Optional[str] = None, file: Optional[BinaryIO] = None,
                 *args, **kwargs):
        super().__init__(filename, file, *args, **kwargs)
        
        # Add XF-specific attributes
        self.xfih = None  # XF Information Header
        self.xfkm = None  # XF Karaoke Message

        # Load XF-specific data
        # Note: This results in reading the file twice (once in the parent's __init__ and once here)
        # but it's acceptable for now to maintain compatibility with the parent class
        if file is not None:
            #file.seek(0)
            self._load_xf(file)
        elif filename is not None:
            with open(filename, "rb") as file:
                self._load_xf(file)
    
    def _load_xf(self, infile):
        if self.debug:
            infile = DebugFileWrapper(infile)

        with meta_charset(self.charset):
            
            current_position = infile.tell()
            # Read the rest of infile
            file_content = infile.read()
            # Read XF Information Header if present
            header = b'XFIH'
            if header in file_content:
                start_index = file_content.index(header)
                infile.seek(current_position + start_index) # Adjust infile position
                if self.debug:
                    _dbg('Track {}:'.format(header))

                self.xfih = read_xf_track(infile,
                                        debug=self.debug,
                                        clip=self.clip)
            # Read XF Karaoke Message if present
            current_position = infile.tell()
            # Read the rest of infile
            file_content = infile.read()            
            header = b'XFKM'
            
            if header in file_content:
                start_index = file_content.index(header)
                infile.seek(current_position + start_index) # Adjust infile position
                if self.debug:
                    _dbg('Track {}:'.format(header))

                self.xfkm = read_xf_track(infile,
                                        debug=self.debug,
                                        clip=self.clip)
