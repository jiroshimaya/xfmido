# XFMIDO

XFMIDOは、XF（拡張フォーマット）MIDIデータ処理のためのPythonライブラリです。  
[mido](https://github.com/mido/mido)をベースとしています。

#### [English](https://github.com/jiroshimaya/xfmido/blob/main/README.md) | 日本語
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

## 背景
XFフォーマットは、ヤマハ株式会社が開発した標準MIDIファイルフォーマットの拡張であり、日本で広く使用されています。ヤマハのウェブサイトで購入可能なほとんどのMIDIファイルは、この仕様に準拠しています。XFフォーマットの詳細な仕様は以下のリンクから確認できます: https://jp.yamaha.com/files/download/other_assets/7/321757/xfspc.pdf

midoはXF仕様の専用チャンクを読み取らないため、歌詞情報などがそこに書かれていた場合、取得できません。もし取得できれば、歌詞とタイミングとメロディが取得でき、様々なアプリケーションの開発が便利になることが期待されます。そこでmidoを拡張し、XF仕様独自のXFIH、XFKMヘッダーを持つチャンクを読み取れるようにしたいと思いました。


# 開発者向け

- パッケージ管理に[uv](https://github.com/astral-sh/uv)を使用しています。
- コマンド管理に[taskipy](https://github.com/taskipy/taskipy)を使用しています。

```
uv run task test
uv run task lint
uv run task format
```

