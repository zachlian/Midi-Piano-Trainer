import mido
from mido import Message, MidiFile, MidiTrack
import time
import os
import pygame
from sampler import Sampler
from display import PianoVisualizer

# 建立 mido 的 MidiFile 和 MidiTrack
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

sampler: Sampler = None

def note_handler(note: mido.Message) -> None:
    if note.type in ["note_on", "note_off"]:
        print(note.type, ', ', note.note, ', ', note.velocity, ', ', note.time)
        note_id = int(note.note) if note.note is not None else -1
        if note.type == "note_on":
            sampler.play(note_id, note.velocity)
            visualizer.press_key(note_id, note.velocity)
        elif note.type == "note_off":
            sampler.stop(note_id)
            visualizer.release_key(note_id)

pygame.init()
pygame.mixer.init() 
sampler = Sampler(pygame.mixer, False, False)
visualizer = PianoVisualizer()

print(mido.get_input_names())
portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
with mido.open_input(portname, callback=note_handler) as port:
    try:
        visualizer.window.mainloop()
    except KeyboardInterrupt:
        pass