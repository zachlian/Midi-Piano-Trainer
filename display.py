from tkinter import *
import tkinter as tk
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

    def press_key(self, key_id, velocity):
        self.canvas.itemconfig(self.keys[key_id], fill = PRESSED_COLOR)
        self.canvas.move(self.keys[key_id], 0, -velocity * JUMP_RATE)

    def release_key(self, key_id):
        self.canvas.move(self.keys[key_id], 0, START_H - self.canvas.coords(self.keys[key_id])[1])
        self.canvas.itemconfig(self.keys[key_id], fill = ORIGIN_COLOR)
        