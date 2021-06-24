class WorldGrid:
    active_cells = 0  # records the number of active cells on the grid
    access_times = 0  # number of times the grid is called
    empty_list = []

    def __init__(self, size_x: int, size_y: int):
        assert size_x > 2 and size_y > 2

        self._x = size_x
        self._y = size_y
        self._live_list = []  # holds the list of cells for rendering
        self.world_grid = {}  # holds all cells
        self.none_cells = []

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def print_grid(self):
        """Prints the grid to output"""
        self.active_cells = 0
        # for y in self.world_grid:
        for y in range(self._y):
            print("|", end="")
            # for x in self.world_grid[y]:
            for x in range(self._x):
                # if self.world_grid[y][x]:
                if self.get_matrix_val(x, y):
                    self.active_cells += 1
                    print(chr(9646), end="|")
                else:
                    print(chr(9647), end="|")
            print()
        print()

        self.access_times += 1

    def live_list(self):
        return self._live_list

    def get_dimensions(self):
        return self._x, self._y

    def switch_cell(self, x: int, y: int):
        """Flips a cells living state"""
        if self.get_matrix_val(x, y):
            self.put_matrix_val(x, y, None)
        else:
            self.put_matrix_val(x, y, 1)

    def next_stage(self):
        """
        Gathers cells information and then modifies all the cells in an instance
        """
        change_list = {}  # records the cells that will change on the world grid

        def update(index, a_list, live_cell: bool):

            # If a cell has already been recorded skip
            if index in a_list:
                return

            # Get the calculated xy position of the cell on the world grid,
            # which is based on the index/hash value
            x, y = self.xy_from_index(index)

            if live_cell:
                empty = False
            else:
                empty = True

            # Count the neighbours of a cell 
            cell, count, empty_list = self._neighbour_count(
                x, y,
                empty_cell=empty
            )

            # - cell,  contains the last count of neighbours or None
            # - count, the up-to-date neighbour count
            # - empty_list, a list of any empty cells.

            # - Note: an empty cell is that which holds a position directly
            # - adjacent to a living one.

            # GoL Rules are as follows
            # an empty cell surrounded 3 living - empty cell comes alive 
            if not cell and count == 3:
                a_list[index] = (x, y, 3)

            # 2 or 3 neighbours - cell remains alive 
            elif cell and count == 2 or count == 3:
                a_list[index] = (x, y, count)

                # in all other cases - the cell will die
            else:
                a_list[index] = (x, y, None)

            # If there are empty cells in the list
            if empty_list:
                # check each to see if they have neighbours
                for x in empty_list:
                    update(x, a_list, False)

        # For any living cell registered on the world grid, update that cell
        for i in self.world_grid.keys():
            update(i, change_list, True)

        self._live_list = []

        for change in change_list.values():
            self.put_matrix_val(change[0], change[1], change[2])
            if change[2]:
                self._live_list.append((change[0], change[1], change[2]))
            else:
                self.delete_matrix_val(change[0], change[1])

    def _gather_cells(self, i):
        pass

    def _neighbour_count(self, pos_x: int, pos_y: int, empty_cell=False):
        """Counts the living neighbours around a given cell"""
        self.empty_list = []
        value = self.get_matrix_val(pos_x, pos_y)

        count = self._get_neighbour(pos_x - 1, pos_y - 1, empty_cell)
        count += self._get_neighbour(pos_x, pos_y - 1, empty_cell)
        count += self._get_neighbour(pos_x + 1, pos_y - 1, empty_cell)

        count += self._get_neighbour(pos_x - 1, pos_y, empty_cell)
        count += self._get_neighbour(pos_x + 1, pos_y, empty_cell)

        count += self._get_neighbour(pos_x - 1, pos_y + 1, empty_cell)
        count += self._get_neighbour(pos_x, pos_y + 1, empty_cell)
        count += self._get_neighbour(pos_x + 1, pos_y + 1, empty_cell)

        return value, count, self.empty_list

    def _get_neighbour(self, x, y, from_empty: bool):

        if self.get_matrix_val(x, y):
            return 1
        else:
            if not from_empty:
                key = (self._x * (y + 1)) - (self._x - (x + 1) + 1)
                self.empty_list.append(key)
            return 0

    def get_matrix_val(self, x_coord, y_coord):
        """
        try:
            assert x_coord >= 0 and x_coord < self._x
            assert y_coord >= 0 and y_coord < self._y
        except AssertionError:
            return None
            #raise IndexError(f'{x_coord}, {y_coord}')
        """
        index = self._i_from_xy(x_coord, y_coord)
        return self.world_grid.get(index, None)

    def _i_from_xy(self, x_coord, y_coord):
        return (self._x * (y_coord + 1)) - (self._x - (x_coord + 1) + 1)

    def put_matrix_val(self, x_coord, y_coord, value):
        try:
            assert 0 <= x_coord < self._x
            assert 0 <= y_coord < self._y
        except AssertionError:
            pass
            # raise IndexError()

        self.world_grid[
            (self._x * (y_coord + 1)) - (self._x - (x_coord + 1) + 1)] = value

    def delete_matrix_val(self, x_coord, y_coord):
        """
        try:
            assert x_coord >= 0 and x_coord < self._x
            assert y_coord >= 0 and y_coord < self._y
        except AssertionError:

            raise IndexError()
        """
        del self.world_grid[
            (self._x * (y_coord + 1)) - (self._x - (x_coord + 1) + 1)]

    def xy_from_index(self, i):
        y, x = divmod(i, self._x)
        if y == 0:
            x = i
        return x, y
