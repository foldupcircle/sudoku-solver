from copy import deepcopy

rows_or = {}
columns_or = {}
boxes_or = {}
board = [
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

original_board = deepcopy(board)

def can_input(r, c, b, key, val):
    '''
    Return True if val can be placed at coordinate key(tuple), else False
    '''
    row = key[0]
    col = key[1]
    box = ((row // 3) * 3) + (col // 3)
    if val in r.get(row) or val in c.get(col) or val in b.get(box):
        return False
    return True

def parse(bo, rows, columns, boxes, avail={}):
    # Parse through the board, storing empty and existing values
    for r in range(len(bo)):
        rows[r] = []
        for c in range(len(bo[0])):
            if r == 0:
                columns[c] = []
            box = ((r // 3) * 3) + (c // 3)
            if r % 3 == 0 and c % 3 == 0:
                boxes[box] = []
            
            v = bo[r][c]
            if v:
                rows[r].append(v)
                columns[c].append(v)
                boxes[box].append(v)
            else:
                avail[(r, c)] = []
    
    # Store all empty values in avail
    for k in avail.keys():
        s = set()
        row = k[0]
        col = k[1]
        for r in rows.get(row):
            s.add(r)
        for c in columns.get(col):
            s.add(c)
        box = ((row // 3) * 3) + (col // 3)
        for b in boxes.get(box):
            s.add(b)
        for n in range(1, 10):
            if n not in s:
                avail[k].append(n)

def solve(bo):
    '''
    Solving the given sudoku board b using the backtracking algorithm
    '''
    # Defining Hashmaps to store values while parsing
    rows = {}
    boxes = {}
    columns = {}
    avail = {}

    parse(bo, rows, columns, boxes, avail)

    rows_or = deepcopy(rows)
    columns_or = deepcopy(columns)
    boxes_or = deepcopy(boxes)

    avail_spaces = sorted(avail.keys())
    def place(k_index):
        '''
        Place the numbers in available spaces, backtracking when they don't fit
        '''
        if k_index == len(avail_spaces):
            return 0
        r = avail_spaces[k_index][0]
        c = avail_spaces[k_index][1]
        b = ((r // 3) * 3) + (c // 3)
        found = False
        for v in avail.get(avail_spaces[k_index]):
            if can_input(rows, columns, boxes, avail_spaces[k_index], v):
                rows[r].append(v)
                columns[c].append(v)
                boxes[b].append(v)
                bo[r][c] = v
                res = place(k_index + 1)
                if res:
                    rows[r].pop()
                    columns[c].pop()
                    boxes[b].pop()
                    bo[r][c] = 0
                else:
                    found = True
        if not found:
            return 1
        else:
            return 0
    place(0)
    return bo

def print_board(b):
    for i in b:
        print(i)

solve(board)
print_board(board)