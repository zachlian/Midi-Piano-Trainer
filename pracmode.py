import mido
from mido import tempo2bpm
import tkinter as tk
from collections import OrderedDict
from drawPiano import WINDOW_H, WINDOW_W, draw_piano, find_ori_color
PRESSED_COLOR = "red"
HL_COLOR_RIGHT = "green"
HL_COLOR_LEFT = "blue"

class Note:
    def __init__(self, note, time):
        self.note_id = int(note)
        self.time = time
        self.end_time = None

class Song:
    def __init__(self, midi_file):
        self.tracks = [[], []]
        self.load_midi(midi_file)
        self.second_per_tick: float
        
    def load_midi(self, midi_file):
        mid = mido.MidiFile(midi_file)
        ticks_per_beat = mid.ticks_per_beat
        # print('ticks per beat', ticks_per_beat)
        note_start_times = {}
        for i, track in enumerate(mid.tracks):
            time = 0
            for msg in track:
                if msg.type == 'set_tempo':
                    #print('tempo', msg.tempo)
                    tempo = msg.tempo
                # print(msg)
                time += msg.time
                if msg.type == 'note_on':
                    if msg.velocity != 0:
                        note = Note(msg.note, time)
                        note_start_times[note.note_id] = note
                        self.tracks[i].append(note)
                    else:
                        if msg.note in note_start_times:
                            note_start_times[msg.note].end_time = time
                        else:
                            print(f"Warning: note_off for note {msg.note} found without corresponding note_on")
                elif msg.type == 'note_off':
                    if msg.note in note_start_times:
                        note_start_times[msg.note].end_time = time
                    else:
                        print(f"Warning: note_off for note {msg.note} found without corresponding note_on")
        self.second_per_tick =1/(tempo2bpm(tempo) / 60 * ticks_per_beat)

class PracMode_display:
    def __init__(self, file_name):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=WINDOW_W, height=WINDOW_H)
        self.canvas.pack()
        self.song = Song(file_name)
        self.current_tick = 0 # current time in the song
        self.is_paused = False # whether the song is paused
        self.keys = draw_piano(self) # draw the piano
        self.isHightlighted = [(-1) for _ in range(109)] # -1 for not highlighted, 0 for right, 1 for left
        self.current_press_notes = [] # list of notes that are currently being pressed
        self.pass_num_0 = 0 # number of notes that have been passped
        self.pass_num_1 = 0
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        self.window.quit()
        self.window.destroy()

    def update_time(self):
        if not self.is_paused:
            self.current_tick += 1
            #print(self.current_tick)
            self.highlight_keys()
        self.check_press()
        self.window.after(round(self.song.second_per_tick * 1000), self.update_time)

    def highlight_keys(self):
        for note in self.song.tracks[0][self.pass_num_0:self.pass_num_0+8]:
            if self.current_tick >= note.time and self.current_tick <= note.end_time:
                #print('check1', note.note_id)
                self.canvas.itemconfig(self.keys[note.note_id-21], fill = HL_COLOR_RIGHT)
                self.isHightlighted[note.note_id] = 0
            else:
                if note.end_time < self.current_tick:
                    self.pass_num_0 += 1
                self.canvas.itemconfig(self.keys[note.note_id-21], fill = find_ori_color(note.note_id))
                self.isHightlighted[note.note_id] = -1
                
        for note in self.song.tracks[1][self.pass_num_1:self.pass_num_1+8]:
            if self.current_tick >= note.time and self.current_tick <= note.end_time:
                #print('check2', note.note_id)
                self.canvas.itemconfig(self.keys[note.note_id-21], fill = HL_COLOR_LEFT)
                self.isHightlighted[note.note_id] = 1
            else:
                if note.end_time < self.current_tick:
                    self.pass_num_1 += 1
                self.canvas.itemconfig(self.keys[note.note_id-21], fill = find_ori_color(note.note_id))
                self.isHightlighted[note.note_id] = -1
    
    def check_press(self):
        '''
        Checks if user has pressed the correct notes
        '''
        curr_notes_right = []
        curr_notes_left = []
        for i in range(21, 109):
            if self.isHightlighted[i] == 0:
                curr_notes_right.append(i)
            elif self.isHightlighted[i] == 1:
                curr_notes_left.append(i)
        # print('curr_press', self.current_press_notes)
        # print('expect', curr_notes_right+curr_notes_left)
        right_correct = all(note in self.current_press_notes for note in curr_notes_right)
        left_correct = all(note in self.current_press_notes for note in curr_notes_left)
        if right_correct and left_correct:
            self.is_paused = False
        elif self.current_tick == self.song.tracks[0][self.pass_num_0].end_time\
            or self.current_tick == self.song.tracks[1][self.pass_num_1].end_time:
            self.is_paused = True
    
    def press_key(self, key_id, velocity):
        self.current_press_notes.append(key_id)
        x1, y1, x2, y2 = self.canvas.coords(self.keys[key_id-21])  # 獲取按鍵的邊界
        radius = 5 # 圓圈的半徑
        x = (x1 + x2) / 2  # 圓圈的中心 x 座標
        y = y2 - radius * 3  # 圓圈的中心 y 座標
        if find_ori_color(key_id) == "white":
            x -= 2.5*33
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=PRESSED_COLOR, tags=f"circle{key_id}")

    def release_key(self, key_id):
        self.current_press_notes.remove(key_id)
        self.canvas.delete(f"circle{key_id}")  # 刪除圓圈
        
