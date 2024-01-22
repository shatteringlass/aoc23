from util import read_input
from collections import deque
import enum

import dataclasses
import typing


class Direction(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


@dataclasses.dataclass(frozen=True)
class State:
    pos: typing.Tuple[int, int]
    steps_left: int

    @property
    def neighbors(self, directions=(Direction.N, Direction.S, Direction.W, Direction.E)):
        return tuple(
            State(
                tuple(
                    sum(coord) for coord in zip(self.pos, d.value)
                ),  self.steps_left-1
            ) for d in directions
        )


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

    # print(
    #    f"This puzzle starts from {start}, has {row+1} rows, {col+1} columns and a total of {len(gardens)} gardens")
    return rocks, gardens, start


def remap_state(state, size):
    pos_x, pos_y = state.pos
    result = State(
        (pos_x % size, pos_y % size),
        state.steps_left)
    return result


def print_map(pos, points, moves, max_x, max_y):
    for i in range(max_x):
        print(''.join(['S' if pos == (i, j) else 'O' if (i, j) in moves else '.' if (
            i, j) in points else '#' for j in range(max_y)]))


def walk_to_gardens(start, gardens, steps, size):
    result = dict()
    queue = deque([State(start, steps)])
    seen = set()

    while queue:
        pos = queue.popleft()
        if (pos.steps_left == -1) or (pos.pos in seen):
            continue

        result.setdefault(steps - pos.steps_left, 0)
        result[steps - pos.steps_left] += 1
        seen.add(pos.pos)

        for neighbor in pos.neighbors:
            remapped = remap_state(neighbor, size)
            if remapped.pos in gardens:
                queue.append(neighbor)

    return sum(amount for distance, amount in result.items() if distance % 2 == steps % 2)


def three_point_formula(y, n):
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c


def get_solution(part):

    solution = 0

    puzzle = read_input('day21').splitlines()
    rocks, gardens, start = parse_puzzle_input(puzzle)

    if part == 1:
        steps = 64
        solution = walk_to_gardens(start, gardens, steps, len(puzzle))

    elif part == 2:
        goal = 26501365
        size = len(puzzle[1])
        edge = size // 2
        steps = tuple(edge + i * size for i in range(3))
        y = [
            walk_to_gardens(start, gardens, s, size)
            for s in steps
        ]

        return three_point_formula(y, ((goal - edge) // size))

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
