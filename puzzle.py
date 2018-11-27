from tkinter import *

import numpy

from ann import Ann
from logic import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

map_key_name_to_number_dict = {
  "up": [1, 0, 0, 0],
  "left": [0, 1, 0, 0],
  "down": [0, 0, 1, 0],
  "right": [0, 0, 0, 1]
}

def get_rand_key():
  number = randint(1, 50)

  if number in range(0, 24):
    return 'w'
  if number in range(24, 49):
    return 'a'
  if number == 49:
    return 's'
  if number == 50:
    return 'd'

def convert_number_to_key(number):
  if number == 1:
    return 'w'
  if number == 2:
    return 'a'
  if number == 3:
    return 's'
  if number == 4:
    return 'd'


def get_next_key(game, random: BooleanVar, ann):
  class Result:
    pass

  if random:
    Result.char = get_rand_key()

  else:
    Result.char = convert_number_to_key(ann.predict(numpy.array([flatten_game(game)])))

  return Result


def flatten_game(game):
  return [i for sublist in game for i in sublist]


class GameGrid(Frame):
  def __init__(self, max_score, ann):
    Frame.__init__(self)

    self.grid()
    self.master.title('2048')
    self.master.bind("<Key>", self.key_down)

    # self.gamelogic = gamelogic
    self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                     KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}

    self.grid_cells = []
    self.init_grid()
    self.init_matrix()
    self.update_grid_cells()
    self.inputs = None

    self.max_score = max_score
    self.ann = ann
    self.prev_matrix = self.matrix

    self.total_steps = 0
    self.random_steps = 0

    def my_mainloop():
      self.total_steps += 1
      isRandom = max_score == 0 or self.matrix == self.prev_matrix
      if isRandom:
        self.random_steps += 1
      self.prev_matrix = self.matrix
      self.key_down(
        get_next_key(
          self.matrix,
          isRandom,
          self.ann))
      if game_state(self.matrix) != 'lose' and game_state(self.matrix) != 'win':
        self.after(5, my_mainloop)
      else:
        if game_state(self.matrix) == 'lose':
          score = sum([i for sublist in self.matrix for i in sublist])
          print('Current score: ' + str(score) + ' max score: ' + str(max_score) + ' random percent: ' + str(
            self.random_steps / self.total_steps * 100))
          if score > self.max_score:
            self.max_score = score
            if self.ann is None:
              self.ann = Ann(self.inputs)
            else:
              self.ann.fit(self.inputs, epochs=self.total_steps)

          self.destroy()
          GameGrid(self.max_score, self.ann)
        else:
          print('win!')

    self.after(1000, my_mainloop)
    self.mainloop()


  def init_grid(self):
    background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
    background.grid()
    for i in range(GRID_LEN):
      grid_row = []
      for j in range(GRID_LEN):
        cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
        cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
        # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
        t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
        t.grid()
        grid_row.append(t)

      self.grid_cells.append(grid_row)

  def gen(self):
    return randint(0, GRID_LEN - 1)

  def init_matrix(self):
    self.matrix = new_game(4)

    self.matrix = add_two(self.matrix)
    self.matrix = add_two(self.matrix)

  def update_grid_cells(self):
    for i in range(GRID_LEN):
      for j in range(GRID_LEN):
        new_number = self.matrix[i][j]
        if new_number == 0:
          self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
        else:
          self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
            fg=CELL_COLOR_DICT[new_number])
    self.update_idletasks()

  def key_down(self, event):
    key = repr(event.char)
    if key in self.commands:
      arr = []
      for sublist in self.matrix:
        for item in sublist:
          arr.append(item)

      arr += self.map_key_name_to_number(event)
      if self.inputs is None:
        self.inputs = numpy.array(arr)
      else:
        self.inputs = numpy.vstack([self.inputs, arr])
      self.matrix, done = self.commands[repr(event.char)](self.matrix)
      if done:
        self.matrix = add_two(self.matrix)
        self.update_grid_cells()
        done = False
        if game_state(self.matrix) == 'win':
          self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
          self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
        if game_state(self.matrix) == 'lose':
          self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
          self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)

  def map_key_name_to_number(self, event):
    return map_key_name_to_number_dict[self.commands[repr(event.char)].__name__]

  def generate_next(self):
    index = (self.gen(), self.gen())
    while self.matrix[index[0]][index[1]] != 0:
      index = (self.gen(), self.gen())
    self.matrix[index[0]][index[1]] = 2


gamegrid = GameGrid(0, None)
