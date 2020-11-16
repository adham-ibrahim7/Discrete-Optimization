# Sudoku Solving

Implementing a better than brute force solution to sudoku solving.

By storing the valid domain of each empty spot, and only trying to fill
the spots with values that have not been determined to be impossible is 
enough to efficiently solve sudokus.

A nice bonus is that by randomizing the order in which numbers are tried,
random valid sudoku boards can be generated efficiently.

Run `python sudoku_solver.py file.txt` on a board to solve it. Run
`python generate_random.py` to print out a random board.