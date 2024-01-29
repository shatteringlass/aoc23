import dataclasses
from util import read_input
import fractions

TEST_AREA = ((200_000_000_000_000, 200_000_000_000_000),
             (400_000_000_000_000, 400_000_000_000_000))


"""
Each stone moves along the line defined by the following parametric equation:

P(t) = P + V*t

where P is position and V is velocity.

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
        return (self.position[i] + t * self.velocity[i] for i, _ in enumerate(self.position))

    def intersects(self, other):

        det = self.vy*other.vx - self.vx*other.vy
        if det != 0:
            t1 = (other.vx*(other.py-self.py) -
                  other.vy*(other.px-self.px))/det
            t2 = (self.vx*(other.py-self.py) - self.vy*(other.px-self.px))/det
            intersect = (t1, t2)
            #print(f"Line {self} intersects {other} at {intersect}")
        else:
            intersect = None

        return intersect

    @classmethod
    def from_str(cls, string):
        position, velocity = tuple(
            tuple(int(y) for y in x.split(',')) for x in string.split(" @ "))
        return Hailstone(position, velocity)


def check_intersections(stones, min_value, max_value):
    intersections = 0

    for idx, stone in enumerate(stones):
        for jdx, other_stone in enumerate(stones[idx+1:]):
            intersect = stone.intersects(other_stone)
            if intersect:
                t0, t1 = intersect
                pxt, pyt, pyz = stone.position_at_time(intersect[0])
                if t0 > 0 and t1 > 0 and (min_value <= pxt <= max_value) and (min_value <= pyt <= max_value):
                    intersections += 1

    return intersections


def get_solution(part):

    solution = 0
    data = read_input('day24').splitlines()

    stones = tuple(Hailstone.from_str(line) for line in data)

    if part == 1:
        solution = check_intersections(
            stones, TEST_AREA[0][0], TEST_AREA[1][1])
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
