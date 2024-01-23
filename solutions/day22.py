from util import read_input
import dataclasses
from typing import Tuple
import enum


class Axis(enum.Enum):
    X = 0
    Y = 1
    Z = 2


@dataclasses.dataclass(frozen=True)
class Brick:
    start: Tuple[int, int, int]
    end: Tuple[int, int, int]

    def min_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(min, axis)

    def max_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(max, axis)

    def _axis_limit(self, func, axis: Axis) -> int:
        return func(self.start[axis.value], self.end[axis.value])

    def __lt__(self, other: "Brick") -> bool:
        return self.min_for_axis(Axis.Z) < other.min_for_axis(Axis.Z)

    def update_z(self, new_z: int) -> "Brick":
        delta = (0, 0, self.min_for_axis(Axis.Z) - new_z)
        return Brick(*(tuple(map(sum, zip(coord, delta))) for coord in (self.start, self.end)))

    @property
    def height(self) -> int:
        return (self.max_for_axis(Axis.Z) - self.min_for_axis(Axis.Z) + 1)

    @property
    def area_xy(self) -> tuple[tuple[int, int]]:
        return (
            (
                self.min_for_axis(Axis.X),
                self.min_for_axis(Axis.Y)
            ),
            (
                self.max_for_axis(Axis.X),
                self.max_for_axis(Axis.Y)
            )
        )

    def intersects(self, other: "Brick") -> bool:
        this_area = self.area_xy()
        other_area = other.area_xy()

        # check if they are next to one another
        if False:
            return False

        # check if they are on top of one another
        if False:
            return False

        return True


def parse_brick(coords):
    points = ((int(c) for c in p.split(",")) for p in coords.split("~"))
    return Brick(*points)


def get_solution(part):

    solution = 0

    bricks = read_input('day22').splitlines()

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
