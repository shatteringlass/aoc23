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
    tile: typing.Tuple[int, int]
    steps_left: int

    @property
    def neighbors(self, directions=(Direction.N, Direction.S, Direction.W, Direction.E)):
        return tuple(State(tuple(sum(coord) for coord in zip(self.pos, d.value)), self.tile, self.steps_left-1) for d in directions)


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


def remap_state(state, modulo):
    pos = (state.pos[0] % modulo, state.pos[1] % modulo)
    tile = state.tile
    return State(pos, tile, state.steps_left)


def print_map(pos, points, moves, max_x, max_y):
    for i in range(max_x):
        print(''.join(['S' if pos == (i, j) else 'O' if (i, j) in moves else '.' if (
            i, j) in points else '#' for j in range(max_y)]))


def walk_to_gardens(start, gardens, steps, modulo):
    result = set()
    queue = deque([State(start, (0, 0), steps)])
    seen = set()

    while queue:
        pos = queue.popleft()
        if pos.steps_left >= 0:

            if pos.steps_left % 2 == steps % 2:
                result.add(pos.pos)

            if pos.steps_left > 0:
                for neighbor in pos.neighbors:
                    neighbor = remap_state(neighbor, modulo)
                    if neighbor.pos in gardens and neighbor not in seen:
                        queue.append(neighbor)
                        seen.add(neighbor)

    return len(result)


def three_point_formula(p1, p2, p3):
    c = p1
    b = (4*p2 - 3*p1 - p3) // 2
    a = p2 - p1 - b
    return a, b, c


def get_solution(part):

    solution = 0

    puzzle = read_input('day21').splitlines()
    rocks, gardens, start = parse_puzzle_input(puzzle)

    if part == 1:
        steps = 64
        solution = walk_to_gardens(start, gardens, steps, len(puzzle))

    elif part == 2:
        steps = 26501365
        period = 65
        samples = tuple(period + i*len(puzzle) for i in range(3))
        p = tuple(walk_to_gardens(start, gardens, s, len(puzzle))
                  for s in samples)
        a, b, c = three_point_formula(*p)
        x = (steps - len(puzzle)//2)
        solution = a*x**2 + b*x + c

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
