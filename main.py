import pygame
from solve import Solver
from GUI2 import GUI

def main(gui: GUI, solver: Solver):
    pygame.init()
    run = True
    solve_time = 0
    while run:
        if gui.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    solve_time = gui.handle_inputs(event)
                    
                gui.draw_sudoku_grid(solver.empty, round(solve_time))
            pygame.display.update()
        gui.draw_sudoku_grid(solver.empty, round(solve_time))
    pygame.quit()

if __name__ == '__main__':
    level = input("Level (1-3): ") 
    assert level.isdigit()
    assert int(level) <= 3 and int(level) >= 1
    gui = GUI()
    if level == 3:
        diff = 0.75
    elif level == 2:
        diff = 0.65
    else:
        diff = 0.55
    solver = Solver(diff, gui)
    gui.solver = solver
    main(gui, solver)
