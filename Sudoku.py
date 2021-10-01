# This Program is able to solve sudoku puzzles that are pulled from
# from a HTTP get request using backtracking and recursion

from time import time

import requests

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def get_board(eb):
    # Calls a new sudoku board and sets the given points into the empty board

    level = input("Enter a difficulty (1, 2, 3). Higher difficulty may take longer: ")
    r = requests.get('http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=' + str(level))
    r.raise_for_status()

    jsonResponse = r.json()

    for i in jsonResponse['squares']:
        eb[i['x']][i['y']] = i['value']

    return eb


def print_board(b):
    # Print the rows and columns of the board to divide into sudoku sections

    for i in range(len(b)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(b[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end="")

            if j == 8:
                print(b[i][j])
            else:
                print(str(b[i][j]) + " ", end="")


def find_empty(b):
    # Iterate through grid to find '0'

    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return i, j

    return None


def check_valid(b, n, p):
    # Check row

    for i in range(len(b[0])):
        if b[p[0]][i] == n and p[1] != i:
            return False

    # Check column

    for i in range(len(b[0])):
        if b[i][p[1]] == n and p[0] != i:
            return False

    # Check box

    x = p[1] // 3
    y = p[0] // 3

    for i in range(y * 3, y * 3 + 3):
        for j in range(x * 3, x * 3 + 3):
            if b[i][j] == n and (i, j) != p:
                return False

    return True


def solve_board(b):
    # Driver code run recursively

    if not find_empty(b):
        return True
    else:
        x, y = find_empty(b)

    for i in range(1, 10):
        if check_valid(b, i, (x, y)):
            b[x][y] = i

            if solve_board(b):
                return True

            b[x][y] = 0

    return False


print_board(get_board(board))
print('\n')

start = int(time() * 1000)
solve_board(board)
end = int(time() * 1000)

print_board(board)
print("\nTime taken to solve = " + str((end - start)) + " milliseconds ")
