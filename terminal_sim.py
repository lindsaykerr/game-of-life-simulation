from objects.world import WorldGrid
import time
import random

""" Prints simulation to standard output """

# State the size of the grid
x_size = 20
y_size = 20

grid = WorldGrid(x_size, y_size)

# Generate random living cells
for x in range(200):
    random.seed()
    randx = random.randrange(0, x_size)
    randy = random.randrange(0, y_size)
    grid.switch_cell(randx, randy)

grid.print_grid()

counter = 0

while grid.active_cells > 0 and counter < 100:
    grid.next_stage()
    grid.print_grid()
    counter += 1
    time.sleep(.75)

# print(grid.get_grid())
print("Levels", grid.access_times)
