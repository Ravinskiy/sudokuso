import json
from typing import List, Callable


def print_grid(grid: List[List[int]]) -> None:
    for line in range(9):
        for column in range(9):
            print(grid[line][column], end='  ')
        print()


def validate_number(
    grid: List[List[int]],
    row: int,
    col: int,
    number: int
) -> bool:
    for index in range(9):
        if grid[row][index] == number:
            return False
    for index in range(9):
        if grid[index][col] == number:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for row in range(3):
        for column in range(3):
            if grid[row + start_row][column + start_col] == number:
                return False
    return True


def sudoku(
    grid: List[List[int]],
    row: int = 0,
    col: int = 0
) -> Callable[[List[List[int]], int, int], Callable]|bool:
    if (row == 8 and col == 9):
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return sudoku(grid, row, col + 1)
    for number in range(1, 9 + 1, 1):
        if validate_number(grid, row, col, number):
            grid[row][col] = number
            if sudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def main(grid: List[List[int]]) -> List[List[int]]:
    mutable_grid = list(grid)
    print_grid(grid)
    print()
    if sudoku(mutable_grid):
        print_grid(grid)
        print('\n\n')
    else:
        raise RuntimeError('Solution does not exist.')
    return mutable_grid


# input_grid = [
#     [2, 5, 0, 0, 3, 0, 9, 0, 1],
#     [0, 1, 0, 0, 0, 4, 0, 0, 0],
#     [4, 0, 7, 0, 0, 0, 2, 0, 8],
#     [0, 0, 5, 2, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 9, 8, 1, 0, 0],
#     [0, 4, 0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 3, 6, 0, 0, 7, 2],
#     [0, 7, 0, 0, 0, 0, 0, 0, 3],
#     [9, 0, 3, 0, 0, 0, 6, 0, 4]
# ]

# print_grid(input_grid)
# print()
# if (sudoku(input_grid)):
#     print_grid(input_grid)
# else:
#     print('Solution does not exist')


if __name__ == "__main__":
    input_filepath = 'inputs/sudokos.json'
    output_filepath = 'output_sudokos.json'
    input_file = open(input_filepath, mode='r', encoding='utf8')
    input_grids = json.load(input_file)
    input_file.close()
    output_grids = list()
    for input_grid in input_grids:
        output_grid = main(input_grid)
        output_grids.append(output_grid)
    output_file = open(output_filepath, mode='w', encoding='utf8')
    json.dump(output_grids, output_file)
    output_file.close()
