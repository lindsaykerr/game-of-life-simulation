from typing import Set


class WorldGrid():

    active_cells = 0 # records the number of active cells on the grid
    access_times = 0 # number of times the grid is called
    empty_list = []

    def __init__(self, size_x: int, size_y:int):
        assert size_x > 2 and size_y > 2

        self._x = size_x
        self._y = size_y
        self._live_list = []
        self.world_grid = {}
        self.none_cells = []

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def print_grid(self):
        """Prints the grid to output"""
        self.active_cells = 0
        #for y in self.world_grid:
        for y in range(self._y):
            print("|", end="")
            #for x in self.world_grid[y]:
            for x in range(self._x):
                #if self.world_grid[y][x]:
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
        return (self._x, self._y)
        


    def switch_cell(self, x: int, y:int):
        """Flips a cells living state"""
        if self.get_matrix_val(x, y):
            self.put_matrix_val(x, y, None)
        else:
            self.put_matrix_val(x, y, 1)
                

    def next_stage(self):
        """Gathers cells information and then modifies all the cells in an instance"""
        change_list = {}
        
        def update(i, change_list, livecell: bool):
            if i in change_list:
                return
        
            x, y = self.xy_from_index(i)
            # returns
            if livecell:
                empty = False
            else:
                empty = True
            
            cell, count, emptyList = self._neighbour_count(x, y, empty_cell=empty)

            if not cell and count == 3:
                change_list[i] = (x, y, 3)
            elif cell and count == 2 or count == 3:
                change_list[i] = (x, y, count) 
            
            # in all other cases the cell will die
            else:
                change_list[i] = (x, y, None)

            if emptyList:
                for x in emptyList:
                    update(x, change_list, False)


        for i in self.world_grid.keys():
            update(i, change_list, True)

            
                
        self._live_list = []
        for change in change_list.values():
            #self.world_grid[change[1]][change[0]] = change[2]
            self.put_matrix_val(change[0],change[1], change[2])
            
            if change[2]:
                self._live_list.append((change[0], change[1], change[2]))
            else:
               self.delete_matrix_val(change[0], change[1])

    def _gather_cells(self, i): 
        pass

    def _neighbour_count(self, pos_x: int, pos_y: int, empty_cell=False):
        '''Counts the living neighbours around a given cell'''
        count = 0
        self.empty_list = []
        value = self.get_matrix_val(pos_x, pos_y)

        count = self._get_neighbour(pos_x-1, pos_y-1, empty_cell)
        count += self._get_neighbour(pos_x, pos_y-1, empty_cell)
        count += self._get_neighbour(pos_x+1, pos_y-1, empty_cell)

        count += self._get_neighbour(pos_x-1, pos_y, empty_cell)
        count += self._get_neighbour(pos_x+1, pos_y, empty_cell)

        count += self._get_neighbour(pos_x-1, pos_y+1, empty_cell)
        count += self._get_neighbour(pos_x, pos_y+1, empty_cell)
        count += self._get_neighbour(pos_x+1, pos_y+1, empty_cell)

        return value, count, self.empty_list

    def _get_neighbour(self, x, y, from_empty: bool):
        if self.get_matrix_val(x, y): 
            return 1    
        else:
            if not from_empty:
                key = (self._x*(y+1))-(self._x-(x+1)+1)
                self.empty_list.append(key)
            return 0



    def get_matrix_val(self, x_coord, y_coord):
        '''
        try:
            assert x_coord >= 0 and x_coord < self._x 
            assert y_coord >= 0 and y_coord < self._y
        except AssertionError:
            return None
            #raise IndexError(f'{x_coord}, {y_coord}')
        '''
        index = self._i_from_xy(x_coord, y_coord)
        return self.world_grid.get(index, None) 

    def _i_from_xy(self, x_coord, y_coord):
        return (self._x*(y_coord+1))-(self._x-(x_coord+1)+1)


    def put_matrix_val(self, x_coord, y_coord, value):
        try:
            assert x_coord >= 0 and x_coord < self._x 
            assert y_coord >= 0 and y_coord < self._y
        except AssertionError:
            pass
            #raise IndexError()

        self.world_grid[(self._x*(y_coord+1))-(self._x-(x_coord+1)+1)] = value

    def delete_matrix_val(self, x_coord, y_coord):
        '''
        try:
            assert x_coord >= 0 and x_coord < self._x 
            assert y_coord >= 0 and y_coord < self._y
        except AssertionError:

            raise IndexError()
        '''
        del self.world_grid[(self._x*(y_coord+1))-(self._x-(x_coord+1)+1)]


    
    def xy_from_index(self, i):
        y, x = divmod(i, self._x)
        if y == 0:
            x = i
        return x, y

        
