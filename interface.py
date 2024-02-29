import pygame
import mido
import tkinter as tk
from freemode import FreeMode_display
from sampler import Sampler
from pracmode import PracMode_display

class FreeMode():
    def note_handler(self, note: mido.Message) -> None:
        if note.type in ["note_on", "note_off"]:
            # print(note.type, ', ', note.note, ', ', note.velocity, ', ', note.time)
            note_id = int(note.note)
            if note.type == "note_on":
                self.sampler.play(note_id, note.velocity)
                self.visualizer.press_key(note_id, note.velocity)
            elif note.type == "note_off":
                self.sampler.stop(note_id)
                self.visualizer.release_key(note_id)

    def start(self):
        pygame.init()
        pygame.mixer.init() 
        self.sampler = Sampler(pygame.mixer, False, False)
        self.visualizer = FreeMode_display()
        print(mido.get_input_names())
        portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
        
        with mido.open_input(portname, callback=self.note_handler) as port:
            try:
                self.visualizer.window.mainloop()
            except KeyboardInterrupt:
                pass

class PracMode(FreeMode):
    def start(self):
        pygame.init()
        pygame.mixer.init() 
        self.sampler = Sampler(pygame.mixer, False, False)
        self.visualizer = PracMode_display('midi_files/test.mid')
        print(mido.get_input_names())
        portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
        
        with mido.open_input(portname, callback=self.note_handler) as port:
            try:
                self.visualizer.window.mainloop()
            except KeyboardInterrupt:
                pass

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.button1 = tk.Button(self.window, text="Free Mode", command=self.start_free_mode)
        self.button1.pack()
        self.button2 = tk.Button(self.window, text="Another Mode", command=self.start_prac_mode)
        self.button2.pack()

    def start_free_mode(self):
        self.mode = FreeMode()
        self.mode.start()

    def start_prac_mode(self):
        self.mode = PracMode()
        self.mode.start()

    def run(self):
        self.window.mainloop()