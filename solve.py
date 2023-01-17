
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

def solve(b):
    '''
    Solving the given sudoku board b using the backtracking algorithm
    '''
    # Defining Hashmaps to store values while parsing
    rows = {}
    boxes = {}
    columns = {}
    avail = {}

    # Parse through the board
    for r in range(len(board)):
        rows[r] = []
        for c in range(len(board[0])):
            if r == 0:
                columns[c] = []
            box = ((r // 3) * 3) + ((c // 3) + 1)
            if r % 3 == 0 and c % 3 == 0:
                boxes[box] = []
            
            v = board[r][c]
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
        box = ((row // 3) * 3) + ((col // 3) + 1)
        for b in boxes.get(box):
            s.add(b)
        for n in range(1, 10):
            if n not in s:
                avail[k].append(n)
    
    print(avail)

solve(board)