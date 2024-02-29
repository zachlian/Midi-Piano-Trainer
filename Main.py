import pygame
import mido
import tkinter as tk
from freemode import FreeMode_ball, FreeMode_piano
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

    def start(self, mode):
        pygame.init()
        pygame.mixer.init() 
        self.sampler = Sampler(pygame.mixer, False, False)
        if mode == 0: # free mode
            self.visualizer = FreeMode_ball()
        elif mode == 1: # piano
            self.visualizer = FreeMode_piano()

        portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT   
        with mido.open_input(portname, callback=self.note_handler) as port:
            self.visualizer.window.mainloop()

class PracMode(FreeMode):
    def start(self):
        pygame.init()
        pygame.mixer.init() 
        self.sampler = Sampler(pygame.mixer, False, False)
        self.visualizer = PracMode_display('midi_files/test.mid')
        
        portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
        with mido.open_input(portname, callback=self.note_handler) as port:
            self.visualizer.window.mainloop()

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.button1 = tk.Button(self.window, text="FreeMode-Ball", command=self.start_free_mode_ball)
        self.button1.pack()
        self.button1 = tk.Button(self.window, text="FreeMode-Piano", command=self.start_free_mode_piano)
        self.button1.pack()
        self.button2 = tk.Button(self.window, text="PracMode", command=self.start_prac_mode)
        self.button2.pack()

    def start_free_mode_ball(self):
        self.mode = FreeMode()
        self.mode.start(0)
    
    def start_free_mode_piano(self):
        self.mode = FreeMode()
        self.mode.start(1)

    def start_prac_mode(self):
        self.mode = PracMode()
        self.mode.start()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    interface = MainInterface()
    interface.run()