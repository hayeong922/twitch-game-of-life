import socket

import numpy as np
from PIL import Image, ImageDraw

from settings import PASS, USER

size = 10

class Conway:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))

    #use two matrices, 
    def tick(self):
        new = np.copy(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                adj_count = 0
                if self.grid[(r+1)%self.rows,c]: adj_count += 1
                if self.grid[(r+1)%self.rows,(c+1)%self.cols]: adj_count += 1
                if self.grid[r,(c+1)%self.cols]: adj_count += 1
                if self.grid[r-1,(c+1)%self.cols]: adj_count += 1
                if self.grid[r-1,c]: adj_count += 1
                if self.grid[r-1,c-1]: adj_count += 1
                if self.grid[r,c-1]: adj_count += 1
                if self.grid[(r+1)%self.rows,c-1]: adj_count += 1
                if self.grid[r,c]:
                    if adj_count < 2 or adj_count > 3:
                        new[r,c] = 0
                else:
                    if adj_count == 3:
                        new[r,c] = 1
        self.grid = new

    def draw(self):
        im = Image.new("RGB", (self.rows*size, self.cols*size), color="white")
        draw = ImageDraw.Draw(im)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r,c]:
                    draw.rectangle([c*size, r*size, (c+1)*size, (r+1)*size],
                                   fill="black",
                                   outline="gray")
        im.save("grid.png")
        
    def flip(self, r, c):
        self.grid[r,c] = not self.grid[r,c]

def create_block(m, r, c):
    m[r,c] = 1
    m[r,c+1] = 1
    m[r+1,c] = 1
    m[r+1,c+1] = 1

def open_socket():
    s = socket.socket()
    s.connect(("irc.twitch.tv", 6667))
    s.send(b"PASS " + PASS + b"\r\n")
    s.send(b"NICK " + USER + b"\r\n")
    s.send(b"JOIN #" + USER + b"\r\n")
    return s

g = Conway(10, 10)
create_block(g.grid,0,0)
create_block(g.grid,2,2)