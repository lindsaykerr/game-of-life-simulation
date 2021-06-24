from gui_elements.canvas_sim import CanvasSim
from tkinter import DISABLED, ACTIVE
from .control_validation import ValidationMethods, ValidationAssignment
from .gui_variables import TkAppVariables, control_values, grid_ratio
import tkinter as tk


class AppControls:
    """
    Assigns controls to widgets, and sets basic widget configuration and
    validation.
    """
    disable_reg = []  # controls list to disabled widgets when sim is running
    _perc_w = None
    _cycles_w = None
    _delays_w = None
    _x_dim_w = None
    _y_dim_w = None
    _x_pos_w = None
    _y_pos_w = None
    _pattern = None
    _run_w = None
    mouse_loc = None

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._run_widget = None

        # set all the variables for the input field
        self._randomize = TkAppVariables.randomize_cells
        self._cycles = TkAppVariables.cycle
        self._delay = TkAppVariables.delays
        self._grid_x = TkAppVariables.grid_x
        self._grid_y = TkAppVariables.grid_y
        self._pattern_x = TkAppVariables.pattern_pos_x
        self._pattern_y = TkAppVariables.pattern_pos_y
        self._run = TkAppVariables.run

    def sim_percentage(self, perc_w: tk.Widget):
        """
        Assign widget for percentage input
        """
        cv = control_values['sim randomize']
        validation = ValidationAssignment(
            self._randomize,
            ValidationMethods.is_valid_range,
            start=cv['range'][0],
            end=cv['range'][1]
        )
        valid_percent = (self._root.register(validation.method), '%P')

        self._perc_w = perc_w
        perc_w.configure(
            textvariable=self._randomize,
            from_=cv['range'][0],
            to=cv['range'][1],
            validate="key",
            validatecommand=valid_percent,
            invalidcommand=validation.back_to_default
        )

        self.disable_reg.append(perc_w)

    def sim_cycles(self, cycles_w: tk.Widget):
        """
        Set cycle control to widget cycles_W
        """
        sc = control_values['sim cycles']
        validation = ValidationAssignment(
            self._cycles,
            ValidationMethods.is_valid_range,
            start=sc['range'][0],
            end=sc['range'][1]
        )
        valid_cycles = (self._root.register(validation.method), '%P')

        self._cycles_w = cycles_w
        cycles_w.configure(
            textvariable=self._cycles,
            from_=sc['range'][0],
            to=sc['range'][1],
            validate="key",
            validatecommand=valid_cycles
        )

        self.disable_reg.append(cycles_w)

    def set_pattern(self, pattern_w: tk.Widget):
        """
        Set pattern variable to drop down widget
        """
        self._pattern = pattern_w
        self._pattern.configure(
            textvariable=TkAppVariables.pattern_type_var

        )

    def sim_delays(self, delays_w: tk.Widget):
        """
        Set delay controls to widget 
        """
        sd = control_values['sim delay']
        validation = ValidationAssignment(
            self._delay,
            ValidationMethods.is_valid_range,
            start=sd['range'][0],
            end=sd['range'][1],
        )
        valid_delays = (self._root.register(validation.method), '%P')

        self._delays_w = delays_w
        delays_w.configure(
            textvariable=self._delay,
            from_=sd['range'][0],
            to=sd['range'][1],
            validate="key",
            validatecommand=valid_delays
        )

        self.disable_reg.append(delays_w)

    def sim_grid_dimX(self, dim_w: tk.Widget, other: tk.Widget,
                      reset_button: tk.Widget):
        """
        Set the grid size x control
        """
        self.disable_reg.append(dim_w)

        def on_spin():
            for widget in self.disable_reg:
                if widget not in [dim_w, other, reset_button]:
                    widget.configure(state=DISABLED)

        gx = control_values['sim gridX']
        validation = ValidationAssignment(
            self._grid_x,
            ValidationMethods.is_valid_x,
            start=gx['range'][0],
            end=gx['range'][1],
            factor=grid_ratio,
            y_widget=other,
            y=self._grid_y,
            default=gx['default']
        )
        valid_delays = (self._root.register(validation.method), '%P')

        self._x_dim_w = dim_w
        self._grid_x.set(str(20))
        dim_w.configure(
            textvariable=self._grid_x,
            from_=gx['range'][0],
            to=gx['range'][1],
            validate="focusout",
            command=on_spin,
            validatecommand=valid_delays
        )

    def sim_grid_dimY(self, dim_w: tk.Widget, other: tk.Widget,
                      reset_button: tk.Widget):
        """
        Set the grid size y control
        """
        gy = control_values['sim gridY']
        self.disable_reg.append(dim_w)

        def on_spin():
            for widget in self.disable_reg:
                if widget not in [dim_w, other, reset_button]:
                    widget.configure(state=DISABLED)

        validation = ValidationAssignment(
            self._grid_y,
            ValidationMethods.is_valid_y,
            start=gy['range'][0],
            end=gy['range'][1],
            factor=grid_ratio,
            x_widget=other,
            x=self._grid_x,
            default=gy['default']
        )
        valid_delays = (self._root.register(validation.method), '%P')

        self._y_dim_w = dim_w
        self._grid_y.set(str(int(20 / grid_ratio)))
        dim_w.configure(
            command=on_spin,
            textvariable=self._grid_y,
            from_=gy['range'][0],
            to=gy['range'][1],
            validate="focusout",
            validatecommand=valid_delays
        )

    def sim_x_pos(self, x_pos_w: tk.Widget):
        """
        Set the x value input control for placing a pattern
        """
        self._x_pos_w = x_pos_w
        validation = ValidationAssignment(
            self._pattern_x,
            ValidationMethods.is_X_position,
        )
        pos_x = (self._root.register(validation.method), '%P')

        # self._pattern_x.set(str(int(20 / grid_ratio)))
        x_pos_w.configure(
            textvariable=self._pattern_x,
            from_=0,
            to=int(self._grid_x.get()) - 1,
            validate="focusout",
            validatecommand=pos_x
        )

    def sim_y_pos(self, y_pos_w: tk.Widget):
        """
        Set the y value input control for placing a pattern
        """
        self._y_pos_w = y_pos_w
        validation = ValidationAssignment(
            self._pattern_y,
            ValidationMethods.is_Y_position,
        )
        pos_y = (self._root.register(validation.method), '%P')

        # self._pattern_y.set(str(int(20 / grid_ratio)))
        y_pos_w.configure(
            textvariable=self._pattern_y,
            from_=0,
            to=int(self._grid_y.get()) - 1,
            validate="focusout",
            validatecommand=pos_y
        )

    def sim_run(self, run_w: tk.Widget, canvas_sim: CanvasSim,
                reset_w: tk.Widget):
        """
        Set the controls for the run button
        """

        def button_press():
            if self._run.get() == "Run":
                self._run.set("Stop")
                canvas_sim.isRunning = True
                for widget in self.disable_reg:
                    if widget not in [run_w, reset_w]:
                        widget.configure(state=DISABLED)

                canvas_sim.start(
                    int(self._grid_x.get()),
                    int(self._grid_y.get()),
                    int(self._randomize.get()),
                    int(self._cycles.get()),
                    int(self._delay.get())
                )

            else:
                self._run.set("Run")
                canvas_sim.stop()
                for widget in self.disable_reg:
                    widget.configure(state=ACTIVE)

        self.disable_reg.append(run_w)

        run_w.configure(
            textvariable=self._run,
            command=button_press
        )
        self._run_w = run_w

    def sim_set_pattern(self, set_w: tk.Widget, canvas_sim: CanvasSim):
        """
        Set the controls for the place pattern set button
        """

        def place():
            x_pos = int(self._pattern_x.get())
            y_pos = int(self._pattern_y.get())
            canvas_sim.place_pattern_button(x_pos, y_pos)

        set_w.configure(
            command=place
        )

    def sim_reset(self, reset_w: tk.Widget, canvas_sim: CanvasSim,
                  pos_x: tk.Widget, pos_y: tk.Widget):
        """
        Set the controls for the reset button
        """

        def reset():
            if canvas_sim.isRunning:
                canvas_sim.stop()
            for widget in self.disable_reg:
                widget.configure(state=ACTIVE)
            canvas_sim.reset()
            self._run.set("Run")
            self._run_w.configure(
                textvariable=self._run
            )
            pos_x.configure(
                to=int(TkAppVariables.grid_x.get()) - 1
            )

            pos_y.configure(
                to=int(TkAppVariables.grid_y.get()) - 1
            )
            self._root.update()

        reset_w.configure(
            command=reset
        )

    def sim_mouse_location(self, canvas_sim: CanvasSim):
        x, y = canvas_sim.mouse_pos()
        self.mouse_loc = (x, y)

    # def sim_set_pattern()
