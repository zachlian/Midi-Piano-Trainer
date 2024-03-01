from tkinter import *
import tkinter as tk
from recorder import Recorder
from drawPiano import draw_piano, WINDOW_H, WINDOW_W, find_ori_color

KEY_NUM = 61
RADIUS = 20
WINDOW_W_B = 1300
WINDOW_H_B = 200
WINDOW_W_P = WINDOW_W
WINDOW_H_P = WINDOW_H
START_W = (WINDOW_W_B - KEY_NUM*RADIUS)/2
START_H = 140
ORIGIN_COLOR = 'white'
PRESSED_COLOR = 'red'
START_KEY = 37
JUMP_RATE = 1
RECORD_KEY = 36
SAVE_KEY = 38
DISCARD_KEY = 40

class FreeMode_ori:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=WINDOW_W_B, height=WINDOW_H_B)
        #self.canvas.pack()
        self.recorder = Recorder()
        self.add_buttons()
        self.time = 0
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        # Stop the loop
        self.window.quit()

        # Close the window
        self.window.destroy()
    def is_recording(self, is_rec):
        if is_rec:
            self.canvas.create_oval(15, 15, 30, 30, fill = 'red')
        else:
            self.canvas.create_oval(15, 15, 30, 30, fill = 'white')
            
    def add_buttons(self):
        self.record_button = tk.Button(self.window, text="Record", command=self.record)
        self.record_button.place(x=40, y=0, anchor='n')
        #self.record_button.pack()
        self.save_button = tk.Button(self.window, text="Save", command=self.save)
        self.save_button.place(relx=100, y=0, anchor='n')
        #self.save_button.pack()
        self.discard_button = tk.Button(self.window, text="Discard", command=self.discard)
        self.discard_button.place(x=160, y=0, anchor='n')
        #self.discard_button.pack()
        
    def record(self):
        self.recorder.record()
        self.is_recording(True)
        
    def save(self):
        self.recorder.save()
        self.is_recording(False)
        
    def discard(self):
        self.recorder.discard()
        self.is_recording(False)
        
    def press_key(self):
        pass
    
    def release_key(self):
        pass

class FreeMode_ball(FreeMode_ori):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self.window, width=WINDOW_W_B, height=WINDOW_H_B)
        self.canvas.pack()
        self.keys = [None]*36 + [self.canvas.create_oval(START_W+i*RADIUS, START_H, START_W+i*RADIUS+RADIUS,
                                                         START_H+RADIUS, fill = ORIGIN_COLOR) for i in range(KEY_NUM)]
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

class FreeMode_piano(FreeMode_ori):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self.window, width=WINDOW_W_P, height=WINDOW_H_P)
        self.canvas.pack()
        self.keys = draw_piano(self)
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

        self.canvas.itemconfig(self.keys[key_id-21], fill = PRESSED_COLOR)
        self.recorder.add_note(key_id, velocity, True)
        
    def release_key(self, key_id):
        self.canvas.itemconfig(self.keys[key_id-21], fill=find_ori_color(key_id))
        self.recorder.add_note(key_id, 0, False)