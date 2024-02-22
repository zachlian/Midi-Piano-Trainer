from tkinter import *
import tkinter as tk
from mido import MidiFile, MidiTrack
import mido
import time
START_W = 100
START_H = 400
RADIUS = 20
WINDOW_W = 1200
WINDOW_H = 400
KEY_NUM = 61
ORIGIN_COLOR = 'white'
PRESSED_COLOR = 'red'
START_KEY = 37
JUMP_RATE = 2

class PianoVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=1500, height=500)
        self.canvas.pack()
        self.keys = [None]*36 + [self.canvas.create_oval(START_W+i*RADIUS, START_H, START_W+i*RADIUS+RADIUS,
                                                          START_H+RADIUS, fill = ORIGIN_COLOR) for i in range(KEY_NUM)]
        self.recording = False
        self.mid = None
        self.track = None
        self.add_record_button()
        self.time = 0
    def add_record_button(self):
        self.record_button = tk.Button(self.window, text="Record", command=self.record)
        self.record_button.pack()
    
    def add_buttons(self):
        self.save_button = tk.Button(self.window, text="Save", command=self.save)
        self.save_button.pack()
        self.re_record_button = tk.Button(self.window, text="Re-record", command=self.re_record)
        self.re_record_button.pack()
        self.discard_button = tk.Button(self.window, text="Discard", command=self.discard)
        self.discard_button.pack()
    
    def destroy_buttons(self):
        self.save_button.destroy()
        self.re_record_button.destroy()
        self.discard_button.destroy()
        
    def record(self):
        print('Start recording')
        self.recording = True
        self.mid = MidiFile(ticks_per_beat=1)
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        self.record_button.destroy()
        self.add_buttons()
        self.time = time.time()
        
    def save(self):
        self.recording = False
        self.mid.save('new_song.mid')
        self.mid = None
        self.track = None
        self.destroy_buttons()
        self.add_record_button()
        
    def re_record(self):
        print('Stop recording')
        print('Start recording again')
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        
    def discard(self):
        print('Stop recording')
        self.recording = False
        self.mid = None
        self.track = None
        self.destroy_buttons()
        self.add_record_button()
        
    def press_key(self, key_id, velocity):
        self.canvas.itemconfig(self.keys[key_id], fill = PRESSED_COLOR)
        self.canvas.move(self.keys[key_id], 0, -velocity * JUMP_RATE)
        if self.recording:
            
            self.track.append(mido.Message('note_on', note=key_id, velocity=velocity, time=(time.time()-self.time)*1000))
            print(key_id, velocity)
            print(self.track)
            
        else:
            print(self.track)
    def release_key(self, key_id):
        self.canvas.move(self.keys[key_id], 0, START_H - self.canvas.coords(self.keys[key_id])[1])
        self.canvas.itemconfig(self.keys[key_id], fill = ORIGIN_COLOR)
        if self.recording:
            self.track.append(mido.Message('note_off', note=key_id, time=(time.time()-self.time)*1000))
            print(self.track)
