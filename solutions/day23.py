from dataclasses import dataclass
import enum

from util import read_input


class Direction(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


@dataclass
class State:
    position: tuple[int, int, int]
    direction: Direction
    path: list[tuple[int, int, int]]


def step(position: tuple[int, int], direction: Direction):
    return tuple(map(sum, zip(position, direction.value)))


def parse_maze(maze: str):
    start, end, paths = None, None, set()
    slopes = {Direction.N: set(), Direction.S: set(),
              Direction.W: set(), Direction.E: set()}

    lines = maze.splitlines()
    rows, cols = len(lines), len(lines[0])

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '.':
                if row == 0 and col == 1:
                    start = (row, col)
                elif row == rows - 1 and col == cols - 2:
                    end = (row, col)
                paths.add((row, col))
            elif char == '<':
                slopes[Direction.W].add((row, col))
            elif char == '>':
                slopes[Direction.E].add((row, col))
            elif char == 'v':
                slopes[Direction.S].add((row, col))
            elif char == '^':
                slopes[Direction.N].add((row, col))

    return start, end, paths, slopes


def get_next_valid(cur_pos, cur_path, paths, slopes, slippery=True):
    for d in Direction:
        c = step(cur_pos, d)

        if c not in cur_path:

            if c in paths:
                yield c

            if slippery:
                if c in slopes[d]:
                    yield c
            else:
                if c in slopes:
                    yield c


def find_longest_walk(start, end, paths, slopes, slippery=True):
    stack = [(start, [start])]
    max_path = [start]

    while stack:
        cur_pos, path = stack.pop()

        # input(f"{cur_pos}, {path}")

        if cur_pos == end and len(path) > len(max_path):
            max_path = path.copy()

        for next_pos in get_next_valid(cur_pos, path, paths, slopes, slippery):
            stack.append((next_pos, path+[next_pos]))

    return max_path


def get_solution(part):

    solution = 0
    maze = read_input('day23')

    start, end, paths, slopes = parse_maze(maze)

    if part == 1:
        walk = find_longest_walk(start, end, paths, slopes)
    elif part == 2:
        walk = find_longest_walk(start, end, paths, set(x for s in slopes.values() for x in s), slippery=False)

    solution = len(walk)-1

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
