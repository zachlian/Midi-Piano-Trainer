from tkinter import *
import tkinter as tk
from recorder import Recorder

KEY_NUM = 61
RADIUS = 20
WINDOW_W = 1300
WINDOW_H = 200
START_W = (WINDOW_W - KEY_NUM*RADIUS)/2
START_H = 140
ORIGIN_COLOR = 'white'
PRESSED_COLOR = 'red'
START_KEY = 37
JUMP_RATE = 1
RECORD_KEY = 36
SAVE_KEY = 38
DISCARD_KEY = 40

class FreeMode:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=WINDOW_W, height=WINDOW_H)
        self.canvas.pack()
        self.keys = [None]*36 + [self.canvas.create_oval(START_W+i*RADIUS, START_H, START_W+i*RADIUS+RADIUS,
                                                          START_H+RADIUS, fill = ORIGIN_COLOR) for i in range(KEY_NUM)]
        self.recorder = Recorder()
        self.add_buttons()
        self.is_recording(False)
        self.time = 0
    
    def is_recording(self, is_rec: bool):
        if is_rec:
            self.canvas.create_oval(30, 30, 45, 45, fill = 'red')
        else:
            self.canvas.create_oval(30, 30, 45, 45, fill = 'white')
        
    def add_buttons(self):
        self.record_button = tk.Button(self.window, text="Record", command=self.record)
        self.record_button.pack(side = tk.LEFT)
        self.save_button = tk.Button(self.window, text="Save", command=self.save)
        self.save_button.pack(side = tk.LEFT)
        self.discard_button = tk.Button(self.window, text="Discard", command=self.discard)
        self.discard_button.pack(side = tk.LEFT)
        
    def record(self):
        self.recorder.record()
        self.is_recording(True)
        
    def save(self):
        self.recorder.save()
        self.is_recording(False)
        
    def discard(self):
        self.recorder.discard()
        self.is_recording(False)
        
    def press_key(self, key_id, velocity):
        if key_id == RECORD_KEY:
            self.record()
            return
        if key_id == SAVE_KEY:
            self.save()
            return
        if key_id == DISCARD_KEY:
            self.discard()
            return
        self.canvas.itemconfig(self.keys[key_id], fill = PRESSED_COLOR)
        self.canvas.move(self.keys[key_id], 0, -velocity * JUMP_RATE)
        self.recorder.add_note(key_id, velocity, True)
        
    def release_key(self, key_id):
        self.canvas.move(self.keys[key_id], 0, START_H - self.canvas.coords(self.keys[key_id])[1])
        self.canvas.itemconfig(self.keys[key_id], fill = ORIGIN_COLOR)
        self.recorder.add_note(key_id, 0, False)
