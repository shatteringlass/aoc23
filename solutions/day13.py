from util import read_input


def distance(l, r):
    return sum(a != b for a, b in zip(l, r))


def transpose(grid):
    return list(zip(*grid))


def find_reflected_rows(grid, diffs=0):
    for idx in range(len(grid)):
        if idx == 0:
            continue

        if (
            sum(
                distance(l, r)
                for l, r in zip(
                    reversed(grid[:idx]),
                    grid[idx:]
                )
            )
            == diffs
        ):
            return idx

    return 0


def get_solution(part):

    solution = 0

    i = read_input('day13').split('\n\n')

    puzzles = [puzzle.splitlines() for puzzle in i]
    puzzles_t = [transpose(puzzle.splitlines()) for puzzle in i]

    for grid in puzzles:
        solution += find_reflected_rows(grid,
                                        diffs=0 if part == 1 else 1)*100

    for grid in puzzles_t:
        solution += find_reflected_rows(grid, diffs=0 if part == 1 else 1)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
