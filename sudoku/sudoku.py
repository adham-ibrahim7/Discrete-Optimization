def filled(board, i, j):
    """
    Determine if [i][j] is unfilled, the algorithm has not chosen a number to fill
    this square yet
    """

    return type(board[i][j]) is int


def single_value(board, i, j):
    """
    Fill a value if there is only one feasible value left
    """

    if not filled(board, i, j) and len(board[i][j]) == 1:
        board[i][j] = board[i][j][0]

    return board


def standard_constraints(board, r, c):
    """
    For a certain position enforce the row, column, and box constraints, only on squares
    that could be affected
    """

    for i in range(9):
        if not filled(board, i, c) and board[r][c] in board[i][c]:
            board[i][c].remove(board[r][c])
            if len(board[i][c]) == 0:
                return None

    for j in range(9):
        if not filled(board, r, j) and board[r][c] in board[r][j]:
            board[r][j].remove(board[r][c])
            if len(board[r][j]) == 0:
                return None

    i0 = r // 3 * 3
    j0 = c // 3 * 3

    for i in range(i0, i0 + 3):
        for j in range(j0, j0 + 3):
            if not filled(board, i, j) and board[r][c] in board[i][j]:
                board[i][j].remove(board[r][c])
                if len(board[i][j]) == 0:
                    return None

    return board


def check_valid(board, r, c):
    valid = set(range(1, 10))

    for i in range(9):
        if board[i][c] in valid:
            valid.remove(board[i][c])

    for j in range(9):
        if board[r][j] in valid:
            valid.remove(board[r][j])

    for i in range(r // 3 * 3, r // 3 * 3 + 3):
        for j in range(c // 3 * 3, r // 3 * 3 + 3):
            if board[i][j] in valid:
                valid.remove(board[i][j])

    return valid

def search(board):
    if not board:
        return None

    for i in range(9):
        for j in range(9):
            if filled(board, i, j):
                continue
            for n in board[i][j]:
                temp = board.copy()
                temp[i][j] = n
                temp = standard_constraints(board, i, j)
                attempt = search(temp)
                if attempt:
                    return attempt
            return None
    else:
        return board

def solve(board):
    for i in range(9):
        for j in range(9):
            board = standard_constraints(board, i, j)
    return search(board)

def print_board(board):
    """
    Pretty print the board
    """

    if board is None:
        print("NULL BOARD")
        return

    for i in range(9):
        if i > 0 and i % 3 == 0:
            print("- - - - - - - - - - - -")

        for j in range(9):
            if j > 0 and j % 3 == 0:
                print(" | ", end="")

            curr = str(board[i][j] if type(board[i][j]) is int else 0)
            #curr = str(board[i][j])

            if j == 9 - 1:
                print(curr)
            else:
                print(curr + " ", end="")
    print()


def read_file(filepath):
    import sys

    with open(filepath) as input_file:
        board = []
        for i in range(9):
            board.append(list(int(s) for s in input_file.readline().split()))
            for j in range(9):
                if board[i][j] == 0:
                    board[i][j] = list(range(1, 10))
        return board
    return None


if __name__ == '__main__':
    """
    board = [[0, 3, 4, 6, 7, 8, 9, 1, 2],
             [6, 7, 2, 1, 9, 5, 3, 4, 8],
             [1, 9, 8, 3, 4, 2, 5, 6, 7],
             [8, 5, 9, 7, 6, 1, 4, 2, 3],
             [4, 2, 6, 8, 5, 3, 7, 9, 1],
             [7, 1, 3, 9, 2, 4, 8, 5, 6],
             [9, 6, 1, 5, 3, 7, 2, 8, 4],
             [2, 8, 7, 4, 1, 9, 6, 3, 5],
             [3, 4, 5, 2, 8, 6, 1, 7, 9]]
    """

    board = read_file("ex1.txt")

    print_board(board)

    print_board(solve(board))
