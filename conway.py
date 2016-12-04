import time
from threading import Thread

import pygame
import numpy as np

from chat import Chat

size = 10
tickrate = 1

def update_flips(game, chat):
    while True:
        for message in chat.get_messages():
            if message.startswith("flip"):
                split = message[4:].strip().split(",")
                if len(split) == 2 and all([n.isnumeric() for n in split]):
                    print("Flipped {}".format(split)) 
                    game.flip_queue.append(split)

class Conway:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.flip_queue = []
        self.generation = 0
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        self.font = pygame.font.SysFont("monospace", int(self.rows*size*.04))
        chat = Chat()
        self.chat_thread = Thread(target=update_flips, args=(self,chat))
        self.chat_thread.start()

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
        self.screen.fill((255,255,255))
        im = Image.new("RGB", (self.rows*size, self.cols*size), color="white")
        draw = ImageDraw.Draw(im)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r,c]:
                    pygame.draw.rect(self.screen, (0,0,0), [c*size, r*size, size, size], 0)
                    pygame.draw.rect(self.screen, (127,127,127), [c*size, r*size, size, size], 1)
        #windows
        #text = draw.text("{}".format(self.generation), 1, (0,0,0))
        #self.screen.blit(text, (size, int(self.rows*size*.96)))
        #draw.text(, repr(self.generation), fill="black", font=ImageFont.truetype("arial", size=int(self.rows*size*.04)))
        #im.save("grid.png")
        pygame.display.update()
        
    def flip(self):
        for r, c in self.flip_queue:
            self.grid[r,c] = not self.grid[r,c]
            draw = True
        self.flip_queue = []

    def loop(self):
        exit = False
        while not exit:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit = True
            self.flip()
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