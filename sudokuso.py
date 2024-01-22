import argparse
import json
from typing import List, Callable

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input',
    required=True,
    type=str,
    help='Input JSON file path'
)
parser.add_argument(
    '-o',
    '--output',
    required=True,
    type=str,
    help='Output JSON file path'
)


def print_grid(grid: List[List[int]]) -> None:
    for line in range(9):
        for column in range(9):
            print(grid[line][column], end='  ')
        print()


def tranpose_grid(grid: List[List[int]]) -> List[List[int]]:
    transposed_tuples = list(zip(*grid))
    transposed = [list(sublist) for sublist in transposed_tuples]
    return transposed


def unfold_cells(grid: List[List[int]]) -> List[List[int]]:
    cells = list()
    for line in range(0, 9, 3):
        for column in range(0, 9, 3):
            cell = []
            for row in range(line, line + 3):
                for col in range(column, column + 3):
                    cell.append(grid[row][col])
            cells.append(cell)
    return cells


def grid_valid(grid: List[List[int]]) -> bool:
    valid = True
    lines = list()
    transposed_grid = tranpose_grid(grid)
    unfolded_cells = unfold_cells(grid)
    lines.extend(grid)
    lines.extend(transposed_grid)
    lines.extend(unfolded_cells)
    for line in lines:
        empty_count = line.count(0)
        empty_correction = int(bool(empty_count))
        numbers_count = len(line) - empty_count + empty_correction
        unique_count = len(set(line))
        diff = numbers_count - unique_count
        if diff:
            valid = False
            break
    return valid


def number_valid(
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
) -> Callable[[List[List[int]], int, int], Callable|bool]|bool:
    if (row == 8 and col == 9):
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return sudoku(grid, row, col + 1)
    for number in range(1, 10, 1):
        if number_valid(grid, row, col, number):
            grid[row][col] = number
            if sudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def solve(grid: List[List[int]]) -> List[List[int]]:
    print_grid(grid)
    print()
    if sudoku(grid):
        print_grid(grid)
        print('\n\n')
    else:
        raise RuntimeError('Solution does not exist.')
    return grid


if __name__ == "__main__":
    args = parser.parse_args()
    input_filepath = args.input
    output_filepath = args.output
    input_file = open(input_filepath, mode='r', encoding='utf8')
    input_grids = json.load(input_file)
    input_file.close()
    output_grids = list()
    for input_grid in input_grids:
        if not grid_valid(input_grid):
            print_grid(input_grid)
            raise RuntimeError('The grid is not valid.')
        output_grid = solve(input_grid)
        output_grids.append(output_grid)
    output_file = open(output_filepath, mode='w', encoding='utf8')
    json.dump(output_grids, output_file)
    output_file.close()
