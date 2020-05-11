import pygame
import random

pygame.init()

width = 500
height = 500
rows = 20
len_between = width // rows

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


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
            color = tuple(abs(c - 50) for c in self.color)
            pygame.draw.rect(surface, color, (self.pos[0] * len_between + 1, self.pos[1] * len_between + 1, len_between - 1, len_between - 1))
        else:
            pygame.draw.rect(surface, self.color, (self.pos[0] * len_between + 1, self.pos[1] * len_between + 1, len_between - 1, len_between - 1))


class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 0

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

        # check collision with walls
        if self.head.pos[0] < 0:
            lose()
        elif self.head.pos[0] > rows - 1:
            lose()
        elif self.head.pos[1] < 0:
            lose()
        elif self.head.pos[1] > rows - 1:
            lose()

    def reset(self):
        pass

    def add_cube(self):
        tail = self.body[-1]
        dir_x = tail.dir_x
        dir_y = tail.dir_y

        if dir_x == 1 and dir_y == 0:
            self.body.append(Cube(tail.pos[0] - 1, tail.pos[1]))
        elif dir_x == -1 and dir_y == 0:
            self.body.append(Cube(tail.pos[0] + 1, tail.pos[1]))
        elif dir_y == 1 and dir_x == 0:
            self.body.append(Cube(tail.pos[0], tail.pos[1] - 1))
        elif dir_x == -1 and dir_x == 0:
            self.body.append(Cube(tail.pos[0], tail.pos[1] + 1))

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
    for i in range(rows):
        x += len_between
        y += len_between
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))
        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, height))


def random_snack():
    positions = s.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
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
    print(random.random())
    print()


def redraw_window():
    win.fill((0, 0, 0))
    draw_grid()
    s.draw(win)
    snack.draw(win)
    pygame.display.update()


run = True
s = Snake((255, 0, 0), (rows // 2, rows // 2))
snack = Cube(random_snack(), color=(0, 255, 0))

while run:
    pygame.time.delay(50)
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    s.move()
    if s.body[0].pos == snack.pos:
        s.add_cube()
        snack = Cube(random_snack(), color=(0, 255, 0))

    redraw_window()

pygame.quit()
