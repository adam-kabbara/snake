import pygame
import random
import tkinter
from tkinter import messagebox
import json

pygame.init()
root = tkinter.Tk()
root.withdraw()

width = 600
height = 600
w_rows = 60
h_rows = 60
len_between_height = height // h_rows
len_between_width = width // w_rows

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

with open('highscore.json', 'r') as f:
    high_score = json.load(f)


class Cube:
    def __init__(self, pos, color=(255, 0, 0)):
        self.pos = pos
        self.dir_x = 0
        self.dir_y = 0
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, first_cube=False):

        if first_cube:
            color = (255, 150, 150)
            pygame.draw.rect(surface, color, (self.pos[0] * len_between_width + 1, self.pos[1] * len_between_height + 1, len_between_width - 1, len_between_height - 1))
        else:
            pygame.draw.rect(surface, self.color, (self.pos[0] * len_between_width + 1, self.pos[1] * len_between_height + 1, len_between_width - 1, len_between_height - 1))


class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 0
        self.pos = pos

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.dir_x != -1:
            self.dir_x = 1
            self.dir_y = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        elif keys[pygame.K_LEFT] and self.dir_x != 1:
            self.dir_x = -1
            self.dir_y = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        elif keys[pygame.K_UP] and self.dir_y != 1:
            self.dir_y = -1
            self.dir_x = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        elif keys[pygame.K_DOWN] and self.dir_y != -1:
            self.dir_x = 0
            self.dir_y = 1
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        for cube in self.body:
            p = cube.pos[:]
            if p in self.turns.keys():
                turn = self.turns[p]
                cube.move(turn[0], turn[1])

                if self.body.index(cube) == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                cube.move(cube.dir_x, cube.dir_y)

        # check collision
        body_copy = self.body[:]
        body_copy.pop(0)
        snake_positions = [cube.pos for cube in body_copy]
        if self.head.pos[0] < 0:
            lose()
        elif self.head.pos[0] > w_rows - 1:
            lose()
        elif self.head.pos[1] < 0:
            lose()
        elif self.head.pos[1] > h_rows - 1:
            lose()
        elif self.body[0].pos in snake_positions:
            lose()

    def reset(self):
        self.body = []
        self.head = Cube(self.pos)
        self.body.append(self.head)
        self.turns = {}

    def add_cube(self):
        tail = self.body[-1]
        dir_x = tail.dir_x
        dir_y = tail.dir_y

        if dir_x == 1 and dir_y == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dir_x == -1 and dir_y == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dir_y == 1 and dir_x == 0:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dir_y == -1 and dir_x == 0:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dir_x
        self.body[-1].dir_y = dir_y

    def draw(self, surface):
        for cube in self.body:
            if self.body.index(cube) == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


def draw_grid():
    x = 0
    y = 0
    for i in range(h_rows):
        y += len_between_height
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))
    for i in range(w_rows):
        x += len_between_width
        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, height))


def random_snack():
    positions = s.body
    while True:
        x = random.randrange(w_rows)
        y = random.randrange(h_rows)
        lst = []
        for c in positions:
            if c.pos == (x, y):
                lst.append(False)
            else:
                lst.append(True)
        if all(lst):
            break
        else:
            continue
    return x, y


def lose():
    global run, score
    again = messagebox.askyesno('Game over', 'Do you want to play again')
    if again:
        s.reset()
        score = 0
        # we do this so the pygame window will be refocused on
        pygame.display.set_mode((width, height))
    else:
        run = False


def redraw_window():
    win.fill((0, 0, 0))
    draw_grid()

    # draw score and high score
    score_font = pygame.font.SysFont('comicsans', 25)
    text = score_font.render(f'SCORE {score}', True, (200, 200, 100))
    win.blit(text, (0, height - 20))
    high_score_font = pygame.font.SysFont('comicsans', 25)
    text = high_score_font.render(f'HIGH SCORE {high_score}', True, (200, 200, 100))
    win.blit(text, (width - 125 - len(str(high_score)) * 7, height - 20))

    s.draw(win)
    snack.draw(win)
    pygame.display.update()


run = True
score = 0
s = Snake((255, 0, 0), (w_rows // 2, h_rows // 2))
snack = Cube(random_snack(), color=(0, 255, 0))

while run:
    clock.tick(9.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    s.move()

    # check collision with snack
    if s.body[0].pos == snack.pos:
        s.add_cube()
        snack = Cube(random_snack(), color=(0, 255, 0))
        score += 1
        if score > high_score:
            high_score = score
            with open('highscore.json', 'w') as f:
                json.dump(high_score, f)

    redraw_window()

pygame.quit()
