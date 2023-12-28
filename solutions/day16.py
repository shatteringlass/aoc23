import enum
import collections


from util import read_input


grid = read_input('day16').splitlines()
rows = len(grid)
cols = len(grid[0])


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def follow_path(grid, start_row=0, start_col=0, start_dir=Direction.RIGHT):

    queue = collections.deque([(start_row, start_col, start_dir)])
    seen = set()
    path = set()

    while queue:

        r, c, d = queue.pop()

        if (r, c, d) not in seen and r >= 0 and r < rows and c >= 0 and c < cols:
            # print(f"Checking cell {r,c} with symbol {grid[r][c]} traveling in d {d.name}, current path is {len(path)} cells long.")
            path.add((r, c))
            seen.add((r, c, d))

            if grid[r][c] == '.':
                queue.append(
                    (r+d.value[0], c+d.value[1], d))
            elif grid[r][c] == '|':
                if d in (Direction.RIGHT, Direction.LEFT):
                    queue.append((r-1, c, Direction.UP))
                    queue.append((r+1, c, Direction.DOWN))
                else:
                    queue.append(
                        (r+d.value[0], c+d.value[1], d))
            elif grid[r][c] == '-':
                if d in (Direction.UP, Direction.DOWN):
                    queue.append((r, c-1, Direction.LEFT))
                    queue.append((r, c+1, Direction.RIGHT))
                else:
                    queue.append(
                        (r+d.value[0], c+d.value[1], d))
            elif grid[r][c] == '/':
                # reflect 90 degrees (RU, LD)
                d = Direction(tuple(-x for x in d.value[::-1]))
                queue.append(
                    (r+d.value[0], c+d.value[1], d))
            elif grid[r][c] == '\\':
                # reflect 90 degrees (RD, LU)
                d = Direction(tuple(x for x in d.value[::-1]))
                queue.append(
                    (r+d.value[0], c+d.value[1], d))

    return path


def print_path(path, height, width):
    for r in range(height):
        line = ['#' if (r, c) in path else '.' for c in range(width)]
        print(line)


def get_solution(part):

    solution = 0

    if part == 1:
        paths = follow_path(grid)
        solution = len(paths)

    elif part == 2:

        for row in (0,rows-1):
            for col in (0,cols-1):
                for d in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
                    solution = max(solution, len(follow_path(grid, row, col, d)))


    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
