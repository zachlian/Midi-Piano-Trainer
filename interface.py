import pygame
import mido
import tkinter as tk
from freemode import FreeMode
from sampler import Sampler

class Mode:
    def start(self):
        pygame.init()
        pygame.mixer.init() 
        self.sampler = Sampler(pygame.mixer, False, False)
        
class FreeMode(Mode):
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
        super().start()
        self.visualizer = FreeMode()
        print(mido.get_input_names())
        portname = "CHMidi-2.3 0"  # replace with your MIDI INPUT
        
        with mido.open_input(portname, callback=self.note_handler) as port:
            try:
                self.visualizer.window.mainloop()
            except KeyboardInterrupt:
                pass

class AnotherMode(Mode):
    def start(self):
        pass

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.button1 = tk.Button(self.window, text="Free Mode", command=self.start_piano_visualizer)
        self.button1.pack()
        self.button2 = tk.Button(self.window, text="Another Mode", command=self.start_another_mode)
        self.button2.pack()

    def start_piano_visualizer(self):
        self.mode = FreeMode()
        self.mode.start()

    def start_another_mode(self):
        self.mode = AnotherMode()
        self.mode.start()

    def run(self):
        self.window.mainloop()