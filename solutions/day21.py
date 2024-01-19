from util import read_input

from collections import deque

import enum


class Direction(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


def parse_puzzle_input(puzzle):
    rocks, gardens, start = set(), set(), None

    for row, line in enumerate(puzzle):
        for col, cell in enumerate(line):
            point = (row, col)
            if cell == '.':
                gardens.add(point)
            if cell == '#':
                rocks.add(point)
            if cell == 'S':
                gardens.add(point)
                start = point

    print(f"This puzzle starts from {start}, has {row+1} rows, {col+1} columns and a total of {len(gardens)} gardens")
    return rocks, gardens, start, row+1, col+1


def get_valid_moves(pos, good, directions=(Direction.N, Direction.S, Direction.W, Direction.E)):
    moves = []
    for d in directions:
        point = tuple(sum(coord) for coord in zip(pos, d.value))
        if point in good:
            moves.append(point)

    print(f"Valid moves from {pos}: {moves}")
    return moves


def print_map(pos, points, moves, max_x, max_y):
    for i in range(max_x):
        print(''.join(['S' if pos == (i, j) else 'O' if (i,j) in moves else '.' if (i,j) in points else '#' for j in range(max_y)]))


def walk_to_gardens(start, gardens, steps, max_x, max_y):
    found = set()
    queue = deque([start])
    max_steps = steps

    while steps and queue:
        print(f"At step {max_steps-steps+1}")
        pos = queue.popleft()
        found.add(pos)
        moves = get_valid_moves(pos, gardens)
        print(f"Found {len(moves)} valid moves.")
        queue.extend(moves)
        steps -= 1
        print_map(pos, gardens, moves, max_x, max_y)

    return len(found)


def get_solution(part):

    solution = 0

    puzzle = read_input('day21_small').splitlines()
    rocks, gardens, start, max_x, max_y = parse_puzzle_input(puzzle)

    if part == 1:
        solution = walk_to_gardens(start, gardens, 12, max_x, max_y)

    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
