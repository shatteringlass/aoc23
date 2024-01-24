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
                if row == 0:
                    start = (row, col)
                elif row == cols - 1:
                    end = (row, col)
                else:
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


def get_next_valid(position, paths, slopes):
    for d in Direction:
        c = step(position, d)
        if c in paths:
            yield c, d
        elif c in slopes[d]:
            yield c, d


def find_longest_walk(start, end, paths, slopes):
    stack = [(start, Direction.S, [start])]
    max_path = [start]

    while stack:
        cur_pos, direction, path = stack.pop()

        if cur_pos == end and len(path) > max_path:
            max_path = path.copy()

        for (next_pos, next_dir) in get_next_valid(cur_pos, paths, slopes):
            if next_pos not in path:
                stack.append((next_pos, next_dir, path+[next_pos]))

    return max_path


def get_solution(part):

    solution = 0
    maze = read_input('day23')

    start, end, paths, slopes = parse_maze(maze)

    if part == 1:
        walk = find_longest_walk(start, end, paths, slopes)
        print(walk)
        solution = len(walk)
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
