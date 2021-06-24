from gui_elements.gui_variables import TkAppVariables
from .cell_patterns import cell_patterns
from tkinter import ttk, font
import tkinter
import tkinter as tk


class GoFView:
    grid_x = None
    grid_y = None
    randomize_cells = None
    pattern_type = None
    pattern_pos_x = None
    pattern_pos_Y = None
    pattern_set = None
    pattern_list = None
    cycle = None
    delays = None
    run = None
    reset = None
    cycle_info = None
    canvas_holder = None
    message = None

    def __init__(self, window: tk.Frame) -> None:
        self.root = window
        self._application_struct()  # builds the structure of the Interface
        self.message = tkinter.Label(window)
        self.message.grid()

    def _application_struct(self):
        self.root.configure(pady=10, padx=10)
        self.root.columnconfigure(6, minsize=10)

        frm_title = tk.Frame(self.root, bg="green")
        frm_cycle_info = tk.Frame(self.root)
        frm_options = tk.Frame(self.root)
        frm_cvs_container = tk.Frame(self.root, width=760, height=760,
                                     bg="yellow")
        frm_grid_op = tk.Frame(self.root, bg="cyan", width=10, height=10)

        frm_title.grid(row=0, column=0, columnspan=4, sticky="NW")
        frm_cycle_info.grid(row=0, column=12, columnspan=4, sticky="SE")
        frm_options.grid(row=1, column=0, columnspan=5, rowspan=11, sticky="NW")
        frm_cvs_container.grid(row=1, column=7, rowspan=11, columnspan=6,
                               sticky="NESW")
        frm_grid_op.grid(row=14, column=11, columnspan=4, sticky="NE")

        # Heading and cycles
        lbl_heading = tk.Label(
            master=frm_title,
            text="Game of Life",
            font=font.Font(size=16, weight="bold")
        )
        lbl_heading.pack(
            side="left"
        )

        lbl_cycles = ttk.Label(
            frm_cycle_info,
            text=""
        )
        lbl_cycles.pack(
            pady=2,
            side="right"
        )

        self._sub_heading(frm_options, "Cells")
        self._randomize_cells(frm_options)
        self._set_pattern(frm_options)
        self._sub_heading(frm_options, "Simulation")
        self._sim_settings(frm_options)
        self._run_button(self.root)
        self._reset_button(self.root)
        self._grid_options(frm_grid_op)

        self.cycle_info = lbl_cycles
        self.canvas_holder = frm_cvs_container

    def _grid_options(self, frame: tk.Frame):
        wrapper = tk.Frame(frame)
        wrapper.pack(fill=tk.X)
        _discrip = ttk.Label(wrapper, text="Grid dimension ")
        _frm_x = ttk.Frame(wrapper)
        _x_box = self._spinbox_option(_frm_x, boxwidth=4, prefix_text="X:")
        _frm_y = tk.Frame(wrapper)
        _y_box = self._spinbox_option(_frm_y, boxwidth=4, prefix_text="Y:")

        _discrip.grid(row=0, column=0, sticky="E", padx=5)
        _frm_x.grid(row=0, column=3, sticky="E", padx=5)
        _frm_y.grid(row=0, column=4, sticky="W")

        self.grid_x = _x_box
        self.grid_y = _y_box

    def _randomize_cells(self, frame):
        sub_frm = tk.Frame(frame)
        sub_frm.pack(fill=tk.X)

        self.randomize_cells = self._spinbox_option(
            sub_frm,
            prefix_text="Randomize Cells",
            posfix_text="%"
        )

    def _set_pattern(self, frm, text="Place Cell Pattern"):
        cell_types = list(cell_patterns.keys())
        cell_types.sort()

        frm_place = ttk.LabelFrame(frm, text=text)
        _option_list = ttk.OptionMenu(frm_place,
                                      TkAppVariables.pattern_type_var,
                                      *cell_types)
        _line1 = tk.Frame(frm_place)
        _x_box = self._spinbox_option(_line1, prefix_text="X:", boxwidth=5,
                                      align=["left", "left", "left"])
        _line2 = tk.Frame(frm_place)
        _y_box = self._spinbox_option(_line2, prefix_text="Y:", boxwidth=5,
                                      align=["left", "left", "left"])
        _btn = ttk.Button(frm_place, text="Set", width=5)

        frm_place.pack(fill=tk.X, pady=10)
        frm_place.rowconfigure([1, 4], minsize=10)
        frm_place.columnconfigure(0, minsize=10)
        _option_list.grid(row=0, column=0, columnspan=3)
        _line1.grid(row=2, column=1, columnspan=3)
        _line2.grid(row=3, column=1, columnspan=3)
        _btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.pattern_set = _btn
        self.pattern_pos_x = _x_box
        self.pattern_pos_Y = _y_box

        self.pattern_list = _option_list

    def _sim_settings(self, frame):
        wrapper = tk.Frame(frame)
        _row1 = tk.Frame(wrapper)
        _row2 = tk.Frame(wrapper)
        _cycles = self._spinbox_option(_row1, boxwidth=6, prefix_text="Cycles:")
        _delays = self._spinbox_option(_row2, boxwidth=6,
                                       prefix_text="Delay (ms):")

        wrapper.pack(fill=tk.X)
        _row1.grid(row=0, column=0, columnspan=3, sticky="E", padx=5)
        _row2.grid(row=1, column=0, columnspan=2, sticky="E", padx=5)

        self.cycle = _cycles
        self.delays = _delays

    def _run_button(self, frame):
        btn_run = ttk.Button(frame, text="Run", padding=5)
        btn_run.grid(
            row=14,
            column=0,
            columnspan=2,
            sticky="SW"
        )

        self.run = btn_run

    def _reset_button(self, frame):
        btn_reset = ttk.Button(frame, text="Reset", padding=5)
        btn_reset.grid(
            row=14,
            column=3,
            columnspan=2,
            sticky="SW"
        )

        self.reset = btn_reset

    @staticmethod
    def _sub_heading(a_frame, text: str, pady=5, padx=0, heading_style=None,
                     separator_style=None):
        wrapper = ttk.Frame(a_frame)
        _sub_head = ttk.Label(wrapper, text=text, style=heading_style,
                              justify="left")
        _sub_sep = ttk.Separator(wrapper, orient="horizontal",
                                 style=separator_style)

        wrapper.pack(fill=tk.X, pady=pady, padx=padx)
        _sub_head.pack(fill=tk.X)
        _sub_sep.pack(fill=tk.X, pady=5)

    @staticmethod
    def _spinbox_option(frm, prefix_text=None, boxwidth=5, posfix_text=None,
                        align=["left", "left", "left"]):
        """
        Creates a general purpose spinbox
        """
        if prefix_text:
            _lbl = ttk.Label(frm, text=prefix_text)
            _lbl.pack(side=align[0], padx=5)

        _scrl_bar = ttk.Spinbox(frm, width=boxwidth)
        _scrl_bar.pack(side=align[1], pady=5)

        if posfix_text:
            _lbl_end = ttk.Label(frm, text=posfix_text)
            _lbl_end.pack(side=align[2])

        return _scrl_bar
