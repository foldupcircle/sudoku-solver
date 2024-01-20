import time
from copy import deepcopy
from square import Square
from sudoku import Sudoku

class Solver:
    def __init__(self, difficulty, gui=None) -> None:
        self.gui = gui
        self.rows = {}
        self.columns = {}
        self.boxes = {}
        self.avail = {}
        self.difficulty = difficulty

        # Sets self.board and returns the number of empty values in the board
        self.empty = self._set_board()

        self.parse()

        self.original_board = deepcopy(self.board)

    def _set_board(self):
        '''
        Private function that sets self.board with Square objects
        Called in Solver.__init__

        Returns: number of empty squares in self.board
        '''
        bo = Sudoku(3).difficulty(self.difficulty)

        self.board = deepcopy(bo.board)
        empty = 0
        for r in range(len(bo.board)):
            for c in range(len(bo.board[0])):
                self.board[r][c] = Square(r, c, bo.board[r][c])
                if not bo.board[r][c]:
                    empty += 1
        
        return empty
    
    def get_box_number(r, c):
        '''
        Returns the correct box number based on the row and column
        '''
        return ((r // 3) * 3) + (c // 3)

    def can_input(self, r, c, val):
        '''
        Returns True if val can be placed at (r, c), else False
        '''
        box = Solver.get_box_number(r, c)
        if val in self.rows.get(r) or val in self.columns.get(c) or val in self.boxes.get(box):
            return False
        return True

    def parse(self):
        '''
        Sets:
        - self.rows: {row number: [numbers in row]}
        - self.columns: {column number: [numbers in column]}
        - self.boxes: {box number: [numbers in box]}
        - self.avail: {(r, c) location: set of values that can go here}
        '''

        # Parse through the board, storing empty and existing values
        for r in range(len(self.board)):
            self.rows[r] = [] # Initalizing row array for each row
            for c in range(len(self.board[0])):
                if r == 0:
                    self.columns[c] = [] # Initalizing column array for each column
                box = Solver.get_box_number(r, c)
                if r % 3 == 0 and c % 3 == 0:
                    self.boxes[box] = [] # Initalizing box array for each box
                
                v = self.board[r][c].value
                if v:
                    self.rows[r].append(v)
                    self.columns[c].append(v)
                    self.boxes[box].append(v)
                else:
                    self.avail[(r, c)] = []
        
        # Store all empty values in avail
        for k in self.avail.keys():
            row = k[0]
            col = k[1]
            for n in range(1, 10):
                if self.can_input(row, col, n):
                    self.avail[k].append(n)

    def _place(self, key_index):
        '''
        Private function to place the numbers in available spaces, backtracking when they don't fit
        '''

        # Get keys from self.avail
        avail_spaces = sorted(self.avail.keys())

        # Base Case
        if key_index == len(avail_spaces):
            return 0

        # Get row, col, and box of location -> avail_spaces[key_index] returns (r, c)
        location = avail_spaces[key_index]
        r = location[0]
        c = location[1]
        b = Solver.get_box_number(r, c)

        # Go through all values that can go in location
        found = False
        for v in self.avail.get(location):

            # Double check if v can go in location (useful in recursive calls because self.avail is not updated)
            if self.can_input(r, c, v):

                # Add value into data structures
                self.rows[r].append(v)
                self.columns[c].append(v)
                self.boxes[b].append(v)
                self.board[r][c].value = v
                self.empty -= 1

                self.gui.draw_sudoku_grid(self.empty, round(time.time() - self.start))
                time.sleep(0.05)

                # Go to next location and attempt to place value, returns 0 (success) or 1 (fail)
                res = self._place(key_index + 1)

                # If fail, remove value from all data structures
                if res:
                    self.rows[r].pop()
                    self.columns[c].pop()
                    self.boxes[b].pop()
                    self.board[r][c].value = 0
                    self.empty += 1
                    self.gui.draw_sudoku_grid(self.empty, round(time.time() - self.start))
                else:
                    found = True
                    break
        if not found:
            return 1
        else:
            return 0

    def solve(self):
        '''
        Solving the given sudoku board using the backtracking algorithm

        Returns: 1 for not solved and 0 for solved
        '''
        self.start = time.time()

        # Call recursive function
        res = self._place(0)

        # Draw final result with solve time
        self.gui.draw_sudoku_grid(self.empty, round(time.time() - self.start))

        return res

    def print_board(self): 
        # TODO
        for i in self.board:
            print(i)
