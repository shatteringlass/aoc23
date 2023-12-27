from util import read_input

from itertools import combinations

i = read_input('day11').split('\n')


def find_empty_rows_and_cols(universe):

    nrows = len(universe)
    ncols = len(universe[0])

    candidate_rows = [x for x in range(nrows)]
    candidate_cols = [y for y in range(ncols)]

    for row in range(nrows):
        for col in range(ncols):
            if i[row][col] == '#':
                # print(f"Found galaxy at ({row},{col})")
                if row in candidate_rows:
                    candidate_rows.remove(row)
                if col in candidate_cols:
                    candidate_cols.remove(col)

    print(f"Universe has empty rows at {candidate_rows} and empty columns at {candidate_cols}")

    return candidate_rows, candidate_cols


def check_empty(a, b, empty_rows, empty_cols):
    # return the total amount of empty rows and columns offsetting points a and b
    er = len([r for r in empty_rows if a[0] < r < b[0] or b[0] < r < a[0]])
    ec = len([c for c in empty_cols if a[1] < c < b[1] or b[1] < c < a[1]])
    # print(f"Found {er} rows and {ec} columns.")
    return er + ec


def shortest_distance(a, b, empty_rows, empty_cols, multiplier):
    # find shortest path between every pair of galaxies (can only move up, down, left, right)
    # print(f"Checking distance between {a} and {b}")
    dist = abs(b[0]-a[0]) + abs(b[1]-a[1]) + check_empty(a,
                                                         b, empty_rows, empty_cols)*(multiplier-1)
    # print(f"Calculated distance is {dist}")
    return dist


def solve(part):
    universe = i

    galaxies = [(row, col)
                for row, r in enumerate(universe) for col, v in enumerate(r) if v == '#']

    empty_rows, empty_cols = find_empty_rows_and_cols(universe)

    if part == 1:
        # for line in i:
        #     print(line)

        # for line in universe:
        #     print(line)
        multiplier = 2

    elif part == 2:
        multiplier = 1000000

    print(f"Found {len(galaxies)} galaxies in universe.")

    pairs = combinations(galaxies, 2)

    return sum([shortest_distance(*p, empty_rows, empty_cols, multiplier) for p in pairs])


def main():
    print(f"Solution for part 1 is: {solve(1)}")
    print(f"Solution for part 2 is: {solve(2)}")


if __name__ == '__main__':
    main()
