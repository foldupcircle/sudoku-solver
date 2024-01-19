from copy import deepcopy

class Solver:
    def __init__(self) -> None:
        self.rows_or = {}
        self.columns_or = {}
        self.boxes_or = {}
        self.board = [
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

        self.avail = {}
        self.parse()

    def can_input(self, r, c, val):
        '''
        Return True if val can be placed at coordinate key(tuple), else False
        '''
        box = ((r // 3) * 3) + (c // 3)
        if val in self.rows_or.get(r) or val in self.columns_or.get(c) or val in self.boxes_or.get(box):
            return False
        return True

    def parse(self):
        # Parse through the board, storing empty and existing values
        for r in range(len(self.board)):
            self.rows_or[r] = []
            for c in range(len(self.board[0])):
                if r == 0:
                    self.columns_or[c] = []
                box = ((r // 3) * 3) + (c // 3)
                if r % 3 == 0 and c % 3 == 0:
                    self.boxes_or[box] = []
                
                v = self.board[r][c]
                if v:
                    self.rows_or[r].append(v)
                    self.columns_or[c].append(v)
                    self.boxes_or[box].append(v)
                else:
                    self.avail[(r, c)] = []
        
        # Store all empty values in avail
        for k in self.avail.keys():
            s = set()
            row = k[0]
            col = k[1]
            for r in self.rows_or.get(row):
                s.add(r)
            for c in self.columns_or.get(col):
                s.add(c)
            box = ((row // 3) * 3) + (col // 3)
            for b in self.boxes_or.get(box):
                s.add(b)
            for n in range(1, 10):
                if n not in s:
                    self.avail[k].append(n)

    def _place(self, rows, columns, boxes, avail_spaces, avail, k_index):
        '''
        Private function to place the numbers in available spaces, backtracking when they don't fit
        '''
        if k_index == len(avail_spaces):
            return 0
        r = avail_spaces[k_index][0]
        c = avail_spaces[k_index][1]
        b = ((r // 3) * 3) + (c // 3)
        found = False
        for v in avail.get(avail_spaces[k_index]):
            if self.can_input(v):
                rows[r].append(v)
                columns[c].append(v)
                boxes[b].append(v)
                self.board[r][c] = v
                res = self._place(k_index + 1)
                if res:
                    rows[r].pop()
                    columns[c].pop()
                    boxes[b].pop()
                    self.board[r][c] = 0
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
        self.parse()

        rows = deepcopy(self.rows_or)
        columns = deepcopy(self.columns_or)
        boxes = deepcopy(self.boxes_or)
        avail_spaces = sorted(self.avail.keys())
        
        self._place(rows, columns, boxes, avail_spaces, 0)
        return self.board

    def print_board(self):
        for i in self.board:
            print(i)
