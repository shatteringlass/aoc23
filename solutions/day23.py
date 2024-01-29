import enum
from collections import defaultdict
from util import read_input


class Direction(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


def step(position: tuple[int, int], direction: Direction):
    return tuple(map(sum, zip(position, direction.value)))


def parse_maze(maze: str):
    start, end, paths = None, None, set()
    slopes = {Direction.N: set(),
              Direction.S: set(),
              Direction.W: set(),
              Direction.E: set()}

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


def get_next_valid(cur_pos, paths, slopes, slippery=True):
    return (
        step(cur_pos, d) for d in Direction
        if step(cur_pos, d) in paths
        or (slippery and step(cur_pos, d) in slopes[d])
    )


def find_nodes(paths, slopes, slippery=True):
    nodes = defaultdict(set)

    for p in paths:
        for n in get_next_valid(p, paths, slopes, slippery):
            nodes.setdefault(p, set()).add(n)
            nodes.setdefault(n, set()).add(p)

    if slippery:
        for s in set(x for subset in slopes.values() for x in subset):
            for n in get_next_valid(s, paths, slopes, slippery):
                nodes.setdefault(s, set()).add(n)
                nodes.setdefault(n, set()).add(s)

    return set(node
               for node, neighbors in nodes.items()
               if len(neighbors) > 2)


def find_edges(paths, slopes, nodes, slippery=True):
    edges = defaultdict(set)

    for j in nodes:
        queue = [(j, 0)]
        seen = set()

        while queue:
            (x, y), dist = queue.pop(0)

            if (x, y) in seen:
                continue

            seen.add((x, y))

            for n in get_next_valid((x, y), paths, slopes, slippery):
                if n in nodes and n != j:
                    edges.setdefault(j, set()).add((n, dist+1))
                else:
                    queue.append((n, dist+1))
    return edges


def find_longest_walk(start, end, edges):
    stack = [(start, [start], 0)]

    valid_paths = []

    while stack:
        current, path, pathlen = stack.pop()

        if current == end:
            valid_paths.append((path, pathlen))
            continue

        for next_node, distance in edges[current]:
            if next_node not in path:
                new_path = path + [next_node]
                stack.append((next_node, new_path, pathlen+distance))

    return sorted(valid_paths, key=lambda x: x[1])[-1]


def get_solution(part):

    solution = 0
    maze = read_input('day23')

    start, end, paths, slopes = parse_maze(maze)
    slippery = True

    if part == 1:
        pass
    elif part == 2:
        slippery = False
        paths = paths.union(set(x for s in slopes.values() for x in s))

    nodes = find_nodes(paths, slopes, slippery=slippery)
    edges = find_edges(paths, slopes, nodes.union({start, end}))

    max_path, solution = find_longest_walk(start, end, edges)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
