import mido
import tkinter as tk
from collections import defaultdict

class Note:
    def __init__(self, note, time):
        self.note = note
        self.time = time

class Track:
    def __init__(self):
        self.notes = defaultdict(list)

    def add_note(self, note):
        self.notes[note.time].append(note)

    def get_next_notes(self):
        if self.notes:
            time, notes = self.notes.popitem(0)
            return notes
        else:
            return None

class Song:
    def __init__(self, midi_file):
        self.tracks = [Track(), Track()]
        self.load_midi(midi_file)

    def load_midi(self, midi_file):
        mid = mido.MidiFile(midi_file)
        for i, track in enumerate(mid.tracks):
            time = 0
            for msg in track:
                time += msg.time
                if msg.type == 'note_on':
                    note = Note(msg.note, time)
                    self.tracks[i].add_note(note)

class PracMode_display:
    def __init__(self, file):
        self.window = tk.Tk()
        self.song = Song(file)
        self.current_notes = [[], []]

    def start(self):
        self.next_notes(0)
        self.next_notes(1)
        self.window.mainloop()

    def next_notes(self, track):
        self.current_notes[track] = self.song.tracks[track].get_next_notes()

    def on_key_press(self, event):
        for i, notes in enumerate(self.current_notes):
            for note in notes:
                if note and event.char == note.note:
                    self.next_notes(i)