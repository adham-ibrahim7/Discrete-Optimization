def print_board(board):
    for i in range(len(board)):
        if i > 0 and i % 3 == 0:
            print("- - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j > 0 and j % 3 == 0:
                print(" | ", end="")

            if j == len(board[0])-1:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


if __name__ == '__main__':
    print_board([[1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9]])
