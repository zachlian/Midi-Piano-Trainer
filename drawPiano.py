import tkinter as tk

START_W = 0
START_H = 40
WHITE_WIDTH = 33
WHITE_HEIGHT = 200
BLACK_WIDTH = 21
BLACK_HEIGHT = 120
WINDOW_W_P = 52*WHITE_WIDTH
WINDOW_H_P = WHITE_HEIGHT+40

def draw_piano(self):
    white_rects = []
    black_rects = []
    for i in range(52):
        x1 = START_W + i * WHITE_WIDTH
        y1 = START_H
        rect = self.canvas.create_rectangle(x1, y1, x1 + WHITE_HEIGHT, y1 + WHITE_HEIGHT, fill='white')
        white_rects.append(rect)
    
    pattern = [2, 3]
    pattern_index = 0
    key_count = 0

    rect = self.canvas.create_rectangle(START_W + WHITE_WIDTH - (BLACK_WIDTH/2), START_H,
                                        START_W + WHITE_WIDTH + (BLACK_WIDTH/2), START_H + BLACK_HEIGHT, fill='black')
    black_rects.append(rect)
    
    for i in range(48):
        if key_count < pattern[pattern_index]:
            x1 = START_W + 2*WHITE_WIDTH + (i+1)*WHITE_WIDTH - (BLACK_WIDTH/2)
            y1 = START_H
            rect = self.canvas.create_rectangle(x1, y1, x1 + BLACK_WIDTH, y1 + BLACK_HEIGHT, fill='black')
            black_rects.append(rect)
            key_count += 1
        else:
            pattern_index = (pattern_index + 1) % len(pattern)
            key_count = 0
            
    keys = white_rects + black_rects
    keys_sorted = sorted(keys, key=lambda rect: self.canvas.coords(rect)[0])
    return keys_sorted
    