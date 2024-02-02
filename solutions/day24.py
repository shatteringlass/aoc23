from random import choice
from itertools import combinations
from typing import Optional, List, Union
import dataclasses
from util import read_input

TEST_AREA = ((200_000_000_000_000, 200_000_000_000_000),
             (400_000_000_000_000, 400_000_000_000_000))


"""
Each stone moves along the line defined by the following parametric equation:

P(t) = P + V*t

where P is position and V is velocity.

For part 2, pick any 3 linearly independent trajectories and solve
the 6 linear equation system derived from their intersection.

"""


@dataclasses.dataclass
class Hailstone:

    position: tuple[int, int, int]
    velocity: tuple[int, int, int]

    @property
    def px(self):
        return self.position[0]

    @property
    def py(self):
        return self.position[1]

    @property
    def pz(self):
        return self.position[2]

    @property
    def vx(self):
        return self.velocity[0]

    @property
    def vy(self):
        return self.velocity[1]

    @property
    def vz(self):
        return self.velocity[2]

    def position_at_time(self, t):
        return tuple(self.position[i] + t * self.velocity[i] for i, _ in enumerate(self.position))

    def adjust(self, frame):
        return Hailstone(self.position, tuple(c-f for c, f in zip(self.velocity, frame)))

    def intersects_xy(self, other):

        det = self.vy*other.vx - self.vx*other.vy
        if det != 0:
            t1 = (other.vx*(other.py-self.py) -
                  other.vy*(other.px-self.px))/det
            t2 = (self.vx*(other.py-self.py) - self.vy*(other.px-self.px))/det
            intersect = (t1, t2)
            # print(f"Line {self} intersects {other} at {intersect}")
        else:
            intersect = None

        return intersect

    @classmethod
    def from_str(cls, string):
        position, velocity = tuple(
            tuple(int(y) for y in x.split(',')) for x in string.split(" @ "))
        return Hailstone(position, velocity)


def find_intersection(stone, other):
    intersect = stone.intersects_xy(other)
    if intersect:
        t0, t1 = intersect
        pxt, pyt, pzt = stone.position_at_time(intersect[0])
        return ((pxt, pyt, pzt), (t0, t1))
    return None


def check_intersections(stones, min_value, max_value):
    intersections = 0

    for idx, stone in enumerate(stones):
        for jdx, other_stone in enumerate(stones[idx+1:]):
            intersection = find_intersection(stone, other_stone)
            if intersection:
                (pxt, pyt, pzt), (t0, t1) = intersection
                if t0 > 0 and t1 > 0 and (min_value <= pxt <= max_value) and (min_value <= pyt <= max_value):
                    intersections += 1

    return intersections


# Credit to github.com/ethanlu/advent-of-code for the gaussian elimination algorithm
def _solve_matrix_equations(matrix: List[List[Union[int, float]]]) -> Optional[List[float]]:
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            return None
        matrix[i] = [matrix[i][k] / matrix[i][i]
                     for k in range(len(matrix[i]))]
        for j in range(i + 1, len(matrix)):
            matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i]
                         for k in range(len(matrix[i]))]

    # back substituion
    for i in reversed(range(len(matrix))):
        for j in range(i):
            matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i]
                         for k in range(len(matrix[i]))]

    return [round(r[-1], 2) for r in matrix]


def find_perfect_shot(trajectories, xy_range=(-500, 500)):
    def xy_coefficients(h: Hailstone) -> List[int]:
        return [
            h.velocity[0],
            -h.velocity[1],
            h.position[0],
            h.position[1],
            h.position[1] * h.velocity[0] - h.position[0] * h.velocity[1]
        ]

    def yz_coefficients(h: Hailstone) -> List[int]:
        return [
            h.velocity[1],
            -h.velocity[2],
            h.position[1],
            h.position[2],
            h.position[2] * h.velocity[1] - h.position[1] * h.velocity[2]
        ]

    # solve for xy and yz using 4 hails and a randomly selected hail
    solution = 0

    for batch in combinations(trajectories, 4):
        random_hail = choice(trajectories)
        xy_matrix = [
            [a - b for a, b in zip(c, xy_coefficients(random_hail))]
            for c in [xy_coefficients(h) for h in batch]
        ]
        xy_solve = _solve_matrix_equations(xy_matrix)
        if xy_solve is None:
            continue

        yz_matrix = [
            [a - b for a, b in zip(c, yz_coefficients(random_hail))]
            for c in [yz_coefficients(h) for h in batch]
        ]
        yz_solve = _solve_matrix_equations(yz_matrix)
        if yz_solve is None:
            continue

        solution = xy_solve[0] + xy_solve[1] + yz_solve[0]
        
        if solution % 1 == 0.0:
            break

    return int(solution)


def get_solution(part):

    solution = 0
    data = read_input('day24').splitlines()

    stones = tuple(Hailstone.from_str(line) for line in data)

    if part == 1:
        solution = check_intersections(
            stones, TEST_AREA[0][0], TEST_AREA[1][1])
    elif part == 2:
        solution = find_perfect_shot(stones)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
