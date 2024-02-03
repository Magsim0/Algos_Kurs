import pygame
import pygame_menu
import numpy as np


def handle_events(menu, sandpile):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu.enable()
                menu.reset(1)
                menu.mainloop(pygame.display.set_mode((300, 300)))


class Sandpile:
    def __init__(self, rows, cols, sands, max_sand):
        self.max_grains = max_sand
        self.rows = rows
        self.sands = sands
        self.cols = cols
        self.grid = np.zeros((cols, rows), int)
        self.grid[rows // 2, cols // 2] = sands
        self.cell_size = 5
        self.width, self.height = cols * self.cell_size, rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sandpile Visualization")

        self.color_map = {0: (0, 0, 0), 1: (139, 216, 240), 2: (240, 139, 139), 3: (213, 139, 240),
                          4: (250, 173, 117), sands: (255, 0, 255)}

    def fall(self, elem_x, elem_y):
        p = self.grid[elem_x, elem_y]
        b = p // self.max_grains
        o = p % self.max_grains
        self.grid[elem_x, elem_y] = o

        self.grid[elem_x - 1, elem_y] += b
        self.grid[elem_x + 1, elem_y] += b
        self.grid[elem_x, elem_y - 1] += b
        self.grid[elem_x, elem_y + 1] += b


        self.grid[0] = self.grid[-1] = 0
        self.grid[:, 0] = self.grid[:, -1] = 0

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                color = self.color_map.get(self.grid[i, j], (0, 0, 0))
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

        pygame.display.flip()

    def run(self, menu):
        clock = pygame.time.Clock()
        running = True
        while running:
            handle_events(menu, self)
            if np.max(self.grid) >= self.max_grains:
                elem_x, elem_y = np.where(self.grid >= self.max_grains)
                self.fall(elem_x, elem_y)
                self.update_screen()
                pygame.time.delay(1)

            clock.tick(360)


class SecondSandpile(Sandpile):
    def __init__(self, rows, cols, sands, max_sand):
        super().__init__(rows, cols, sands, max_sand)

    def fall(self, elem_x, elem_y):
        p = self.grid[elem_x, elem_y]
        b = p // self.max_grains
        o = p % self.max_grains
        self.grid[elem_x, elem_y] = o

        self.grid[elem_x - 1, elem_y+1] += b
        self.grid[elem_x + 1, elem_y+1] += b
        self.grid[elem_x - 1, elem_y-1] += b
        self.grid[elem_x + 1, elem_y-1] += b
        self.grid[0] = self.grid[-1] = 0
        self.grid[:, 0] = self.grid[:, -1] = 0

class ThirdSandpile(Sandpile):
    def __init__(self, rows, cols, sands, max_sand):
        super().__init__(rows, cols, sands, max_sand)

    def fall(self, elem_x, elem_y):
        p = self.grid[elem_x, elem_y]
        b = p // self.max_grains
        o = p % self.max_grains
        self.grid[elem_x, elem_y] = o

        if np.all(self.grid[elem_x - 1, elem_y - 1]) <1:
            self.grid[elem_x + 1, elem_y + 1] += b
        self.grid[elem_x + 1, elem_y - 1] += b
        if np.all(self.grid[elem_x + 1, elem_y - 1])<1:
            self.grid[elem_x + 1, elem_y - 1] += b
        self.grid[elem_x - 1, elem_y ] += b
        self.grid[elem_x + 1, elem_y ] += b
        self.grid[elem_x , elem_y - 1] += b
        self.grid[elem_x , elem_y - 1] += b


        self.grid[0] = self.grid[-1] = 0
        self.grid[:, 0] = self.grid[:, -1] = 0



def start_simulation(menu, userdata):
    simulation_type = userdata[0]
    rows = userdata[1]
    cols = userdata[2]
    sands = userdata[3]
    max_sand = userdata[4]

    sandpile = Sandpile(rows, cols, sands, max_sand)
    sandpile.run(menu)


def start_simulation2(menu, userdata):
    simulation_type = userdata[0]
    rows = userdata[1]
    cols = userdata[2]
    sands = userdata[3]
    max_sand = userdata[4]

    sandpile = SecondSandpile(rows, cols, sands, max_sand)
    sandpile.run(menu)


def start_simulation3(menu, userdata):
    simulation_type = userdata[0]
    rows = userdata[1]
    cols = userdata[2]
    sands = userdata[3]
    max_sand = userdata[4]

    sandpile = ThirdSandpile(rows, cols, sands, max_sand)
    sandpile.run(menu)


def create_menu():
    pygame.init()
    pygame.display.set_mode((400, 300))  # Set the display mode here

    menu = pygame_menu.Menu('Sandpile Simulation', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

    rows = 150
    cols = 150
    sands = 2 ** 15

    menu.add.button("Square grid", start_simulation, menu, ['Square grid', rows, cols, sands,4])
    menu.add.button("Rhomb grid", start_simulation2, menu, ['Rhomb grid', rows, cols, sands, 4])
    menu.add.button("Inclined plane", start_simulation3, menu, ['Inclined plane', rows, cols, sands, 6])
    return menu


menu = create_menu()
menu.mainloop(pygame.display.set_mode((400, 300)))



