from .gui_variables import TkAppVariables, control_values, WINDOW_SIZE, grid_ratio
import tkinter as tk
from tkinter import SOLID
import random, time
from math import floor 
from objects.world import WorldGrid
from .cell_patterns import cell_patterns

class CanvasSim:
    """
    Handles the rendering of the simulation to a tkinter canvas
    """
    def __init__(self, frm:tk.Frame, window, message:tk.Label) -> None:
        self._w = WINDOW_SIZE[0]
        self._h = WINDOW_SIZE[1]       
        self._c = tk.Canvas(frm, width=self._w, height=self._h, background="#181c27", borderwidth=1, relief=SOLID)
        self._c.grid()
        self.cycle = 0
        self.isRunning = False
        self.message = message
        self.window = window
        self._grid = None
        self._grid_width = None
        #self._mouse_pos = tk.Label(window, textvariable=TkAppVariables.message)
        #self._mouse_pos.grid()
        self._model = WorldGrid(
            int(TkAppVariables.grid_x.get()), 
            int(TkAppVariables.grid_y.get())
            )
        self._set_grid_scale()
        self._last_frame = None
        self._c.bind("<Motion>", self.mouse_pos)
        self._c.bind("<Button>", self.place_pattern_mouse)

    def stop(self):
        """
        Stops the simulation
        """
        self._last_frame = self._model.world_grid
        self.isRunning = False
        
       
    def reset(self):
        """
        Resets the simulation
        """
        self.cycle = 0
        self.isRunning = False
        self._model = None
        self._last_frame = None
        self._c.delete("cell") 
        self._record_cycles(0)
        self._c.update()


    def start(self, gx:int, gy:int, rand:int, cycles:int, delay:int):
        """
        Runs the simulation
        """
        # size of the grid will may change on stop/run or reset, update the app variables                
        TkAppVariables.grid_x.set(gx)
        TkAppVariables.grid_y.set(gy)
        # verify there is model
        if self._model:
            # check if model is the same size as the dimesion submitted
            if self._model.get_x() != gx or self._model.get_y() != gy:
                self._last_frame = None
                self._model = WorldGrid(gx, gy)
            else:
                # if the model is the same, check if a the model has 
                # been previously run and load that data
                if self._last_frame:
                    self._model.world_grid = self._last_frame
        else:
            self._model = WorldGrid(gx, gy)

        self._isrunning = True
        self._grid_width = gx 
        self._set_grid_scale()

        
        for x in range(floor(gx * gy * (rand / 100))):
            random.seed()
            randx = random.randrange(0, gx)
            randy = random.randrange(0, gy)
            self._model.switch_cell(randx,randy)

        self._render_sim(cycles, delay)
 
    

    def _render_sim(self, cycles, delay):
        """
        Renders a simulation animation onto the canvas 
        """

        # load initial data used by the animation
        self._grid = self._model.live_list()
        while self.isRunning and cycles > self.cycle:
            
            # delete any cells from a previous frame
            self._c.delete("cell") 
            
            # state which frame or cycle the animation is on
            self._record_cycles(self.cycle)
            self._draw_frame()
            time.sleep(delay / 1000) 
            # update() refreshes the canvas object
            self._c.update()
            # if the model is longer present then end the animation
  
                     
            if not self._model:
                self.isRunning = False
                break
            self._model.next_stage() 
            self._grid = self._model.live_list()
            # get the data for the next frame
            self.cycle += 1 


    def _draw_frame(self):
        """
        Draws a single frame or cycle when the simulation is run
        """
        color = ""
        for live_cell in self._grid:
            if live_cell[2] == 2:
                color = "#b0ff00"
            elif live_cell[2] == 3:
                color = "#ff00aa"
            
            self._draw_cell(live_cell[0], live_cell[1], color)

    
    def _draw_cell(self, x, y, color):
        """
        Draws a single cell onto the canvas
        """
        self._c.create_oval(
            
            x*self._scale_x, 
            y*self._scale_y, 
            (x+1)*self._scale_x, 
            (y+1)*self._scale_y, 
            tags="cell",
            fill=color,
            outline="#181c27",
            
            ) 


    def _record_cycles(self, cycle:int) -> None:
        """
        Used to update the cycles information on the window
        """
        TkAppVariables.cycle_info.set(f'{cycle} cycles')
        self.message.configure(
            textvariable=TkAppVariables.cycle_info
        )

    def place_pattern_mouse(self, event):
        self._pattern(
            int(TkAppVariables.mouse_pos_x.get()), 
            int(TkAppVariables.mouse_pos_y.get())
            )

    def place_pattern_button(self, x, y):
        self._pattern(x, y)


    def _pattern(self, x, y):
        """
        Places cell patterns onto canvas
        """
        self._c.update()
        # selected pattern
        pattern = cell_patterns[TkAppVariables.pattern_type_var.get()]
       
        
        # if there is no model assinged to sim then initialise one
        if not self._model:
            self._model = WorldGrid(
                int(TkAppVariables.grid_x.get()), 
                int(TkAppVariables.grid_y.get()),
                )
            
            self._grid_width = self._model.get_x()
            self._set_grid_scale()
        
        # place the cell pattern onto the model and canvas 
        self._place_pattern(pattern, x, y)
        
        # updating the _last_frame enables the sim to run from there with 
        # placed pattern encluded 
        self._last_frame = self._model.world_grid


    def _place_pattern(self, pattern, x_pos, y_pos):
        """
        Loops over the pattern and registers new cells to the model and 
        canvas
        """
        height = len(pattern)
        width = len(pattern[0])    
        for y in range (height):
            for x in range(width):
                if pattern[y][x] == 1:
                    self._place_cell(x + x_pos, y + y_pos)

        
            

    def _place_cell(self, x_pos, y_pos):
        """
        Places a cell onto the canvas or removes a cell from the canvas
        depending on whether cell is alive or not
        """
        if y_pos <= int(TkAppVariables.grid_y.get()) \
            and x_pos <= int(TkAppVariables.grid_x.get()) :

            # if cell is alive then remove it, else create a new one
            if self._model.get_matrix_val(x_pos, y_pos):
                self._model.put_matrix_val(x_pos, y_pos, None)
                self._draw_cell(x_pos, y_pos, "#181c27")
            else:    
                self._draw_cell(x_pos, y_pos, "green")
                self._model.put_matrix_val(x_pos, y_pos, 1)


    def mouse_pos(self, event):
        """
        Using the canvas xy coordinates this method calculates the position 
        of the mouse in terms of the grid coordinates, based on the 
        simulation model.
        """
        if not self._grid_width:
            x_size = control_values['sim gridX']['default']
        else:
            x_size = TkAppVariables.grid_x.get()
            if x_size == '':
                x_size = control_values['sim gridX']['default']
            else:
                x_size = int(x_size)
        
        # calculate the grid position of the mouse pointer
        x_pos = int(event.x / (self._w / x_size))
        y_pos = int(event.y / (self._h / (x_size / grid_ratio)))

        # assign mouse xy grid position to the global static variables
        TkAppVariables.mouse_pos_x.set(x_pos)
        TkAppVariables.mouse_pos_y.set(y_pos)
        
        return (x_pos, y_pos)
        
        
    def _set_grid_scale(self):
        """
        Calculates the scale factor in relation to canvas size an the grid size
        """
        self._scale_x = self._w / int(TkAppVariables.grid_x.get()) 
        self._scale_y = self._h / int(TkAppVariables.grid_y.get())


    