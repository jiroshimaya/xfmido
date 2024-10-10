# XFMIDO

XFMIDOは、XF（拡張フォーマット）MIDIデータ処理のためのPythonライブラリです。

## 特徴

- XF準拠のヘッダー（XFIH）およびカラオケ情報（XFKM）チャンクの読み取り
- 標準的なMIDIファイル（SMF）の読み取りも可能

## 使い方

```
pip install xfmido
```


```python
from xfmido import XFMidiFile

# サンプルMIDIファイルを読み込む
xfmidifile = XFMidiFile("sample/sample.mid", charset="cp932")

# 読み込んだMIDIファイルの情報を表示
print("MIDIファイル情報:")
print(xfmidifile)

# XF準拠のヘッダー情報を表示
print("\nXFヘッダー情報:")
print(xfmidifile.xfih)

# カラオケ情報を表示
print("\nカラオケ情報:")
print(xfmidifile.xfkm)
```

```
MIDIファイル情報:
XFMidiFile(type=1, ticks_per_beat=480, tracks=[
  MidiTrack([
    Message('note_on', channel=0, note=60, velocity=100, time=0),
    Message('note_off', channel=0, note=60, velocity=64, time=480),
    MetaMessage('lyrics', text='Hello World', time=0),
    MetaMessage('end_of_track', time=0)])
])

XFヘッダー情報:
MidiTrack([
  MetaMessage('text', text='XF Version 1', time=0),
  MetaMessage('end_of_track', time=0)])

カラオケ情報:
MidiTrack([
  MetaMessage('cue_marker', text='$Lyrc:1:312:JP', time=0),
  MetaMessage('lyrics', text='Hello', time=0),
  MetaMessage('lyrics', text='World', time=480),
  MetaMessage('lyrics', text='Hello World', time=0),
  MetaMessage('end_of_track', time=0)])
```




