import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

size = 10
tickrate = .5

class Conway:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.flip_queue = []
        self.generation = 0

    def count_neighbors(self, r, c):
        adj_count = 0
        if self.grid[(r+1)%self.rows,c]: adj_count += 1
        if self.grid[(r+1)%self.rows,(c+1)%self.cols]: adj_count += 1
        if self.grid[r,(c+1)%self.cols]: adj_count += 1
        if self.grid[r-1,(c+1)%self.cols]: adj_count += 1
        if self.grid[r-1,c]: adj_count += 1
        if self.grid[r-1,c-1]: adj_count += 1
        if self.grid[r,c-1]: adj_count += 1
        if self.grid[(r+1)%self.rows,c-1]: adj_count += 1
        return adj_count

    def tick(self):
        new = np.copy(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                adj_count = self.count_neighbors(r, c)
                if self.grid[r,c]:
                    if adj_count < 2 or adj_count > 3:
                        new[r,c] = 0
                else:
                    if adj_count == 3:
                        new[r,c] = 1
        self.grid = new
        self.generation += 1

    def draw(self):
        im = Image.new("RGB", (self.rows*size, self.cols*size), color="white")
        draw = ImageDraw.Draw(im)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r,c]:
                    draw.rectangle([c*size, r*size, (c+1)*size, (r+1)*size], fill="black", outline="gray")
        #windows
        draw.text((0, self.rows*size*.9), repr(self.generation), fill="black", font=ImageFont.truetype("arial", size=int(self.rows*size*.1)))
        im.save("grid.png")
        
    def flip(self):
        draw = False
        for r, c in self.flip_queue:
            self.grid[r,c] = not self.grid[r,c]
            draw = True
        self.flip_queue = []
        return draw

    def loop(self):
        while True:
            self.flip
            self.draw()
            time.sleep(tickrate/2)
            self.tick()
            self.draw()
            time.sleep(tickrate/2)
            print("Generation {}".format(self.generation))

def create_block(m, r, c):
    m[r,c] = 1
    m[r,c+1] = 1
    m[r+1,c] = 1
    m[r+1,c+1] = 1

g = Conway(10, 10)
create_block(g.grid,0,0)
create_block(g.grid,2,2)