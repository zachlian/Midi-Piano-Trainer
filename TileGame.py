import mido
from mido import Message, MidiFile, MidiTrack
import time
import os
from sampler import Sampler
# 建立 mido 的 MidiFile 和 MidiTrack
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

sampler: Sampler = None

# 找出第一個可用的 MIDI 輸入裝置
input_name = mido.get_input_names()[0]

def note_handler(note: mido.Message) -> None:
    """
    Midi message event handler
    """
    if note.type in ["note_on", "note_off"]:
        print('inf: ', note.type, note.note, note.velocity, note.time)
        note_id = int(note.note) if note.note is not None else -1
        if note.type == "note_on":
            sampler.play(note_id, note.velocity)

        elif note.type == "note_off":
            sampler.stop(note_id)

# 開啟 MIDI 輸入裝置
with mido.open_input(input_name) as inport:
    for msg in inport:
        # MIDI 訊息的第一個位元組是狀態位元組，它的高四位元碼表明訊息的類型
        status_byte = msg.type
        note = msg.note
        velocity = msg.velocity
        timestamp = msg.time

        # 判斷 MIDI 訊息的類型
        if status_byte == 'note_on':  # Note on
            print(f"{note} key, on")
            track.append(Message('note_on', note=note, velocity=velocity, time=timestamp))
        elif status_byte == 'note_off':  # Note off
            print(f"{note} key, off")
            track.append(Message('note_off', note=note, velocity=velocity, time=timestamp))

        # 儲存 MIDI 檔案
        #mid.save('output.mid')