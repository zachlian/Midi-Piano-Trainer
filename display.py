from tkinter import *
import tkinter as tk
START_W = 100
START_H = 100
RADIUS = 20
WINDOW_W = 1200
WINDOW_H = 400

class PianoVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=1500, height=500)
        self.canvas.pack()
        self.keys = [self.canvas.create_oval(START_W+i*RADIUS, START_H, START_W+i*RADIUS+RADIUS, START_H+RADIUS, fill='white') for i in range(88)]

    def press_key(self, key_id, velocity):
        self.canvas.itemconfig(self.keys[key_id], fill='red')
        self.canvas.move(self.keys[key_id], 0, -velocity)

    def release_key(self, key_id):
        self.canvas.move(self.keys[key_id], 0, self.canvas.coords(self.keys[key_id])[1] - 100)