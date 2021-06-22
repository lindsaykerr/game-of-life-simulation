from gui_elements.gui_variables import window
from gui_elements.view_elements import GoFView
from gui_elements.canvas_sim import CanvasSim
from gui_elements.controls import AppControls


def main():
    
    # VIEW SETUP
    view = GoFView(window)      
    sim = CanvasSim(view.canvas_holder, window, view.cycle_info) 
    controls = AppControls(window)  
    # ASSIGNING CONTROLS
    controls.sim_percentage(view.randomize_cells)
    controls.sim_cycles(view.cycle)
    controls.sim_delays(view.delays)
    controls.sim_run(view.run, sim, view.reset)
    controls.sim_reset(view.reset,sim)
    controls.sim_grid_dimX(view.grid_x, view.grid_y, view.reset)
    controls.sim_grid_dimY(view.grid_y, view.grid_x, view.reset)
    controls.sim_y_pos(view.pattern_pos_Y)
    controls.sim_x_pos(view.pattern_pos_x)
    controls.sim_set_pattern(view.pattern_set, sim)
   
    window.mainloop()


if __name__ == '__main__':
    main()
