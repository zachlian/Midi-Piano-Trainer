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


print(mido.get_input_names())
portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
with mido.open_input(portname, callback=note_handler) as port:
    print("portname= ", port)
    while(1):
        pass