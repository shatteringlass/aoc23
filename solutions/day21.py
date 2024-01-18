from util import read_input


def parse_puzzle_input(puzzle):
    rocks, gardens, start = set(), set(), None

    for row, line in enumerate(puzzle):
        for col, cell in enumerate(line):
            point = (row, col)
            if cell == '.':
                gardens.add(point)
            if cell == '#':
                rocks.add(point)
            else:
                start = point

    return rocks, gardens, start


def get_valid_moves(pos, good, bad, max_x, max_y):
    pass


def get_solution(part):

    solution = 0

    puzzle = read_input('day21').splitlines()
    rocks, gardens, start = parse_puzzle_input(puzzle)

    if part == 1:
        print(rocks, gardens, start)
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
