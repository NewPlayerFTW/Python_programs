import random
import time
import os
from threading import Thread, Lock
from Tkinter import *
from PIL import Image, ImageTk

DEAD, DYING, ALIVE, REVIVE = range(4)


class Cell:
    def __init__(self, x, y):
        self.current_state = -1
        self.next_state = -1
        self.x = x
        self.y = y
        self.taken = None


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
        for i in range(self.width):
            for j in range(self.height):
                if self.cells[i][j].next_state is DYING:
                    self.cells[i][j].current_state = DEAD
                else:
                    self.cells[i][j].current_state = ALIVE


class Tribe(Thread):
    lock = Lock()
    amount = 0
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
        for i in range(self.units):
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - 1)
            if None is self.board.cells[x][y].taken:
                self.board.cells[x][y].taken = True
                self.board.pixels[x, y] = self.color
            else:
                i -= 1

    def run(self):
        pass


# for i in range(1000):
#     print '\n' * 10
#     b.show()
#     b.update_states()
#     b.set_states()
#     time.sleep(1)
#     b.image.show()



b = Board(500, 500)
t1 = Tribe(b, 2000, (255, 0, 0))
t2 = Tribe(b, 2000, (0, 255, 0))
t3 = Tribe(b, 2000, (0, 0, 255))
t4 = Tribe(b, 2000, (255, 255, 0))
t5 = Tribe(b, 2000, (255, 0, 255))
print Tribe.amount

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

root = Tk()

display = ImageTk.PhotoImage(b.image)

label = Label(root, image=display)
label.pack()

root.mainloop()