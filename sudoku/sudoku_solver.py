from copy import deepcopy
from random import shuffle
import sys


def filled(board, i, j):
    return type(board[i][j]) is int


def standard_constraints(board, r, c):
    for i in range(9):
        if not filled(board, i, c) and board[r][c] in board[i][c]:
            board[i][c].remove(board[r][c])

    for j in range(9):
        if not filled(board, r, j) and board[r][c] in board[r][j]:
            board[r][j].remove(board[r][c])

    i0 = r // 3 * 3
    j0 = c // 3 * 3

    for i in range(i0, i0 + 3):
        for j in range(j0, j0 + 3):
            if not filled(board, i, j) and board[r][c] in board[i][j]:
                board[i][j].remove(board[r][c])

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


calls: int = 0


def search(board, empty_positions, shuffle_board=False):
    global calls
    calls += 1

    if len(empty_positions) == 0:
        print("SUCCESS! " + str(calls) + " calls made to search()")
        print_board(board)
        if check_board(board):
            print("constraints met")
        return True

    i, j = empty_positions[0]

    if shuffle_board:
        shuffle(board[i][j])
    valid = board[i][j]
    for n in valid:
        board[i][j] = n
        if search(standard_constraints(deepcopy(board), i, j), empty_positions[1:], shuffle_board):
            return True
        board[i][j] = valid
    return False


def solve(board):
    empty_positions = []

    for i in range(9):
        for j in range(9):
            if filled(board, i, j):
                board = standard_constraints(board, i, j)
            else:
                empty_positions.append((i, j))

    search(board, empty_positions)


def check_board(board):
    for i in range(9):
        if len(set(board[i][j] for j in range(9))) < 9:
            return False

    for j in range(9):
        if len(set(board[i][j] for i in range(9))) < 9:
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = set()
            for k in range(i, i + 3):
                for h in range(j, j + 3):
                    box.add(board[k][h])
            if len(box) < 9:
                return False

    return True


def print_board(board):
    if board is None:
        print("NULL BOARD")
        return

    for i in range(9):
        if i > 0 and i % 3 == 0:
            print("- - - - - - - - - - - -")

        for j in range(9):
            if j > 0 and j % 3 == 0:
                print(" | ", end="")

            curr = str(board[i][j] if type(board[i][j]) is int else " ")
            # curr = str(board[i][j])

            if j == 9 - 1:
                print(curr)
            else:
                print(curr + " ", end="")
    print()


def read_file(filepath):
    with open(filepath) as input_file:
        board = []
        for i in range(9):
            board.append(list(int(s) for s in input_file.readline().split()))
            for j in range(9):
                if board[i][j] == 0:
                    board[i][j] = list(range(1, 10))
        return board


if __name__ == '__main__':
    board = read_file(sys.argv[1])

    print("Solving:")
    print_board(board)

    solve(board)
