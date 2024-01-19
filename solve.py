import time
from copy import deepcopy
from square import Square
from GUI2 import GUI

class Solver:
    def __init__(self, gui: GUI) -> None:
        self.gui = gui
        self.rows_or = {}
        self.columns_or = {}
        self.boxes_or = {}
        self.avail = {}

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
        bo = [
            [5,0,0,0,1,6,2,0,0],
            [0,0,0,9,8,0,5,0,4],
            [0,3,0,0,0,0,0,0,9],
            [0,0,0,6,0,0,1,0,0],
            [9,0,6,0,0,0,0,0,2],
            [0,2,3,0,4,9,0,0,0],
            [0,4,0,0,0,0,0,8,1],
            [3,1,5,2,9,0,0,6,7],
            [8,0,9,4,7,1,0,2,5]
        ]

        self.board = deepcopy(bo)
        empty = 0
        for r in range(len(bo)):
            for c in range(len(bo[0])):
                self.board[r][c] = Square(r, c, bo[r][c])
                if not bo[r][c]:
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
        box = ((r // 3) * 3) + (c // 3)
        if val in self.rows_or.get(r) or val in self.columns_or.get(c) or val in self.boxes_or.get(box):
            return False
        return True

    def parse(self):
        '''
        Sets:
        - self.rows_or: {row number: [numbers in row]}
        - self.columns_or: {column number: [numbers in column]}
        - self.boxes_or: {box number: [numbers in box]}
        - self.avail: {(r, c) location: set of values that can go here}
        '''
        # Parse through the board, storing empty and existing values
        for r in range(len(self.board)):
            self.rows_or[r] = [] # Initalizing row array for each row
            for c in range(len(self.board[0])):
                if r == 0:
                    self.columns_or[c] = [] # Initalizing column array for each column
                box = Solver.get_box_number(r, c)
                if r % 3 == 0 and c % 3 == 0:
                    self.boxes_or[box] = [] # Initalizing box array for each box
                
                v = self.board[r][c].value
                if v:
                    self.rows_or[r].append(v)
                    self.columns_or[c].append(v)
                    self.boxes_or[box].append(v)
                else:
                    self.avail[(r, c)] = []
        
        # Store all empty values in avail
        for k in self.avail.keys():
            row = k[0]
            col = k[1]
            for n in range(1, 10):
                if self.can_input(row, col, n):
                    self.avail[k].append(n)

        self.avail.sort()

    def _place(self, rows, columns, boxes, avail_spaces, avail, key_index):
        '''
        Private function to place the numbers in available spaces, backtracking when they don't fit
        '''
        avail_spaces = sorted(self.avail.keys())
        if key_index == len(avail_spaces):
            return 0
        r = avail_spaces[key_index][0]
        c = avail_spaces[key_index][1]
        b = Solver.get_box_number(r, c)
        found = False
        for v in avail.get(avail_spaces[key_index]):
            if self.can_input(v):
                rows[r].append(v)
                columns[c].append(v)
                boxes[b].append(v)
                self.board[r][c] = v
                self.board[r][c].value = v
                self.gui.draw_sudoku_grid(self.board, (0, 0), False, len(self.avail), round(time.time() - self.start))
                time.sleep(0.05)
                res = self._place(key_index + 1)
                if res:
                    rows[r].pop()
                    columns[c].pop()
                    boxes[b].pop()
                    self.board[r][c].value = 0
                    self.gui.draw_sudoku_grid(self.board, (0, 0), False, len(self.avail), round(time.time() - self.start))
                else:
                    found = True
        if not found:
            return 1
        else:
            return 0

    def solve(self):
        '''
        Solving the given sudoku board b using the backtracking algorithm
        '''
        rows = deepcopy(self.rows_or)
        columns = deepcopy(self.columns_or)
        boxes = deepcopy(self.boxes_or)
        avail_spaces = sorted(self.avail.keys())

        self.start = time.time()
        self._place(rows, columns, boxes, avail_spaces, 0)
        self.gui.draw_sudoku_grid(self.board, (0, 0), False, len(self.avail), round(time.time() - self.start))
        return self.board

    def print_board(self):
        for i in self.board:
            print(i)
