import mido
from mido import MidiFile, MidiTrack
import time
from datetime import datetime
import os
class Recorder:
    def record(self):
        print('Start recording')
        self.mid = MidiFile(ticks_per_beat=480)
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        self.last_time = time.time()
        
    def add_note(self, note_id, velocity, on: bool):
        current_time = time.time() - self.last_time
        self.last_time = time.time()
        current_tick = int(round(mido.second2tick(current_time, self.mid.ticks_per_beat, mido.bpm2tempo(120))))
        if on:
            self.track.append(mido.Message('note_on', note=note_id, velocity=velocity, time=current_tick))
        else:
            self.track.append(mido.Message('note_off', note=note_id, velocity=velocity, time=current_tick))
        
    def save(self):
        print('Save recording')
        cur = datetime.now()
        name = f'{cur.year}{cur.month:02d}{cur.day:02d}-{cur.hour:02d}{cur.minute:02d}{cur.second:02d}'
        self.mid.save(os.path.join('Recordings/'+name+'.mid'))
    
    def discard(self):
        print('Discard recording')
        self.mid = None
        self.track = None
        self.last_time = None