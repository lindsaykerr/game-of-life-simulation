import tkinter as tk

window = tk.Tk()

WINDOW_SIZE = (700, 600)

grid_ratio = WINDOW_SIZE[0] / WINDOW_SIZE[1]

# Used to set the default ranges and values on the interface
control_values = {
    "sim randomize": {
        "default": 0,
        "range" : [0, 100]
    },
    "sim cycles": {
        "default": 1000,
        "range" : [1, 100000]
    },
    "sim delay": {
        "default": 10,
        "range" : [1, 10000]
    },
    "sim gridX": {
        "default": 20,
        "range" : [10, 200]
    },
    "sim gridY": {
        "default": int(20 / grid_ratio),
        "range" : [10, 200]
    },
    "sim pattern": {
        "default": "Single"
    }
}

# For providing access to tkinter variables across objects 
class TkAppVariables:
    grid_x = tk.StringVar(
        window, 
        value=control_values['sim gridX']['default']
        )
    grid_y = tk.StringVar(
        window, 
        value=control_values['sim gridY']['default']
        )
    randomize_cells = tk.StringVar(
        window, 
        value=control_values['sim randomize']['default']
        )
    pattern_type_var = tk.StringVar(
        window, 
        value=control_values['sim pattern']['default']
        )
    pattern_pos_x = tk.StringVar(window, value="0")
    pattern_pos_y = tk.StringVar(window, value="0")
    cycle = tk.StringVar(
            window, 
            value=control_values['sim cycles']['default']
            )
    delays = tk.StringVar(
            window, 
            value=control_values['sim delay']['default']
            )
    run = tk.StringVar(window, value="Run")
    cycle_info = tk.StringVar(window)
    #message = tk.StringVar(window, value="")
    mouse_pos_x = tk.StringVar(window, value="0")
    mouse_pos_y = tk.StringVar(window, value="0")