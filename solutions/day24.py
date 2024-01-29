import dataclasses
from util import read_input

TEST_AREA = ((200_000_000_000_000, 200_000_000_000_000),
             (400_000_000_000_000, 400_000_000_000_000))


"""
The system dynamic is described by the following system of equations:

P(t) = P + V*t

In part 1, reduce to a n**2 system of equations and compute 
the number of linearly independent vectors that intersect in the test area.

"""

@dataclasses.dataclass
class Hailstone:

    position: tuple[int, int, int]
    velocity: tuple[int, int, int]

    @classmethod
    def from_str(cls, string):
        position, velocity = tuple(
            tuple(int(y) for y in x.split(',')) for x in string.split(" @ "))
        return Hailstone(position, velocity)


def get_solution(part):

    solution = 0
    data = read_input('day24').splitlines()

    stones = tuple(Hailstone.from_str(line) for line in data)

    input(stones)

    if part == 1:
        pass
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
