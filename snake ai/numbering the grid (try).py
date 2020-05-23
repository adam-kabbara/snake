import pygame

pygame.init()
width = 600
height = 600
w_rows = 6
h_rows = 6
len_between_height = height // h_rows
len_between_width = width // w_rows

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


def draw_grid():
    x = 0
    y = 0
    for i in range(h_rows):
        y += len_between_height
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))
    for i in range(w_rows):
        x += len_between_width
        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, height))


def redraw_window():
    win.fill((0, 0, 0))

    # --------------------------------------------------------- #
    for n, c in num_coordinates.items():
        str_num = str(n)
        coordinates = (
            c[0] * len_between_width + 1, c[1] * len_between_height + 1, len_between_width - 1,
            len_between_height - 1)

        font = pygame.font.SysFont('comicsans', 50 - len(str_num) * 10)
        text = font.render(str_num, True, (255, 0, 255))
        win.blit(text, coordinates)
    # --------------------------------------------------------- #

    draw_grid()
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


num = 0
x_list = []
y_list = []
num_coordinates = {}
neighbours = {}

for y in range(h_rows):
    for x in range(w_rows):
        y_list.append(y)
        x_list.append(x)
        num_coordinates[num] = (x, y)
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
for k, v in num_coordinates.items():
    if k in neighbours.keys():
        for k2, v2 in neighbours.items():
            if k == k2:
                print(f'{k} coords --> {v} <<>> neighbours --> {v2}')
    else:
        print(f'{k} --> {v}')

print(f'the hamiltonian path is {hamilton(neighbours, 0)}')
#print(neighbours)

run = True
while run:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redraw_window()
    p = False

pygame.quit()
