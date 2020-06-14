import pygame
import random
import tkinter
from tkinter import messagebox
import json
import itertools
from datetime import datetime

pygame.init()
root = tkinter.Tk()
root.withdraw()

width = 300
height = 300
# if you want to make the height value and the width value different make sure that
# the width height w_rows and h_rows are proportional
# example if width = 600 and height = 1200
# then w_rows = 60 and h_rows = 30
w_rows = 6
h_rows = 6
len_between_height = height // h_rows
len_between_width = width // w_rows

# put win = pygame.display.set_mode((width, height)) down in the program so we get the cycle first and then display the game
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

with open('C:\\Users\\kabba\\PythonProjects\\python project\\pygame\\snake\\highscore.json', 'r') as f:
    high_score = json.load(f)

# get previously calculated hamiltonian cycles so we don't have to calculate them again
with open('C:\\Users\\kabba\\PythonProjects\\python project\\pygame\\snake\\snake ai\\hamilton cycles.json', 'r') as f:
    hamiltonian_dict = json.load(f)


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
            pygame.draw.rect(surface, color, (
                self.pos[0] * len_between_width + 1, self.pos[1] * len_between_height + 1, len_between_width - 1,
                len_between_height - 1))
        else:
            pygame.draw.rect(surface, self.color, (
                self.pos[0] * len_between_width + 1, self.pos[1] * len_between_height + 1, len_between_width - 1,
                len_between_height - 1))


class Snake:

    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 0
        self.pos = pos
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def move(self):
        if self.right and self.dir_x != -1:
            self.dir_x = 1
            self.dir_y = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            self.right = False

        elif self.left and self.dir_x != 1:
            self.dir_x = -1
            self.dir_y = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            self.left = False

        elif self.up and self.dir_y != 1:
            self.dir_y = -1
            self.dir_x = 0
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            self.up = False

        elif self.down and self.dir_y != -1:
            self.dir_x = 0
            self.dir_y = 1
            self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            self.down = False

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
        self.dir_x = 0
        self.dir_y = 0

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

    # --------------------------------------------------------- #
    #    for n, c in num_coordinates.items():
    #        str_num = str(n)
    #        coordinates = (
    #            c[0] * len_between_width + 1, c[1] * len_between_height + 1, len_between_width - 1,
    #            len_between_height - 1)
    #
    #        font = pygame.font.SysFont('comicsans', 50 - len(str_num) * 10)
    #        text = font.render(str_num, True, (255, 0, 255))
    #        win.blit(text, coordinates)
    # --------------------------------------------------------- #

    s.draw(win)
    snack.draw(win)
    pygame.display.update()


def hamilton(g, pt, path=None):
    if path is None:
        path = []
    size = len(g)
    if pt not in set(path):
        path.append(pt)
        if len(path) == size:
            return path
        for pt_next in g.get(pt, []):
            res_path = [i for i in path]
            candidate = hamilton(g, pt_next, res_path)
            if candidate is not None:
                return candidate


start_time = datetime.now()
run = True
score = 0
s = Snake((255, 0, 0), (w_rows // 2, h_rows // 2))
snack = Cube(random_snack(), color=(0, 255, 0))

# only graphs with an odd number of vertices have a hamilton cycle
if w_rows * h_rows % 2 == 0:

    # if hamilton path already calculated grab it
    if f'{w_rows}, {h_rows}' in hamiltonian_dict.keys():
        cycled_commands = itertools.cycle(hamiltonian_dict[f'{w_rows}, {h_rows}'])
        print('found hamilton cycle in file. No need to calculate')

    else:
        # ------------------Calculate Hamiltonian path------------------ #
        num = 0
        x_list = []
        y_list = []
        num_coordinates = {}
        flipped_num_coordinates = {}
        neighbours = {}

        for y in range(h_rows):
            for x in range(w_rows):
                y_list.append(y)
                x_list.append(x)
                num_coordinates[num] = (x, y)
                flipped_num_coordinates[(x, y)] = num
                num += 1

        # ANGELS
        neighbours[0] = (w_rows, 1)
        neighbours[w_rows - 1] = (w_rows - 2, w_rows * 2 - 1)
        neighbours[w_rows * (h_rows - 1)] = (h_rows * w_rows - w_rows + 1, w_rows * (h_rows - 1) - w_rows)
        neighbours[h_rows * w_rows - 1] = (h_rows * w_rows - 2, h_rows * w_rows - w_rows - 1)

        # SIDES
        for n, c in num_coordinates.items():
            # exclude sides
            if c[1] != 0 and c[1] != h_rows - 1:
                # exclude interior
                if c[0] == 0:
                    neighbours[n] = (n + 1, n - w_rows, n + w_rows)
                elif c[0] == w_rows - 1:
                    neighbours[n] = (n - 1, n + w_rows, n - w_rows)
            # top sides
            elif c[1] == h_rows - 1:
                if c[0] != 0 and c[0] != w_rows - 1:
                    neighbours[n] = (n - 1, n + 1, n - w_rows)
            elif c[1] == 0:
                if c[0] != 0 and c[0] != w_rows - 1:
                    neighbours[n] = (n - 1, n + 1, n + w_rows)

        # MIDDLE TILES
        for n, c in num_coordinates.items():
            if c[0] != 0 and c[0] != w_rows - 1 and c[1] != h_rows - 1 and c[1] != 0:
                neighbours[n] = (n + 1, n - 1, n + w_rows, n - w_rows)

        # print values
        print(f'\n\nneighbours are {neighbours}\n\n')
        for k, v in num_coordinates.items():
            if k in neighbours.keys():
                for k2, v2 in neighbours.items():
                    if k == k2:
                        print(f'{k} coords --> {v} <<>> neighbours --> {v2}')
            else:
                print(f'{k} --> {v}')

        # create and check if hamilton path is correct or not
        starting_point = 0
        h_path = hamilton(neighbours, starting_point)
        good_hamilton = False
        if h_path[-1] not in neighbours[starting_point]:
            while not good_hamilton:
                starting_point += 1
                h_path = hamilton(neighbours, starting_point)
                if h_path is None:
                    print('no path')
                    break
                else:
                    if h_path[-1] in neighbours[starting_point]:
                        good_hamilton = True
                        break

        # organize the hamilton cycle so it starts at the pos of the snake
        if h_path[0] != flipped_num_coordinates[s.pos]:
            snake_starting_index = h_path.index(flipped_num_coordinates[s.pos])
            lst_to_move = h_path[:snake_starting_index]
            del h_path[:snake_starting_index]
            h_path = h_path + lst_to_move
            h_path.append(flipped_num_coordinates[s.pos])
        print(f'\nthe hamiltonian path is {h_path}')

        # create commands to move the snake
        commands = []
        for c, i in enumerate(h_path):
            if c != len(h_path) - 1:
                next_num = h_path[c + 1]

                if next_num - i == 1:
                    commands.append('r')
                elif next_num - i == - 1:
                    commands.append('l')
                elif next_num > i:
                    commands.append('d')
                elif next_num < i:
                    commands.append('u')
        print(commands)
        cycled_commands = itertools.cycle(commands)

        # add hamilton cycle to file so we don't have to calculate it next time
        str_rows = f'{w_rows}, {h_rows}'
        hamiltonian_dict[str_rows] = commands
        with open('C:\\Users\\kabba\\PythonProjects\\python project\\pygame\\snake\\snake ai\\hamilton cycles.json',
                  'w') as f:
            json.dump(hamiltonian_dict, f)

        # ------------------Calculated Hamiltonian path------------------ #

    print(f'time spent {datetime.now() - start_time}')
    win = pygame.display.set_mode((width, height))
    messagebox.showinfo('done calculating', 'press ok to continue')

    while run:
        clock.tick(9)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # ------------------------------- #
        c = next(cycled_commands)
        if c == 'r':
            s.right = True
        elif c == 'l':
            s.left = True
        elif c == 'u':
            s.up = True
        elif c == 'd':
            s.down = True
        # ------------------------------- #

        s.move()

        # check collision with snack
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(), color=(0, 255, 0))
            score += 1
            if score > high_score:
                high_score = score
                with open('C:\\Users\\kabba\\PythonProjects\\python project\\pygame\\snake\\highscore.json', 'w') as f:
                    json.dump(high_score, f)

        redraw_window()

    pygame.quit()

else:
    print('no hamilton path found')