from util import read_input
import enum

"""
Count the points on and inside the border.
"""


class Direction(enum.Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)


def count_inner_points(outer_points, perimeter):
    from itertools import pairwise
    shoelace_area = sum(r1*c2 - r2*c1 for (r1, c1),
                        (r2, c2) in pairwise(outer_points))/2
    picks_points = int(abs(shoelace_area) + perimeter//2 + 1)
    return picks_points


def step(start, dct, steps=1):
    dct = (steps*x for x in dct)
    return tuple(map(sum, zip(start, dct)))


def dig_trench(instructions, is_hex=False):
    hexdct = ('R', 'D', 'L', 'U')
    trench = [(0, 0)]
    perimeter = 0

    for inst in instructions:
        dct, length, hexcode = inst.split()

        if is_hex:
            *hex_length, hex_dct = hexcode[2:-1]
            length = int(''.join(hex_length), 16)
            dct = hexdct[int(hex_dct)]

        length = int(length)
        trench.append(step(trench[-1], Direction[dct].value, length))
        perimeter += length

    return trench, perimeter


def get_solution(part):

    solution = 0
    lines = read_input('day18').splitlines()

    if part == 1:
        solution = count_inner_points(*dig_trench(lines))
    elif part == 2:
        solution = count_inner_points(*dig_trench(lines, is_hex=True))

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
