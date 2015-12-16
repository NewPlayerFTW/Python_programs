import random
import time
import os
from threading import Thread, Lock, Condition
from Tkinter import *
from PIL import Image, ImageTk

DEAD, DYING, ALIVE, REVIVE = range(4)


class Cell:
    def __init__(self, x, y):
        self.current_state = -1
        self.next_state = -1
        self.x = x
        self.y = y
        self.visited = None
        self.color = (255, 255, 255)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.create_array_of_cells(width, height)
        self.image = Image.new('RGB', (self.width, self.height))
        self.pixels = self.image.load()

    def load_from_file(self, name):
        file = open(name, 'r')
        for i in range(self.width):
            marks = list(file.readline())
            for j in range(len(marks) - 1):
                if '.' is marks[j]:
                    self.cells[i][j].current_state = DEAD
                    self.cells[i][j].next_state = DYING
                else:
                    self.cells[i][j].current_state = ALIVE
                    self.cells[i][j].next_state = REVIVE


    def create_array_of_cells(self, width, height):
        cells = []
        for i in range(width):
            cells.append([None] * width)
            cells[i] = [Cell(i, j) for j in range(height)]
        return cells

    def show(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.cells[i][j].current_state is ALIVE:
                    print 'o',
                else:
                    print '#',
            print

    def index_in_range(self, x, y):
        return (0 <= x and x < self.width and 0 <= y and y < self.height)

    def count_alive_cells(self, cell):
        alive = 0
        for i in range(-1, 2, 1):
            x = cell.x + i
            y = cell.y - 1
            if(self.index_in_range(x, y) and self.cells[x][y].current_state):
                alive += 1
        if(self.index_in_range(cell.x - 1, cell.y) and self.cells[cell.x - 1][cell.y].current_state):
            alive += 1
        if(self.index_in_range(cell.x + 1, cell.y) and self.cells[cell.x + 1][cell.y].current_state):
            alive += 1
        for i in range(-1, 2, 1):
            x = cell.x + i
            y = cell.y + 1
            if(self.index_in_range(x, y) and self.cells[x][y].current_state):
                alive += 1
        return alive

    def update_states(self):
        for i in range(self.width):
            for j in range(self.height):
                alive_around = self.count_alive_cells(self.cells[i][j])
                if self.cells[i][j].current_state is ALIVE:
                    if 2 > alive_around or 4 <= alive_around:
                        self.cells[i][j].next_state = DYING
                else:
                    if 3 is alive_around:
                        self.cells[i][j].next_state = REVIVE

    def set_states(self):
        self.pixels = self.image.load()
        for i in range(self.width):
            for j in range(self.height):
                if self.cells[i][j].next_state is DYING:
                    self.cells[i][j].current_state = DEAD
                    self.pixels[i, j] = (0, 0, 0)
                else:
                    self.cells[i][j].current_state = ALIVE
                    self.pixels[i, j] = self.cells[i][j].color


class Tribe(Thread):
    lock = Lock()
    condition = Condition()

    amount = 0
    count = 0
    def __init__(self, board, units, color):
        super(Tribe, self).__init__()
        self.board = board
        self.color = color
        self.units = units
        self.populate()

        Tribe.lock.acquire()
        Tribe.amount += 1
        Tribe.lock.release()

    def populate(self):
        cells = self.board.cells
        pixels = self.board.pixels
        for i in range(self.units):
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - 1)
            if None is cells[x][y].visited:
                cells[x][y].visited = True
                pixels[x, y] = self.color
            else:
                i -= 1

    def run(self):
        while(1):
            cells = self.board.cells
            for i in range(self.board.width):
                for j in range(self.board.height):
                    if None is cells[i][j].visited and False is Tribe.lock.locked():
                        Tribe.lock.acquire()
                        cells[i][j].visited = True
                        cells[i][j].color = self.color
                        Tribe.lock.release()

            if False is Tribe.lock.locked():
                Tribe.lock.acquire()
                Tribe.count += 1
                Tribe.lock.release()

            Tribe.condition.acquire()
            while Tribe.count != Tribe.amount:
                Tribe.condition.wait()

            Tribe.condition.notify_all()
            Tribe.condition.release()
            Tribe.count = 0


def loop(board, threads, iterations, tk, label):
    if 0 < iterations:
        print 'loop {:d}'.format(100 - iterations)
        board.update_states()
        board.set_states()

        tk.after(100, loop, board, Tribes, iterations - 1, tk)


#Board init
board = Board(300, 300)

#Threads init
Tribes = []
Tribes.append(Tribe(board, 2000, (255, 0, 0)))
Tribes.append(Tribe(board, 2000, (0, 255, 0)))
Tribes.append(Tribe(board, 2000, (0, 0, 255)))
Tribes.append(Tribe(board, 2000, (255, 255, 0)))
Tribes.append(Tribe(board, 2000, (255, 0, 255)))
for i in range(len(Tribes)):
    Tribes[i].start()
#for i in range(len(Tribes)):
#    Tribes[i].join()

#Tkinter init
tk = Tk()
display = ImageTk.PhotoImage(board.image)
label = Label(tk, image=display)
label.pack()

tk.after(100, loop, board, Tribes, 100, tk)
tk.mainloop()