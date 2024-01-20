# Sudoku Solver

![](https://github.com/foldupcircle/sudoku-solver/blob/main/sudoku-solve.gif)

## Key Features
* Create a sudoku board of varying difficulty
* Solve a sudoku board using a backtracking algorithm
* GUI display with visual representation of algorithm and solve time

## How to Use
Run `python main.py` and choose a difficulty level, 1 being the easiest and 3 the hardest.

## Backtracking Algorithm
The backtracking algorithm is an improvement of the naive approach. It goes through each empty square, inputs a valid number, and moves on to the next empty square. However, if a square doesn't have any valid numbers, it will "backtrack" to the previous square and try a different solution. This avoids going through solutions that we already know aren't correct
