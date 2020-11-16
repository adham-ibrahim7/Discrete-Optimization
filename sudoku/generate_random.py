from sudoku.sudoku_solver import search


def get_random_board():
    board = []
    empty_positions = []
    for i in range(9):
        board.append(list(list(range(1, 10)) for j in range(9)))
        for j in range(9):
            empty_positions.append((i, j))
    search(board, empty_positions, True)


if __name__ == '__main__':
    get_random_board()
