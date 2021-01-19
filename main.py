import pygame
import random
import os
import sys
import time
import tkinter as tk
from pprint import pprint

stat = [0, 0, 0, 0, 0, 0]


def load_image(colorkey=None):
    fullname = os.path.join('flag5.png')
    image = pygame.image.load(fullname)
    return image


class Cell:
    def __init__(self, is_b, is_op, is_flag, opb):
        self.op_b = opb
        self.is_b = is_b
        self.is_op = is_op
        self.is_flag = is_flag
        self.value = -1

    def set_value(self, value):
        if not self.is_b:
            self.value = value

    def get_value(self):
        return self.value

    def get_flag(self):
        return self.is_flag

    def set_flag(self):
        if self.is_flag:
            self.is_flag = False
        else:
            self.is_flag = True

    def set_bomb(self):
        self.is_b = True

    def set_open(self):
        self.is_op = True

    def bomb(self):
        return self.is_b

    def open(self):
        return self.is_op


class Minesweeper:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.start_time = 0
        self.t1 = time.time()
        self.board = [[Cell(False, False, False, False) for _ in range(width)] for _ in range(height)]
        self.was_in_cell = [[False for _ in range(width)] for _ in range(height)]
        self.mines = mines
        self.colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
                       (0, 255, 255), (155, 155, 255))

        self.gg = width * height - mines
        self.ff = mines + 1
        self.open_bomb = False
        self.gl = False
        self.hf = 1
        self.left = 10
        self.top = 10
        self.a = 0
        self.cell_size = 25
        self.root, self.zagalovok, self.timetxt, self.best_timetxt = 0, 0, 0, 0
        self.count, self.won, self.lose, self.procent, self.again, self.exit = 0, 0, 0, 0, 0, 0
        self.ticks = 0

    def board_fill(self):
        for i in range(self.height):
            for j in range(self.width):
                c = 0
                if not self.board[i][j].bomb():
                    if i != 0 and self.board[i - 1][j].bomb():
                        c += 1
                    if i != self.height - 1 and self.board[i + 1][j].bomb():
                        c += 1
                    if j != 0 and self.board[i][j - 1].bomb():
                        c += 1
                    if j != self.width - 1 and self.board[i][j + 1].bomb():
                        c += 1
                    if i != 0 and j != 0:
                        if self.board[i - 1][j - 1].bomb():
                            c += 1
                    if i != 0 and j != self.width - 1:
                        if self.board[i - 1][j + 1].bomb():
                            c += 1
                    if i != self.height - 1 and j != 0:
                        if self.board[i + 1][j - 1].bomb():
                            c += 1
                    if i != self.height - 1 and j != self.width - 1:
                        if self.board[i + 1][j + 1].bomb():
                            c += 1
                    self.board[i][j].set_value(c)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_gl(self, pos):
        if self.ticks == 0:
            self.start_time = time.time()
        self.ticks += 1
        if self.get_cell(pos) is not None:
            xx, yy = self.get_cell(pos)
            self.gl = True
            if self.hf == 1:
                for _ in range(self.mines):
                    x, y = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
                    b = 0
                    while b == 0:
                        if x != xx and y != yy and not self.board[x][y].is_b:
                            self.board[x][y].set_bomb()
                            self.board[x][y].set_open()
                            b = 1
                        else:
                            x, y = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
                    self.board_fill()
                    self.hf = 10

    def flag(self, pos):
        if self.get_cell(pos) is not None and self.ff > 0:
            i, j = self.get_cell(pos)
            if not self.board[i][j].open() or self.board[i][j].bomb():
                self.board[i][j].set_flag()
                if self.board[i][j].get_flag():
                    self.ff -= 1
                else:
                    self.ff += 1
        if self.get_cell(pos) is not None:
            i, j = self.get_cell(pos)
            if not self.board[i][j].open() or self.board[i][j].bomb():
                if self.ff == 0 and self.board[i][j].get_flag():
                    self.board[i][j].set_flag()
                    self.ff += 1

    def restart(self):
        self.root.destroy()
        b = Minesweeper(10, 15, 15)
        b.tkinit()
        scr = pygame.display.set_mode((270, 430))
        pygame.display.set_caption('Minesweeper')
        glu = False
        while True:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evnt.type == pygame.MOUSEBUTTONDOWN:
                    if evnt.button == 1:
                        glu = True
                        b.set_gl(evnt.pos)
                        b.get_click(evnt.pos)
                    if evnt.button == 3:
                        b.flag(evnt.pos)
            scr.fill((15, 15, 30))
            b.render(scr)
            pygame.display.flip()

    def render(self, scr):
        global stat
        if self.a != self.mines:
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j].bomb() and self.gl:
                        pygame.draw.rect(scr, (255, 255, 255), (j * self.cell_size + self.left,
                                                                i * self.cell_size + self.top,
                                                                self.cell_size, self.cell_size), 1)
                    if self.board[i][j].bomb() and not self.gl:
                        pygame.draw.rect(scr, (255, 255, 255), (j * self.cell_size + self.left,
                                                                i * self.cell_size + self.top,
                                                                self.cell_size, self.cell_size), 1)
                    if self.board[i][j].bomb() and self.open_bomb:
                        pygame.draw.rect(scr, (random.choice(self.colors)), (j * self.cell_size
                                                                             + self.left,
                                                                             i * self.cell_size
                                                                             + self.top,
                                                                             self.cell_size,
                                                                             self.cell_size), 7)
                        self.a += 1
                        self.board[i][j].set_bomb()
                    if self.board[i][j].get_flag():
                        pygame.draw.rect(scr, (25, 25, 20), (j * self.cell_size + self.left,
                                                             i * self.cell_size + self.top,
                                                             self.cell_size, self.cell_size), 0)
                        big_f = pygame.image.load(
                            'flag5.png').convert_alpha()
                        screen.blit(big_f, (j * self.cell_size + self.left + 1, i * self.cell_size + self.top + 1))
                    if not self.board[i][j].bomb():
                        pygame.draw.rect(scr, (255, 255, 255), (j * self.cell_size + self.left,
                                                                i * self.cell_size + self.top,
                                                                self.cell_size, self.cell_size), 1)
                    if self.board[i][j].bomb() and self.board[i][j].get_flag():
                        pygame.draw.rect(scr, (255, 255, 255), (j * self.cell_size + self.left,
                                                                i * self.cell_size + self.top,
                                                                self.cell_size, self.cell_size), 1)
                    if self.board[i][j].open():
                        if not self.board[i][j].bomb() and not self.board[i][j].get_flag():
                            pygame.draw.rect(scr, (43, 43, 68), (j * self.cell_size + self.left,
                                                                 i * self.cell_size + self.top,
                                                                 self.cell_size, self.cell_size), 0)
                            pygame.font.init()
                            font = pygame.font.Font(None, 25)
                            value = self.board[i][j].get_value()
                            if value == 1:
                                text = font.render(str(value), True, (19, 168, 253))
                            elif value == 2:
                                text = font.render(str(value), True, (52, 190, 55))
                            elif value == 3:
                                text = font.render(str(value), True, (237, 13, 26))
                            elif value == 4:
                                text = font.render(str(value), True, (238, 64, 252))
                            elif value == 5:
                                text = font.render(str(value), True, (130, 3, 15))
                            elif value == 0:
                                text = font.render(str(value), True, (83, 83, 113))
                            else:
                                text = font.render(str(value), True, (100, 255, 100))
                            text_x = j * self.cell_size + self.left + 3
                            text_y = i * self.cell_size + self.top + 2
                            screen.blit(text, (text_x, text_y))

                    if self.gg == 0:
                        end_time = time.time() - self.start_time
                        stat[0] += 1
                        stat[3] += 1
                        stat[4] = end_time

                        if stat[5] == 0:
                            stat[5] = end_time
                        elif stat[4] < stat[5]:
                            stat[5] = end_time

                        stat[2] = stat[0]/stat[3]

                        self.zagalovok.config(text="         Вы Победильник!         ")
                        self.timetxt.config(text=f"Время: {int(stat[4])} сек")
                        self.best_timetxt.config(text=f"Лучшее время: {int(stat[5])} сек")
                        self.count.config(text=f"Проведяно игр: {stat[3]}")
                        self.won.config(text=f"Выиграно игр: {stat[0]}")
                        self.lose.config(text=f"Проиграно игр: {stat[1]}")
                        self.procent.config(text=f"Процент побед: {int(stat[2]*100)}%")
                        self.root.eval('tk::PlaceWindow . center')
                        self.root.mainloop()
                        self.gg += 10
                pos = pygame.mouse.get_pos()
                cell = self.get_cell(pos)
                if cell is not None:
                    try:
                        if not self.board[cell[0]][cell[1]].open() or self.board[cell[0]][cell[1]].bomb():
                            if not self.board[cell[0]][cell[1]].get_flag():
                                pygame.draw.rect(scr, (45, 44, 100), (cell[1] * self.cell_size + self.left + 1,
                                                                      cell[0] * self.cell_size + self.top + 1,
                                                                      self.cell_size - 2, self.cell_size - 2), 0)
                    except:
                        pass
                pygame.font.init()
                font = pygame.font.Font(None, 24)
                text = font.render('Количество бомб: ' + str(self.ff - 1), True, (61, 137, 198))
                screen.blit(text, (10, 399))
        else:
            end_time = time.time() - self.start_time
            stat[1] += 1
            stat[3] += 1
            stat[4] = int(end_time)

            if stat[0] != 0:
                stat[2] = stat[0]/stat[3]

            self.zagalovok.config(text="К сожалению вы проиграли...")
            self.timetxt.config(text=f"Время: {int(stat[4])} сек")
            self.best_timetxt.config(text=f"Лучшее время: {int(stat[5])} сек")
            self.count.config(text=f"Проведяно игр: {stat[3]}")
            self.won.config(text=f"Выиграно игр: {stat[0]}")
            self.lose.config(text=f"Проиграно игр: {stat[1]}")
            self.procent.config(text=f"Процент побед: {int(stat[2]*100)}%")

            self.root.eval('tk::PlaceWindow . center')
            self.root.mainloop()
            self.gg += 10

    def get_cell(self, pos):
        if pos is not None:
            x, y = pos
            x -= self.left
            y -= self.top
            if 0 <= x <= self.cell_size * self.width and 0 <= y <= self.cell_size * self.height:
                return y // self.cell_size, x // self.cell_size

    def open_empty_cells(self, cell):
        i, j = cell
        self.gg -= 1
        self.board[i][j].set_open()
        self.was_in_cell[i][j] = True
        if self.board[i][j].value != 0:
            return None
        if i != 0:
            if not self.was_in_cell[i - 1][j]:
                self.open_empty_cells((i - 1, j))
        if i != self.height - 1:
            if not self.was_in_cell[i + 1][j]:
                self.open_empty_cells((i + 1, j))
        if j != 0:
            if not self.was_in_cell[i][j - 1]:
                self.open_empty_cells((i, j - 1))
        if j != self.width - 1:
            if not self.was_in_cell[i][j + 1]:
                self.open_empty_cells((i, j + 1))
        if i != 0 and j != 0:
            if not self.was_in_cell[i - 1][j - 1]:
                self.open_empty_cells((i - 1, j - 1))
        if i != 0 and j != self.width - 1:
            if not self.was_in_cell[i - 1][j + 1]:
                self.open_empty_cells((i - 1, j + 1))
        if i != self.height - 1 and j != 0:
            if not self.was_in_cell[i + 1][j - 1]:
                self.open_empty_cells((i + 1, j - 1))
        if i != self.height - 1 and j != self.width - 1:
            if not self.was_in_cell[i + 1][j + 1]:
                self.open_empty_cells((i + 1, j + 1))

    def on_click(self, cell):
        if cell is not None:
            x, y = cell
            if not self.board[x][y].get_flag():
                if not self.board[x][y].open():
                    self.gg -= 1
                self.board[x][y].set_open()
                self.was_in_cell[x][y] = True
                if self.board[x][y].get_value() == 0 and not self.board[x][y].bomb():
                    self.open_empty_cells(cell)
                    self.gg += 1
                if self.board[x][y].bomb():
                    self.open_bomb = True

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def tkinit(self):
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.title('Игра закончена')
        self.root.protocol("WM_DELETE_WINDOW", lambda x=0: exit())

        self.zagalovok = tk.Label(text="Квантовая суперпозиция")
        self.zagalovok.grid(row=0, column=0, columnspan=3, padx=90, pady=10)

        self.timetxt = tk.Label(text="Время: 0 сек")
        self.timetxt.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.best_timetxt = tk.Label(text="Лучшее время: 0 сек")
        self.best_timetxt.grid(row=1, column=2, sticky="e", padx=10, pady=15)

        self.count = tk.Label(text="Проведяно игр: 0")
        self.count.grid(row=2, column=0, sticky="w", padx=10)

        self.won = tk.Label(text="Выиграно игр: 0")
        self.won.grid(row=3, column=0, sticky="w", padx=10)

        self.lose = tk.Label(text="Проиграно игр: 0")
        self.lose.grid(row=4, column=0, sticky="w", padx=10)

        self.procent = tk.Label(text="Процент побед: 0%")
        self.procent.grid(row=4, column=2, sticky="e", padx=10)

        self.again = tk.Button(text="Играть снова", command=self.restart, padx=20)
        self.again.grid(row=5, column=0, padx=10, pady=10)

        self.exit = tk.Button(text="Выход", command=lambda: exit(), padx=40)
        self.exit.grid(row=5, column=2, padx=10, pady=10)


if __name__ == "__main__":
    board = Minesweeper(10, 15, 15)
    board.tkinit()
    running = True
    screen = pygame.display.set_mode((270, 430))
    pygame.display.set_caption('Minesweeper')
    gl = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gl = True
                    board.set_gl(event.pos)
                    board.get_click(event.pos)
                if event.button == 3:
                    board.flag(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    board.draw_rect(event.pos)
        screen.fill((15, 15, 30))
        board.render(screen)
        pygame.display.flip()
